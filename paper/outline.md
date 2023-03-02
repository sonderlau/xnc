## 智慧农村

1. 农业现代化：农业是国家的重要产业，也是人民的重要生活来源。通过智慧农村管理技术，可以提高农业生产效率，提升农业现代化水平。
2. 环保和资源保护：农业是重要的资源消耗和环境污染行业，智慧农村管理技术可以通过智能化的管理方式，减少农业对环境的影响，保护资源。
3. 数据驱动：智慧农村管理技术可以通过数据驱动的方式，提高农业管理的效率和准确性。
4. 技术创新：智慧农村管理技术的研究和实现是当前农业技术的创新方向，也是科技发展的重要内容。





## 解决的具体问题

清洁工

车/行人

**杂物堆**



为什么选这几个？旨在解决什么问题？能提供怎么样的价值？





> 传统方法写不写？
>
> 失败的案例
>
> 会不会显得跑题？
>
> 想标达出传统方法的局限性



## 目标识别 YOLOv5

### 模型

YOLOv5

D



### 高分辨率图片

SAHI

滑动窗口



### 数据集分析

TODO: Matplotlib 绘制

种类分部 大小

形状/数量

收集、标注成本



### 数据增强

Albumentations 库



#### YOLOv5 内置

Mosaic

Copy-Paste augmentation https://arxiv.org/abs/2012.07177

Image cutout augmentation https://arxiv.org/abs/1708.04552

MixUp augmentation https://arxiv.org/pdf/1710.09412.pdf



#### 自行实现的功能：

Blur

MedianBlur

ToGray

CLAHE

RandomBrightnessContrast

RandomGamma

ImageCompression

RadonWeather

> RandomRain
>
> RandomSnow
>
> RandomSunFlare
>
> RandomShadow
>
> RandomFog









### 训练与Validation

#### 多GPU

RTX 3090 * 3 : 11h



#### 验证与改进

F1 Curve

Confusion Matrix



负样本





### TensorRT 推理

TensorRT 的预期推理速度

#### 优势与限制

推理速度很快



需要手动编写对应的算子

#### NVIDIA 平台支持

边缘计算式设备的环境有一定的要求



### Hyperparameter Optimization 超参优化



#### Optuna



#### TPESampler

#### HyperbandPruner  rqdf



## 垃圾桶分类 ： ConvNeXt

垃圾桶分类



参数量并不高，推理时不会使用很多





输入的图片 resize

只考虑垃圾桶上半部分



开盖 闭盖 溢满





## 单目镜头物体大小估计



预估杂物堆或其他物体大小等



局限：

需要事先提供



## Jetson Nano 部署

### 设备简介

功耗、运算性能、可扩展性

| 项       | 参数                            |
| -------- | ------------------------------- |
| CPU      | Quad-Core ARM Cortex-A57 MPCore |
| GPU      | 128-Core NVIDIA Maxwell GPU     |
| AI 性能  | 473 GFLOPS                      |
| USB      | 4*USB 3.0                       |
| IO       | 40 Pin                          |
| 额定功率 | 5-10 W                          |



### 外置设备

#### 摄像头

Sony IMX219

焦距 3.15 mm

像素 800万

160‘ 视场角



#### 蜂鸣器

5V 无震源



