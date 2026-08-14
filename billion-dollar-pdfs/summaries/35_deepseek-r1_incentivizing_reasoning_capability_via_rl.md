# 35. DeepSeek-R1: Incentivizing Reasoning Capability via RL

## Metadata
- **Position**: 35
- **Billion Dollar PDF URL**: https://billiondollarpdf.com/entry/deepseek-r1/
- **Original Document**: https://arxiv.org/abs/2501.12948
- **Category**: strict receipt
- **Thesis**: Reinforcement learning can elicit strong reasoning in LLMs at a fraction of frontier training cost.

## Summary

DeepSeek (2025): RL can elicit strong reasoning in LLMs at fraction of frontier training cost. DeepSeek-R1 (671B MoE, 37B active) matches o1 on math/code reasoning using pure RL (no SFT). Two-stage: R1-Zero (RL only, emergent reasoning) → R1 (RL + cold-start SFT). Cost: ~$6M vs $100M+ for comparable models. Triggered ~$1T NVIDIA drawdown on cost-efficiency fears (Jan 2025).

## Key Takeaways
- Pure RL from base model → emergent reasoning (no SFT needed)
- Two-stage: R1-Zero (raw RL) → R1 (RL + cold-start data)
- MoE architecture: 671B total, 37B active per token
- ~$6M training cost vs $100M+ for o1-class models
- Open weights: released under MIT license

## Capital Impact
Shattered 'scaling requires $100M+' narrative. NVIDIA -17% in one day ($600B market cap loss). Accelerated open-source reasoning models (Qwen, Nemotron, Skywork). Forced frontier labs to defend moats.

## Related Mental Models
RL for reasoning, MoE efficiency, open weights, cost disruption, reasoning emergence

## Source
[billiondollarpdf.com entry](https://billiondollarpdf.com/entry/deepseek-r1/) | [Original Document](https://arxiv.org/abs/2501.12948)
