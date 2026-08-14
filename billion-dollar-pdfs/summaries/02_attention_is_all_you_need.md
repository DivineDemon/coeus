# 2. Attention Is All You Need

## Metadata
- **Position**: 2
- **Billion Dollar PDF URL**: https://billiondollarpdf.com/entry/attention-is-all-you-need/
- **Original Document**: https://arxiv.org/abs/1706.03762
- **Category**: strict receipt
- **Thesis**: See Billion Dollar PDF entry for thesis

## Summary

Vaswani et al. (Google, 2017) introduced the Transformer architecture, replacing recurrence and convolution entirely with attention mechanisms. The model uses multi-head self-attention to capture dependencies regardless of distance, enabling parallelization and superior sequence modeling. Key innovations: scaled dot-product attention, multi-head attention (parallel attention layers), positional encodings, encoder-decoder architecture with residual connections and layer normalization. Achieved SOTA on WMT 2014 English-to-German/French translation with significantly less training compute.

## Key Takeaways
- Self-attention captures global context in O(1) sequential operations vs O(n) for RNNs
- Multi-head attention learns different representation subspaces simultaneously
- Positional encodings inject sequence order without recurrence
- Parallelizable training enables massive scaling (GPT, BERT, etc.)
- Architecture is universal: works for translation, language modeling, vision, audio

## Capital Impact
Foundation of the entire modern LLM ecosystem. Enabled GPT-3/4, BERT, T5, PaLM, LLaMA, and all subsequent foundation models. Directly responsible for >$1T in AI market cap (NVIDIA, OpenAI, Anthropic, Google, Microsoft valuations). Triggered the current GPU/data center buildout.

## Related Mental Models
Sequence-to-sequence, attention mechanism, parallel compute scaling, foundation models, transfer learning

## Source
[billiondollarpdf.com entry](https://billiondollarpdf.com/entry/attention-is-all-you-need/) | [Original Document](https://arxiv.org/abs/1706.03762)
