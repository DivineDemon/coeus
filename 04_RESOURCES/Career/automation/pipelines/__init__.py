"""
Pipeline automation package for Haga lead generation.
6 pipelines running concurrently at 1PM PKT daily.
"""

from .base import BasePipeline, PipelineResult
from .pipeline_a_design_partner import DesignPartnerDiscoveryPipeline
from .pipeline_b_investor_lead import InvestorLeadGenerationPipeline
from .pipeline_c_lead_enrichment import LeadEnrichmentPipeline
from .pipeline_d_competitor_discovery import CompetitorDiscoveryPipeline
from .pipeline_e_competitor_forensics import CompetitorForensicsPipeline
from .pipeline_f_quota_check import QuotaCheckPipeline

__all__ = [
    "BasePipeline",
    "PipelineResult",
    "DesignPartnerDiscoveryPipeline",
    "InvestorLeadGenerationPipeline",
    "LeadEnrichmentPipeline",
    "CompetitorDiscoveryPipeline",
    "CompetitorForensicsPipeline",
    "QuotaCheckPipeline",
]