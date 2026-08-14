# 33. Scaling Laws for Neural Language Models

## Metadata
- **Position**: 33
- **Billion Dollar PDF URL**: https://billiondollarpdf.com/entry/scaling-laws/
- **Original Document**: https://arxiv.org/abs/2001.08361
- **Category**: strict receipt
- **Thesis**: Model performance scales predictably as a power law with compute, data, and parameters.

## Summary

Kaplan et al. (OpenAI, 2020): Model performance scales predictably as a power law with compute, data, and parameters. L(C) = aC^(-b) + c. No signs of saturation up to 10^3 petaflop-days. Optimal allocation: scale model and data equally. Predicted GPT-3 performance from smaller runs. Established the 'scaling hypothesis' as empirical law.

## Key Takeaways
- Power law scaling: loss �� compute^(-0.05) to compute^(-0.07)
- No saturation observed; more compute = better models
- Optimal: scale model size and dataset size proportionally
- Compute is the main driver; architecture matters less
- Predictable: can forecast large model performance from small runs

## Capital Impact
Justified GPT-3 (175B) and subsequent 100B+ models. Directed $100B+ in training compute. Hyperscalers (Microsoft, Google, Meta, AWS) build capex plans on these laws.

## Related Mental Models
Power laws, compute-optimal scaling, Chinchilla, scaling hypothesis, predictable AI progress

## Source
[billiondollarpdf.com entry](https://billiondollarpdf.com/entry/scaling-laws/) | [Original Document](https://arxiv.org/abs/2001.08361)
