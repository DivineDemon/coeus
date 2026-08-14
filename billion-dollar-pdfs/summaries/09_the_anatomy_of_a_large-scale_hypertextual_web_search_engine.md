# 9. The Anatomy of a Large-Scale Hypertextual Web Search Engine

## Metadata
- **Position**: 9
- **Billion Dollar PDF URL**: https://billiondollarpdf.com/entry/anatomy-web-search/
- **Original Document**: https://snap.stanford.edu/class/cs224w-readings/Brin98Anatomy.pdf
- **Category**: strict receipt
- **Thesis**: See Billion Dollar PDF entry for thesis

## Summary

Brin & Page (1998) introduced Google and PageRank: ranking pages by link structure rather than keyword matching. PageRank models a 'random surfer' following links; pages with many high-quality inbound links rank higher. System architecture: distributed crawlers, compressed repository, inverted index with compact encoding, anchor text propagation, PageRank computation via eigenvector. Scaled to 24M pages in <1 week; designed for 100M+.

## Key Takeaways
- Link structure = collective intelligence; citations = quality votes
- PageRank = principal eigenvector of normalized link matrix
- Anchor text provides better descriptions than page content
- Scalable systems design: Bigfiles, barrel sharding, compact hit encoding
- Quality > recall: precision at top-10 matters most for users

## Capital Impact
Created Google (~$2T market cap), defined search advertising ($200B+/year), organized world's information, enabled entire SEO/SEM industry, made 'to google' a verb.

## Related Mental Models
Citation analysis, eigenvector centrality, web-scale systems, information retrieval, link economy

## Source
[billiondollarpdf.com entry](https://billiondollarpdf.com/entry/anatomy-web-search/) | [Original Document](https://snap.stanford.edu/class/cs224w-readings/Brin98Anatomy.pdf)
