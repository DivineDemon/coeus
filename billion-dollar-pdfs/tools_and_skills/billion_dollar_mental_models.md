---
name: billion-dollar-mental-models
version: 1.0
description: Apply mental models from 89 billion-dollar PDFs to investment, startup, AI, macro, and personal decisions
category: decision-making
trigger: When making high-stakes decisions requiring mental models from proven capital movers
author: Hermes Agent (Mushood Hanif)
source: billiondollarpdf.com archive
---

# Billion Dollar Mental Models Skill

This skill loads the mental models toolkit derived from 89 documents that introduced new mental models and changed how billions of dollars of capital flowed.

## Quick Reference: Top 10 Mental Models by Category

### Investment Decision Making
1. **Expectations Investing** (Mauboussin) — Price = expectations; find the gap
2. **Magic Formula** (Greenblatt) — Mechanical: Earnings Yield + Return on Capital
3. **Cycle Positioning** (Marks) — Where are we? Second-level thinking; counter-cyclical
4. **Mean Reversion / Blood in Streets** (Grantham) — Buy quality at max fear
5. **Reflexivity** (Soros/Druckenmiller) — Trade narrative inflections; concentrated bets

### Startup & Company Building
6. **Zero to One / Monopoly** (Thiel) — Secrets → monopoly → expand concentrically
7. **Do Things That Don't Scale** (Graham) — Manual → automated; organic ideas
8. **Blitzscale vs Endure** (Hoffman/Sequoia) — Match strategy to market + capital regime
9. **Founder Mode** (Chesky/Musk/Huang) — Stay in details; avoid manager abstraction
10. **Audience-First / Small Bets** (Barry/Levels/Vassallo) — Teach → audience → products

### AI & Technology Strategy
11. **Scaling Laws / Chinchilla** (Kaplan/Hoffmann/Sutton) — Compute-optimal: 20 tokens/param
12. **Software 2.0** (Karpathy/Huang) — Learned > written; differentiable end-to-end
13. **AI Moats** (Chen/DeepSeek) — Data network effects > model access; cost disruption risk

### Macro & Geopolitical
14. **Big Debt Cycles** (Dalio) — 250yr empire / 50-75yr debt; diversify 15+ uncorrelated
15. **Fiscal Dominance** (Alden/Druckenmiller) — Debt/GDP > 120% → yield control → inflation
16. **Energy Reality** (Smil) — Transitions take decades; power density matters

### Personal Productivity & Wealth
17. **Munger Latticework** — Invert; incentives; base rates; 25 biases; avoid stupidity
18. **Antifragile** (Taleb) — Barbell 90/10; via negativa; skin in the game; Lindy; optionality
19. **Psychology of Money** (Housel) — Wealth invisible; saving rate > returns; room for error
20. **Compounding Self-Improvement** (Altman) — Career = compound interest; 10yr horizon

---

## Usage Patterns

### Pattern 1: Investment Decision
```
User: "Should I buy NVIDIA at $120?"
Agent: 
1. Load Expectations Investing tool → reverse DCF implied expectations
2. Load Cycle Positioning → where in semiconductor cycle?
3. Load Reflexivity → narrative check (AI boom/bust?)
4. Load Magic Formula → earnings yield + ROC rank
5. Synthesize: position size based on conviction + margin of safety
```

### Pattern 2: Startup Strategy
```
User: "We have $500K ARR, raising Series A. Blitzscale or endure?"
Agent:
1. Load Blitzscale vs Endure Selector → assess market (network effects?) + capital regime
2. Load Founder Mode → stay in product details during scale
3. Load Zero to One → is there a secret/monopoly or competitive market?
4. Synthesize: recommendation with specific actions
```

### Pattern 3: AI Architecture Decision
```
User: "Build vs buy for our LLM application?"
Agent:
1. Load Software 2.0 → differentiable pipeline vs explicit logic
2. Load AI Moat Evaluator → data network effects? closed-loop?
3. Load Scaling Laws → compute budget allocation
4. Load Cost Disruption (DeepSeek) → can RL replicate at 1/100th cost?
5. Synthesize: build/buy/partner decision
```

### Pattern 4: Macro Portfolio Construction
```
User: "How to position for next 5 years?"
Agent:
1. Load Dalio Big Cycle → US cycle stage; 15+ uncorrelated streams
2. Load Fiscal Dominance → debt trajectory → hard assets allocation
3. Load Reflexivity → narrative inflection points to trade
4. Load Energy Reality → physical constraints on green transition
5. Synthesize: asset allocation with specific % targets
```

### Pattern 5: Personal Life Decision
```
User: "Take high-paying job vs start business?"
Agent:
1. Load Munger Latticework → invert: how could each go wrong?
2. Load Antifragile → barbell: keep job (safe) + nights/weekends (speculative)
3. Load Psychology of Money → wealth = freedom; saving rate > returns
4. Load Compounding Self-Improvement → 10yr horizon; compound skills
5. Synthesize: decision framework with risk/reward
```

---

## Tool Invocation

The skill provides access to the toolkit at:
`/Users/mushood/Documents/code/personal/coeus/billion-dollar-pdfs/tools_and_skills/billion_dollar_toolkit.json`

Load it in your context and apply the relevant tools based on the decision category.

---

## Source Documents (89 Total)

