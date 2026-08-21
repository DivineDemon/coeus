"""
Orchestrator for running Haga daily pipelines at 1PM PKT.
- Quota Check runs FIRST
- If quota allows, remaining pipelines run SEQUENTIALLY
"""

import asyncio
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any

# Add the pipelines directory to path
PIPELINES_DIR = Path(__file__).parent / "pipelines"
sys.path.insert(0, str(PIPELINES_DIR))

# Add automation directory for whatsapp_notifier
AUTOMATION_DIR = Path(__file__).parent
sys.path.insert(0, str(AUTOMATION_DIR))

from pipelines import (
    DesignPartnerDiscoveryPipeline,      # Pipeline A
    InvestorLeadGenerationPipeline,       # Pipeline B
    LeadEnrichmentPipeline,               # Pipeline C
    CompetitorDiscoveryPipeline,          # Pipeline D
    CompetitorForensicsPipeline,          # Pipeline E
    QuotaCheckPipeline,                   # Pipeline F (runs FIRST)
)

# Import WhatsApp notifier
WHATSAPP_AVAILABLE = False  # WhatsApp integration removed by user request (2026-08-21)


async def run_pipeline(pipeline) -> Dict[str, Any]:
    """Run a single pipeline with error handling."""
    name = pipeline.name
    print(f"\n{'='*60}")
    print(f"▶️  STARTING: {name}")
    print(f"{'='*60}")

    try:
        result = await pipeline.run()
        await pipeline.close()
        print(f"\n✅ COMPLETED: {name} - Status: {result.status}")
        return {"pipeline": name, "result": result, "error": None}
    except Exception as e:
        print(f"\n❌ FAILED: {name} - Error: {e}")
        import traceback
        traceback.print_exc()
        return {"pipeline": name, "result": None, "error": str(e)}


