# 34. Training Compute-Optimal Large Language Models (Chinchilla)

## Metadata
- **Position**: 34
- **Billion Dollar PDF URL**: https://billiondollarpdf.com/entry/chinchilla/
- **Original Document**: https://arxiv.org/abs/2203.15556
- **Category**: strict receipt
- **Thesis**: For a fixed compute budget, models should be smaller and trained on far more data than prior practice.

## Summary

Hoffmann et al. (DeepMind, 2022): For fixed compute budget, models should be SMALLER and trained on MORE data than prior practice. Chinchilla (70B params, 1.4T tokens) outperformed Gopher (280B, 300B tokens) with 4x less compute. Optimal: ~20 tokens per parameter. Previous models undertrained (GPT-3: ~0.5 tokens/param). Data is the new bottleneck.

## Key Takeaways
- Optimal scaling: N �� C^0.5, D �� C^0.5 (not N �� C^0.73 as Kaplan suggested)
- 20 tokens/parameter is compute-optimal
- Undertraining wastes compute; overtraining wastes data
- Data quality > quantity; curation matters
- Chinchilla 70B = Gopher 280B with 4x less compute

## Capital Impact
Redirected $100B+ from model scaling to data scaling. LLaMA (65B, 1.4T tokens), PaLM-2, GPT-4 all follow Chinchilla scaling. Data curation became primary research focus.

## Related Mental Models
Compute-optimal scaling, tokens/parameter, data quality, LLaMA, undertraining

## Source
[billiondollarpdf.com entry](https://billiondollarpdf.com/entry/chinchilla/) | [Original Document](https://arxiv.org/abs/2203.15556)