The mental models are derived from these billion-dollar PDFs:
1. Bitcoin Whitepaper (Nakamoto) — Trustless consensus
2. Attention Is All You Need (Vaswani et al.) — Transformer architecture
3. Situational Awareness (Aschenbrenner) — AGI by 2027
4. Black-Scholes (Black/Scholes/Merton) — No-arbitrage pricing
5. Software Eating World (Andreessen) — Software-mediated disruption
6. Tesla Master Plan (Musk) — Top-down market entry
7. Ethereum Whitepaper (Buterin) — Programmable blockchain
8. Internet Tidal Wave (Gates) — Platform inflection
9. PageRank (Brin/Page) — Link structure = quality
10. RIP Good Times (Sequoia) — Structural reset; survive
11. Superinvestors (Buffett) — Value investing refutes EMH
12. AlexNet (Krizhevsky et al.) — Deep learning on GPU
13. Bitter Lesson (Sutton) — Compute > human knowledge
14. GPT-3 (Brown et al.) — Few-shot scaling
15. WWW Proposal (Berners-Lee) — Decentralized hypertext
16. Scion Capital / Big Short (Burry) — Forensic credit
17. Zero to One (Thiel) — Monopoly via secrets
18. Adapting to Endure (Sequoia) — Profitability > growth
19. Do Things That Don't Scale (Graham) — Manual → automated
20. How to Get Startup Ideas (Graham) — Organic ideation
21. Competition Is for Losers (Thiel) — Monopoly profits
22. Aggregation Theory (Thompson) — Integrate forward to users
23. Marketplace Framework (Gurley) — 10-factor scorecard
24. 1,000 True Fans (Kelly) — Direct creator economy
25. Blitzscaling (Hoffman) — Speed over efficiency
26. Toy to Platform (Dixon) — Disruption starts as toy
27. Decentralization Matters (Dixon) — Crypto alignment
28. Invisible Asymptotes (Wei) — Growth ceilings
29. What Happened to Future (Founders Fund) — Hard tech
30. New Moats (Chen) — Data network effects
31. SaaS Metrics 2.0 (Skok) — Unit economics bible
32. Uniswap AMM (Adams) — Constant product
33. Scaling Laws (Kaplan) — Power law predictability
34. Chinchilla (Hoffmann) — Compute-optimal scaling
35. DeepSeek-R1 — RL reasoning at 1/100th cost
36. Software 2.0 (Karpathy) — Learned differentiable programs
37. Moore's Law for Everything (Altman) — AI economics
38. AI Will Save World (Andreessen) — Techno-optimism
39. Machines of Loving Grace (Amodei) — AI for science
40. Sea Change (Marks) — Regime shift
41. Race to Bottom (Marks) — Yield chasing
42. Bretton Woods III (Pozsar) — Commodity money
43. Changing World Order (Dalio) — Big cycles
44. Waiting for Last Dance — TBD
45. Buy American — TBD
46. Fraying USD Reserve — TBD
47. Herbalife Short (Ackman) — Activist short
48. Lehman Short (Sohn) — Crisis alpha
49. Enron Short — Fraud detection
50. Sino-Forest Short (Muddy Waters) — Forensic
51. Nikola Short (Hindenburg) — SPAC fraud
52. Adani Short (Hindenburg) — Conglomerate fraud
53. Valeant Short — Pharma fraud
54. Internet Trends (Meeker) — Sector shifts
55. AI Trends — Paradigm shifts
56. Mobile Eating World — Platform shift
57. Big Ideas (ARK) — Convergence
58. Airbnb Pitch Deck — Marketplace wedge
59. Uber Pitch Deck — Network effects
60. YouTube Memo — UGC platform
61. Sovereign Individual — Digital sovereignty
62. Techno-Optimist Manifesto — Abundance
63. Most Important Century — AI pivotal
64. Moloch — Coordination traps
65. What We Owe Future — Longtermism
66. AGI Ruin — Alignment lethality
67. Progress Studies — Accelerate progress
68. Scaling Hypothesis (Gwern) — Scaling continues
69. Fat Protocols (Burniske) — Protocol value capture
70. Bullish Bitcoin — Monetization path
71. Solo Capitalists — GP disruption
72. SPAC Investor Letters — IPO 2.0
73. Lean Startup / MVP — Build-measure-learn
74. Big Debt Crises (Dalio) — Mechanical template
75. Reinvesting When Terrified (Grantham) — Buy fear
76. Allied Capital Short (Einhorn) — Accounting fraud
77. Luckin Coffee (Muddy Waters) — Fabricated revenue
78. Facebook Pitch — Social network wedge
79. OpenCloud Report — Infrastructure shift
80. ResNet — Residual connections
81. word2vec — Vector embeddings
82. Solana — Proof of History
83. Superintelligence (Bostrom) — Existential risk
84. Increasing Returns (Arthur) — Winner-take-all
85. Information Theory (Shannon) — Bits, capacity, noise
86. Madoff Fraud — Impossible returns
87. Block Intelligence-Native — AI-first org
88. Fairchild Founding — Silicon Valley genesis
89. DEC/ARD Proposal — Venture capital birth

---

## Integration with Hermes

Add to your `~/.hermes/skills/` or reference in `cronjob` with:
```bash
cronjob create --name "billion-dollar-decision-support"   --skills "billion-dollar-mental-models"   --schedule "0 9 * * 1"   --prompt "Review portfolio/startup/life decisions using billion-dollar mental models toolkit"
```

---

## Maintenance

- Update when new documents added to billiondollarpdf.com
- Refine tool steps based on decision outcomes
- Track which models used for which decisions (audit trail)
- Quarterly review: are models still predictive?
