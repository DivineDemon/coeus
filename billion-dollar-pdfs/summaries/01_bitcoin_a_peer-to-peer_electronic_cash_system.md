# 1. Bitcoin: A Peer-to-Peer Electronic Cash System

## Metadata
- **Position**: 1
- **Billion Dollar PDF URL**: https://billiondollarpdf.com/entry/bitcoin-whitepaper/
- **Original Document**: https://bitcoin.org/bitcoin.pdf
- **Category**: strict receipt
- **Thesis**: See Billion Dollar PDF entry for thesis

## Summary

Satoshi Nakamoto's 2008 whitepaper introduced Bitcoin, a decentralized electronic cash system that solves the double-spending problem without trusted intermediaries. The core innovation is a peer-to-peer distributed timestamp server using proof-of-work to create an immutable chain of transactions. Nodes vote with CPU power, the longest chain wins, and honest nodes controlling majority hashpower secure the network. The paper defines the transaction structure (digital signatures chaining ownership), the proof-of-work mechanism (Hashcash-style SHA256 with adjustable difficulty), network protocol, incentive model (block rewards + fees), disk space reclamation via Merkle trees, and simplified payment verification (SPV).

## Key Takeaways
- Trustless consensus via proof-of-work replaces centralized intermediaries
- Digital signatures + public ledger = ownership without identity
- Difficulty adjustment maintains ~10 min block time despite hardware improvements
- Economic incentives align honest behavior (mining rewards > attack profits)
- SPV enables lightweight clients without full node verification

## Capital Impact
Created the $1T+ cryptocurrency asset class, spawned thousands of blockchain projects, and catalyzed a new paradigm of decentralized finance. Bitcoin's market cap alone has exceeded $1T, with the broader crypto ecosystem reaching $3T+ at peak.

## Related Mental Models
Byzantine fault tolerance, digital scarcity, sound money, censorship resistance, Nakamoto consensus

## Source
[billiondollarpdf.com entry](https://billiondollarpdf.com/entry/bitcoin-whitepaper/) | [Original Document](https://bitcoin.org/bitcoin.pdf)