async def check_quota_and_proceed() -> Dict[str, Any]:
    """
    Run quota check first. If quota allows, run remaining pipelines sequentially.
    """
    print(f"\n{'#'*60}")
    print(f"#  HAGA DAILY PIPELINE ORCHESTRATOR")
    print(f"#  Scheduled: 1PM PKT Daily")
    print(f"#  Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S %Z')}")
    print(f"{'#'*60}")

    # ============================================================
    # STEP 1: Run Quota Check FIRST
    # ============================================================
    print(f"\n{'='*60}")
    print(f"🔍 STEP 1: QUOTA CHECK (Pipeline F)")
    print(f"{'='*60}")
    
    quota_pipeline = QuotaCheckPipeline()
    quota_result = await run_pipeline(quota_pipeline)
    
    if quota_result["error"]:
        print(f"\n❌ Quota check failed: {quota_result['error']}")
        return build_failure_summary(quota_result)
    
    quota_data = quota_result["result"].metadata if quota_result["result"] else {}
    health = quota_data.get("health_assessment", {})
    health_status = health.get("health", "unknown")
    total_remaining = health.get("total_remaining", 0)
    usage_pct = health.get("usage_percentage", 100)
    
    print(f"\n📊 Quota Health: {health_status.upper()}")
    print(f"📊 Total Remaining: {total_remaining}")
    print(f"📊 Usage: {usage_pct}%")
    
    # Check if we have enough quota to proceed
    # Threshold: need at least 10% remaining or health != critical
    if health_status == "critical" or total_remaining < 200:
        print(f"\n⛔ INSUFFICIENT QUOTA - Aborting remaining pipelines")
        print(f"   Health: {health_status}, Remaining: {total_remaining}")
        return build_quota_denied_summary(quota_result, health)
    
    print(f"\n✅ QUOTA OK - Proceeding with remaining pipelines")
    
    # ============================================================
    # STEP 2: Run remaining pipelines SEQUENTIALLY
    # ============================================================
    print(f"\n{'='*60}")
    print(f"🚀 STEP 2: RUNNING PIPELINES SEQUENTIALLY")
    print(f"{'='*60}")
    
    remaining_pipelines = [
        DesignPartnerDiscoveryPipeline(),      # Pipeline A
        InvestorLeadGenerationPipeline(),       # Pipeline B
        LeadEnrichmentPipeline(),               # Pipeline C
        CompetitorDiscoveryPipeline(),          # Pipeline D
        CompetitorForensicsPipeline(),          # Pipeline E
    ]
    
    print(f"\n📦 Initialized {len(remaining_pipelines)} pipelines for sequential execution")
    for i, p in enumerate(remaining_pipelines, 1):
        print(f"  {i}. {p.name}")
    
    start_time = datetime.now()
    all_results = [quota_result]  # Include quota result
    
    for pipeline in remaining_pipelines:
        result = await run_pipeline(pipeline)
        all_results.append(result)
        
        # Optional: brief pause between pipelines to be polite to servers
        if pipeline != remaining_pipelines[-1]:
            print(f"  ⏸️  Brief pause before next pipeline...")
            await asyncio.sleep(2)
    
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()
    
    # ============================================================
    # Generate summary
    # ============================================================
    successful = []
    failed = []
    
    for r in all_results:
        if isinstance(r, Exception):
            failed.append({"pipeline": "unknown", "error": str(r)})
        elif isinstance(r, dict) and r.get("error"):
            failed.append({"pipeline": r["pipeline"], "error": r["error"]})
        elif isinstance(r, dict):
            successful.append(r)
    
    summary = {
        "timestamp": datetime.now().isoformat(),
        "duration_seconds": round(duration, 2),
        "total_pipelines": len(all_results),
        "successful": len(successful),
        "failed": len(failed),
        "quota_checked": True,
        "quota_health": health_status,
        "quota_remaining": total_remaining,
        "pipelines": {}
    }
    
    for r in successful:
        res = r["result"]
        summary["pipelines"][r["pipeline"]] = {
            "status": res.status,
            "total_processed": res.total_processed,
            "with_emails": res.with_emails,
            "verified": res.verified,
            "total_emails": res.total_emails,
        }
    
    for f in failed:
        summary["pipelines"][f["pipeline"]] = {
            "status": "failed",
            "error": f["error"]
        }
    
    # Print final summary
    print(f"\n{'='*60}")
    print(f"📊 ORCHESTRATION COMPLETE")
    print(f"{'='*60}")
    print(f"⏱️  Duration: {duration:.1f} seconds")
    print(f"✅ Successful: {len(successful)}/{len(all_results)}")
    print(f"❌ Failed: {len(failed)}/{len(all_results)}")
    
    for name, info in summary["pipelines"].items():
        if info.get("status") == "failed":
            print(f"  ❌ {name}: {info.get('error', 'Unknown error')}")
        else:
            print(f"  ✅ {name}: {info.get('total_processed', 0)} processed, {info.get('total_emails', 0)} emails")
    
    # Save orchestration summary
    save_orchestration_summary(summary)
    
    return summary


def build_failure_summary(quota_result: Dict[str, Any]) -> Dict[str, Any]:
    """Build summary when quota check itself fails."""
    return {
        "timestamp": datetime.now().isoformat(),
        "duration_seconds": 0,
        "total_pipelines": 1,
        "successful": 0,
        "failed": 1,
        "quota_checked": True,
        "quota_health": "error",
        "quota_remaining": 0,
        "pipelines": {
            "Pipeline F: Quota Check": {
                "status": "failed",
                "error": quota_result.get("error", "Unknown error")
            }
        }
    }


