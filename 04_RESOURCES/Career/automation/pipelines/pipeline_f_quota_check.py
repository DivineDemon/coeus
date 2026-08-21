"""
Pipeline F: Quota Check Job
Verifies Redis budget allocations and API quota status.
"""

import asyncio
import json
import os
from typing import Dict, Any, List
from datetime import datetime

from .base import BasePipeline, PipelineResult


class QuotaCheckPipeline(BasePipeline):
    """Pipeline F: Quota Check - verifies daily API budgets and quota status."""

    # Budget pools from the quota reset log
    BUDGET_POOLS = {
        "openrouter_remaining_today": {"allocated": 1000, "description": "OpenRouter API calls"},
        "extraction_pool": {"allocated": 500, "description": "Content extraction operations"},
        "forensics_pool": {"allocated": 250, "description": "Competitor forensics operations"},
        "scoring_pool": {"allocated": 100, "description": "Lead scoring operations"},
        "drafting_pool": {"allocated": 100, "description": "Email drafting operations"},
        "buffer_pool": {"allocated": 50, "description": "Buffer for unexpected usage"},
    }

    def __init__(self):
        super().__init__("Pipeline F: Quota Check", "quota_check")
        self.redis_url = os.environ.get("REDIS_URL", "redis://localhost:6379/0")
        self.redis_client = None

    async def _get_redis(self):
        """Get Redis connection."""
        if self.redis_client is None:
            try:
                import redis.asyncio as redis
                self.redis_client = redis.from_url(self.redis_url, decode_responses=True)
                await self.redis_client.ping()
            except Exception as e:
                print(f"  ⚠️  Redis connection failed: {e}")
                self.redis_client = None
        return self.redis_client

    async def check_redis_budgets(self) -> Dict[str, Any]:
        """Check current budget status from Redis."""
        redis = await self._get_redis()
        if not redis:
            return self._get_mock_budgets()
        
        budgets = {}
        try:
            for pool_name, pool_info in self.BUDGET_POOLS.items():
                key = f"redis:budget:{pool_name}"
                remaining = await redis.get(key)
                if remaining is not None:
                    budgets[pool_name] = {
                        "allocated": pool_info["allocated"],
                        "remaining": int(remaining),
                        "used": pool_info["allocated"] - int(remaining),
                        "description": pool_info["description"]
                    }
                else:
                    budgets[pool_name] = {
                        "allocated": pool_info["allocated"],
                        "remaining": pool_info["allocated"],
                        "used": 0,
                        "description": pool_info["description"]
                    }
            
            last_reset = await redis.get("redis:budget:last_reset")
            if last_reset:
                budgets["last_reset"] = last_reset
                
        except Exception as e:
            print(f"  ⚠️  Redis read error: {e}")
            return self._get_mock_budgets()
        
        return budgets

    def _get_mock_budgets(self) -> Dict[str, Any]:
        """Return mock budget data when Redis unavailable."""
        budgets = {}
        for pool_name, pool_info in self.BUDGET_POOLS.items():
            budgets[pool_name] = {
                "allocated": pool_info["allocated"],
                "remaining": pool_info["allocated"],
                "used": 0,
                "description": pool_info["description"]
            }
        budgets["last_reset"] = datetime.now().isoformat() + " (mock)"
        return budgets

    async def check_openrouter_quota(self) -> Dict[str, Any]:
        """Check OpenRouter quota via API if possible."""
        # This would require OpenRouter API key
        # For now return mock data
        return {
            "provider": "OpenRouter",
            "model": "nvidia/nemotron-3-ultra-550b-a55b:free",
            "quota_remaining": "Unknown (requires API key)",
            "status": "needs_api_key"
        }

    async def check_scraping_quota(self) -> Dict[str, Any]:
        """Check scraping service quotas."""
        # Could check Scrapling, Hunter.io, etc. if configured
        return {
            "scrapling": "local (no quota)",
            "hunter_io": "not_configured",
            "apify": "not_configured"
        }

    def assess_budget_health(self, budgets: Dict) -> Dict[str, Any]:
        """Assess overall budget health."""
        total_allocated = sum(p["allocated"] for p in budgets.values() if isinstance(p, dict) and "allocated" in p)
        total_used = sum(p["used"] for p in budgets.values() if isinstance(p, dict) and "used" in p)
        total_remaining = sum(p["remaining"] for p in budgets.values() if isinstance(p, dict) and "remaining" in p)
        
        health = "healthy"
        warnings = []
        
        if total_used / total_allocated > 0.8:
            health = "warning"
            warnings.append(f"High usage: {total_used}/{total_allocated} ({total_used/total_allocated*100:.1f}%)")
        elif total_used / total_allocated > 0.95:
            health = "critical"
            warnings.append(f"Critical usage: {total_used}/{total_allocated} ({total_used/total_allocated*100:.1f}%)")
        
        for pool_name, pool_info in budgets.items():
            if isinstance(pool_info, dict) and "allocated" in pool_info and pool_info["allocated"] > 0:
                usage_pct = pool_info["used"] / pool_info["allocated"]
                if usage_pct > 0.9:
                    health = "critical"
                    warnings.append(f"{pool_name}: {usage_pct*100:.1f}% used")
                elif usage_pct > 0.7:
                    if health != "critical":
                        health = "warning"
                    warnings.append(f"{pool_name}: {usage_pct*100:.1f}% used")
        
        return {
            "health": health,
            "total_allocated": total_allocated,
            "total_used": total_used,
            "total_remaining": total_remaining,
            "usage_percentage": round(total_used / total_allocated * 100, 1) if total_allocated > 0 else 0,
            "warnings": warnings
        }

    async def run(self) -> PipelineResult:
        print(f"\n🚀 Starting {self.name}...")
        
        # Check all quota sources
        budgets = await self.check_redis_budgets()
        openrouter = await self.check_openrouter_quota()
        scraping = await self.check_scraping_quota()
        health = self.assess_budget_health(budgets)
        
        # Create result
        result = PipelineResult(
            pipeline_name=self.name,
            pipeline_type=self.pipeline_type,
            timestamp=self.timestamp,
            status="success",
            total_processed=len(budgets),
            with_emails=0,
            verified=0,
            inferred=0,
            total_emails=0,
            companies=[],  # Not applicable for quota check
            metadata={
                "toolchain": "redis+httpx",
                "method": "budget_verification",
                "budgets": budgets,
                "openrouter": openrouter,
                "scraping_services": scraping,
                "health_assessment": health
            }
        )
        
        # Save outputs
        md_path = self.save_result(result)
        json_path = self.save_json(result)
        print(f"  ✅ Saved: {md_path}")
        print(f"  ✅ Saved: {json_path}")
        
        # Print summary
        print(f"\n  📊 Budget Health: {health['health'].upper()}")
        print(f"  📊 Total Allocated: {health['total_allocated']}")
        print(f"  📊 Total Used: {health['total_used']} ({health['usage_percentage']}%)")
        if health["warnings"]:
            for w in health["warnings"]:
                print(f"  ⚠️  {w}")
        
        return result

    def to_markdown(self) -> str:
        """Override to generate quota-specific markdown."""
        budgets: Dict[str, Any] = getattr(self, 'metadata', {}).get("budgets", {}) if hasattr(self, 'metadata') else {}
        health: Dict[str, Any] = getattr(self, 'metadata', {}).get("health_assessment", {}) if hasattr(self, 'metadata') else {}
        openrouter: Dict[str, Any] = getattr(self, 'metadata', {}).get("openrouter", {}) if hasattr(self, 'metadata') else {}
        scraping: Dict[str, Any] = getattr(self, 'metadata', {}).get("scraping_services", {}) if hasattr(self, 'metadata') else {}
        
        lines = [
            f"# {self.name}",
            "",
            f"**Timestamp:** {self.timestamp}  ",
            f"**Pipeline:** {self.pipeline_type}  ",
            f"**Toolchain:** redis + httpx  ",
            "",
            "## Budget Health Assessment",
            "",
            f"**Overall Health:** {health.get('health', 'unknown').upper()}",
            f"**Total Allocated:** {health.get('total_allocated', 0)}",
            f"**Total Used:** {health.get('total_used', 0)} ({health.get('usage_percentage', 0)}%)",
            f"**Total Remaining:** {health.get('total_remaining', 0)}",
            "",
        ]
        
        if health.get("warnings"):
            lines.append("### Warnings")
            for w in health["warnings"]:
                lines.append(f"- ⚠️ {w}")
            lines.append("")
        
        lines.append("## Budget Pools")
        lines.append("")
        lines.append("| Pool | Allocated | Remaining | Used | Description |")
        lines.append("|------|-----------|-----------|------|-------------|")
        
        for pool_name, pool_info in budgets.items():
            if pool_name == "last_reset":
                continue
            if isinstance(pool_info, dict):
                lines.append(f"| {pool_name} | {pool_info.get('allocated', 0)} | {pool_info.get('remaining', 0)} | {pool_info.get('used', 0)} | {pool_info.get('description', '')} |")
        
        if "last_reset" in budgets:
            lines.append(f"\n**Last Reset:** {budgets['last_reset']}")
        
        lines.append("")
        lines.append("## OpenRouter Quota")
        lines.append("")
        lines.append(f"- **Provider:** {openrouter.get('provider', 'N/A')}")
        lines.append(f"- **Model:** {openrouter.get('model', 'N/A')}")
        lines.append(f"- **Quota Remaining:** {openrouter.get('quota_remaining', 'N/A')}")
        lines.append(f"- **Status:** {openrouter.get('status', 'N/A')}")
        
        lines.append("")
        lines.append("## Scraping Services")
        lines.append("")
        for service, status in scraping.items():
            lines.append(f"- **{service}:** {status}")
        
        lines.append("")
        lines.append(f"✅ **QUOTA CHECK COMPLETE:** Health = {health.get('health', 'unknown')}")
        
        return "\n".join(lines)

    async def close(self):
        if self.redis_client:
            await self.redis_client.close()