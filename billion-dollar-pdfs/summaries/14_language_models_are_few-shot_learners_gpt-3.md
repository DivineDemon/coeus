# 14. Language Models are Few-Shot Learners (GPT-3)

## Metadata
- **Position**: 14
- **Billion Dollar PDF URL**: https://billiondollarpdf.com/entry/gpt-3/
- **Original Document**: https://arxiv.org/abs/2005.14165
- **Category**: strict receipt
- **Thesis**: Scaling language models to 175B parameters yields emergent few-shot task performance without fine-tuning.

## Summary

Brown et al. (OpenAI, 2020) introduced GPT-3: 175B parameter autoregressive language model showing that scaling up enables few-shot learning without fine-tuning. GPT-3 performs translation, QA, cloze, reasoning, arithmetic, and word manipulation from just a few examples in context. Identified limitations: struggles with some reasoning tasks, methodological issues from web training data, generates human-like news articles. The paper demonstrated the scaling hypothesis empirically: bigger models + more data = emergent capabilities.

## Key Takeaways
- 175B params (10x prior) enables task-agnostic few-shot performance
- No gradient updates needed; tasks specified via text interaction
- Emergent capabilities: arithmetic, unscrambling, novel word usage
- Scaling laws predict performance; no fine-tuning datasets required
- Societal impacts: synthetic media, automation, alignment concerns

## Capital Impact
Catalyzed the LLM arms race. OpenAI valuation $80B+, Microsoft $13B investment, Anthropic $4B+, Google DeepMind consolidation. Spawned the 'foundation model' paradigm and $100B+ in training compute demand.

## Related Mental Models
Scaling laws, few-shot learning, in-context learning, emergence, foundation models

## Source
[billiondollarpdf.com entry](https://billiondollarpdf.com/entry/gpt-3/) | [Original Document](https://arxiv.org/abs/2005.14165)