def build_quota_denied_summary(quota_result: Dict[str, Any], health: Dict[str, Any]) -> Dict[str, Any]:
    """Build summary when quota check denies execution."""
    return {
        "timestamp": datetime.now().isoformat(),
        "duration_seconds": 0,
        "total_pipelines": 6,
        "successful": 1,  # Quota check ran successfully
        "failed": 0,
        "quota_checked": True,
        "quota_denied": True,
        "quota_health": health.get("health", "unknown"),
        "quota_remaining": health.get("total_remaining", 0),
        "pipelines": {
            "Pipeline F: Quota Check": {
                "status": "success",
                "total_processed": quota_result["result"].total_processed if quota_result["result"] else 0,
                "total_emails": 0,
                "verified": 0
            },
            "Pipeline A: Design Partner Discovery": {"status": "skipped", "reason": "quota_denied"},
            "Pipeline B: Investor Lead Generation": {"status": "skipped", "reason": "quota_denied"},
            "Pipeline C: Lead Enrichment": {"status": "skipped", "reason": "quota_denied"},
            "Pipeline D: Competitor Discovery": {"status": "skipped", "reason": "quota_denied"},
            "Pipeline E: Competitor Forensics": {"status": "skipped", "reason": "quota_denied"},
        }
    }


def save_orchestration_summary(summary: Dict[str, Any]):
    """Save orchestration summary to logs."""
    log_dir = Path(__file__).parent.parent.parent.parent / "logs" / f"orchestration-{datetime.now().strftime('%Y-%m-%d')}"
    log_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    
    # Save JSON
    json_path = log_dir / f"{timestamp}_orchestration_summary.json"
    with open(json_path, "w") as f:
        import json
        json.dump(summary, f, indent=2)
    
    # Save Markdown
    md_path = log_dir / f"{timestamp}_orchestration_summary.md"
    with open(md_path, "w") as f:
        f.write(generate_orchestration_markdown(summary))
    
    print(f"\n📝 Orchestration summary saved:")
    print(f"  - {json_path}")
    print(f"  - {md_path}")


def generate_orchestration_markdown(summary: Dict[str, Any]) -> str:
    """Generate markdown report for orchestration."""
    quota_denied = summary.get("quota_denied", False)
    quota_health = summary.get("quota_health", "unknown")
    quota_remaining = summary.get("quota_remaining", 0)
    
    lines = [
        f"# Daily Pipeline Orchestration Summary",
        "",
        f"**Date:** {datetime.now().strftime('%Y-%m-%d')}  ",
        f"**Time:** {datetime.now().strftime('%H:%M:%S')} PKT  ",
        f"**Duration:** {summary['duration_seconds']} seconds  ",
        f"**Total Pipelines:** {summary['total_pipelines']}  ",
        f"**Successful:** {summary['successful']}  ",
        f"**Failed:** {summary['failed']}  ",
        "",
        "## Quota Check",
        "",
        f"**Health:** {quota_health.upper()}  ",
        f"**Remaining:** {quota_remaining}  ",
        f"**Status:** {'⛔ DENIED' if quota_denied else '✅ APPROVED'}  ",
        "",
    ]
    
    if quota_denied:
        lines.append("> ⛔ **Remaining pipelines skipped due to insufficient quota**")
        lines.append("")
    
    lines.extend([
        "## Pipeline Results",
        "",
        "| Pipeline | Status | Processed | Emails | Verified |",
        "|----------|--------|-----------|--------|----------|",
    ])
    
    for name, info in summary["pipelines"].items():
        status = info.get("status", "unknown")
        if status == "failed":
            lines.append(f"| {name} | ❌ Failed | - | - | - |")
        elif status == "skipped":
            lines.append(f"| {name} | ⏭️ Skipped | - | - | - |")
        else:
            lines.append(f"| {name} | ✅ {status} | {info.get('total_processed', 0)} | {info.get('total_emails', 0)} | {info.get('verified', 0)} |")
    
    lines.append("")
    lines.append("## Next Run")
    lines.append(f"- **Scheduled:** Tomorrow at 1:00 PM PKT")
    lines.append(f"- **Timezone:** Pakistan Standard Time (UTC+5)")
    
    return "\n".join(lines)


async def main():
    """Main entry point."""
    try:
        await check_quota_and_proceed()
    except KeyboardInterrupt:
        print("\n⚠️  Orchestration interrupted by user")
    except Exception as e:
        print(f"\n💥 Orchestration failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())