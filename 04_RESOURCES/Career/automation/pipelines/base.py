"""
Base pipeline class for all Haga lead generation pipelines.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional
import json
import os
from pathlib import Path


@dataclass
class PipelineResult:
    """Result of a pipeline execution."""
    pipeline_name: str
    pipeline_type: str
    timestamp: str
    status: str  # "success", "partial", "failed"
    total_processed: int = 0
    with_emails: int = 0
    verified: int = 0
    inferred: int = 0
    total_emails: int = 0
    companies: List[Dict[str, Any]] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    error: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "pipeline_name": self.pipeline_name,
            "pipeline_type": self.pipeline_type,
            "timestamp": self.timestamp,
            "status": self.status,
            "total_processed": self.total_processed,
            "with_emails": self.with_emails,
            "verified": self.verified,
            "inferred": self.inferred,
            "total_emails": self.total_emails,
            "companies": self.companies,
            "metadata": self.metadata,
            "error": self.error,
        }

    def to_markdown(self) -> str:
        """Generate markdown report like the existing logs."""
        lines = [
            f"# Pipeline: {self.pipeline_name}",
            "",
            f"**Timestamp:** {self.timestamp}  ",
            f"**Pipeline:** {self.pipeline_type}  ",
            f"**Toolchain:** httpx  ",
            f"**Total Companies:** {self.total_processed}",
            "",
            "## Summary",
            "",
            "| Metric | Count |",
            "|--------|-------|",
            f"| Total Processed | {self.total_processed} |",
            f"| With Emails | {self.with_emails} |",
            f"| Verified | {self.verified} |",
            f"| Inferred | {self.inferred} |",
            f"| Total Emails | {self.total_emails} |",
            "",
            "## Companies with Contact Info",
            "",
        ]

        for company in self.companies:
            lines.append(f"### [{company.get('tier', 'Unknown')}] {company.get('name', 'Unknown')}")
            lines.append("")
            lines.append(f"- **Homepage:** {company.get('homepage', 'N/A')}")
            lines.append(f"- **Score:** {company.get('score', 'N/A')}")
            lines.append(f"- **Tier:** {company.get('tier', 'N/A')}")
            
            emails = company.get('emails', [])
            if emails:
                lines.append(f"- **Emails ({len(emails)}):**")
                for email in emails:
                    lines.append(f"  - {email}")
            else:
                lines.append("- **Emails (0):**")
            
            team = company.get('team_members', [])
            if team:
                lines.append(f"- **Team Members ({len(team)}):**")
                for member in team[:5]:  # Limit to 5
                    lines.append(f"  - {member}")
                if len(team) > 5:
                    lines.append(f"  - ... and {len(team) - 5} more")
            
            linkedin = company.get('linkedin_profiles', [])
            if linkedin:
                lines.append(f"- **LinkedIn Profiles ({len(linkedin)}):**")
                for profile in linkedin[:3]:
                    lines.append(f"  - {profile}")
                if len(linkedin) > 3:
                    lines.append(f"  - ... and {len(linkedin) - 3} more")
            
            signals = company.get('signals', [])
            if signals:
                lines.append(f"- **Signals:** {', '.join(signals)}")
            
            lines.append("")

        if self.error:
            lines.append(f"**ERROR:** {self.error}")
            lines.append("")

        lines.append(f"✅ **{self.pipeline_name.upper()} COMPLETE:** {self.total_processed} companies analyzed")
        return "\n".join(lines)


class BasePipeline(ABC):
    """Abstract base class for all pipelines."""

    def __init__(self, name: str, pipeline_type: str):
        self.name = name
        self.pipeline_type = pipeline_type
        self.timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    @abstractmethod
    async def run(self) -> PipelineResult:
        """Execute the pipeline and return results."""
        pass

    def save_result(self, result: PipelineResult, output_dir: Optional[str] = None) -> str:
        """Save pipeline result to markdown file."""
        if output_dir is None:
            output_dir = os.path.join(
                os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))),
                "logs",
                f"pipeline-{self.pipeline_type.replace('_', '-')}-{self.timestamp.split('_')[0]}"
            )
        
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        
        filename = f"{self.timestamp}_{self.pipeline_type}.md"
        filepath = Path(output_dir) / filename
        
        with open(filepath, "w") as f:
            f.write(result.to_markdown())
        
        return str(filepath)

    def save_json(self, result: PipelineResult, output_dir: Optional[str] = None) -> str:
        """Save pipeline result as JSON for programmatic access."""
        if output_dir is None:
            output_dir = os.path.join(
                os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))),
                "logs",
                f"pipeline-{self.pipeline_type.replace('_', '-')}-{self.timestamp.split('_')[0]}"
            )
        
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        
        filename = f"{self.timestamp}_{self.pipeline_type}.json"
        filepath = Path(output_dir) / filename
        
        with open(filepath, "w") as f:
            json.dump(result.to_dict(), f, indent=2)
        
        return str(filepath)