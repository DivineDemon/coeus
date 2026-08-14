# 12. ImageNet Classification with Deep Convolutional Neural Networks (AlexNet)

## Metadata
- **Position**: 12
- **Billion Dollar PDF URL**: https://billiondollarpdf.com/entry/alexnet/
- **Original Document**: https://papers.nips.cc/paper/2012/hash/c399862d3b9d6b76c8436e924a68c45b-Abstract.html
- **Category**: strict receipt
- **Thesis**: Deep CNNs trained on GPUs shatter the ImageNet benchmark, igniting the modern deep-learning era.

## Summary

Krizhevsky, Sutskever, Hinton (2012) trained a deep CNN on 1.3M ImageNet images (1000 classes) using GPUs. Achieved 39.7% top-1 / 18.9% top-5 error vs 26% previous SOTA. Architecture: 5 conv layers (some with max-pooling), 2 FC layers, 60M parameters, ReLU activations, dropout regularization, data augmentation. GPU implementation (2 GTX 580s) made training feasible in ~1 week.

## Key Takeaways
- Deep CNNs + GPUs + large labeled data = breakthrough performance
- ReLU avoids vanishing gradients vs sigmoid/tanh
- Dropout prevents overfitting in large FC layers
- Data augmentation (crops, flips) effectively multiplies dataset
- Visualizable features: edges → textures → objects → concepts

## Capital Impact
Ignited deep learning revolution. Led directly to Google/DeepMind acquisition, GPU demand explosion (NVIDIA pivot to AI), ResNet, GANs, and all modern computer vision. NVIDIA market cap from $10B → $3T+.

## Related Mental Models
Deep learning, GPU computing, transfer learning, representation learning, scaling hypothesis

## Source
[billiondollarpdf.com entry](https://billiondollarpdf.com/entry/alexnet/) | [Original Document](https://papers.nips.cc/paper/2012/hash/c399862d3b9d6b76c8436e924a68c45b-Abstract.html)
