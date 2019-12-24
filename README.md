# LSQ-Net: Learned Step Size Quantization

## Introduction

This is an unofficial implementation of LSQ-Net, a deep neural network quantization framework.
LSQ-Net is proposed by Steven K. Esser and et al. from IBM. It can be found on [arXiv:1902.08153](https://arxiv.org/abs/1902.08153).

|Model|Quantization|Top-1 @ Original|Top-1 @ This work|Top-5 @ Original|Top-5 @ This work|
|:----------:|:------:|:----:|:----:|:----:|:----:|
| ResNet-18  | w3, a3 | 70.2 | 68.9 | 89.4 | 88.5 |

There are some little differences between my implementation and the original paper, which will be described in detail below.

If this repository is helpful to you, please star it.

## User Guide

This program use YAML files as inputs. A template as well as the default configuration is providen as `config.yaml`.

If you want to change the behaviour of this program, please copy it somewhere else. And then run the `main.py` with your modified configuration file.

```
python main.py /path/to/your/config/file.yaml
```

The modified options in your YAML file will overwrite the default settings. For details, please read the comments in `config.yaml`.

After every epoch, the program will automatically store the best model parameters as a checkpoint. You can use the argument `--resume /path/to/checkpoint.pth.tar` to resume the training process, or evaluate the accuracy of the quantized model.

## Implementation Differences From the Original Paper

LSQ-Net paper has two versions, [v1](https://arxiv.org/pdf/1902.08153v2.pdf) and [v2](https://arxiv.org/pdf/1902.08153v1.pdf).
To improve accuracy, the authors expanded the quantization space in the v2 version.

My implementation generally follows the v2 version, except for the following points.

### Optimizers and Hyper-parameters

In the original paper, the network parameters are updated by a SGD optimizer with a momentum of 0.9, a weight decay of 10^-5 ~ 10^-4 and a initial learning rate of 0.01.
A cosine learning rate decay without restarts is also performed to adjust the learning rate during training.

I use an AdaM optimizer instead of the original SGD. The initial learning rate is set to 10^-3, and the other hyper-parameters of the optimizer are left at the default values.

### Initial Values of the Quantization Step Size

The authors use 2<|v|>/sqrt(Qp) as initial values of the step sizes in both weight and activation quantization layers, where Qp is the upper bound of the quantization space, and v is the initial weight values or the first batch of activations.

In my implementation, the step sizes in weight quantization layers are initialized as `Tensor(v.abs().mean()/Qp)`. In activation quantization layers, the step sizes are initialized as `Tensor(1.0)`.

### Supported Models

Currently, only ResNet-18/34/50/101 is supported, because I do not have enough GPUs to evaluate my code on other networks. Nevertheless, it is easy to add another new architecture beside ResNet.

All you need is a `Quantize` class in `quan/lsq.py`. With it, you can easily insert activation/weight quantization layers before matrix multiplication in your networks.

## Contributing Guide

I am not a professional algorithm researcher, and the current accuracy is enough for me. And I only have very limited GPU resources. Thus, I may not spend too much time continuing to optimize its results.

However, if you find any bugs in my code or have any ideas to improve the quantization results, please feel free to open an issue. I will be glad to join the discussion.
