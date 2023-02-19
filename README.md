# XNC



## 介绍

边缘计算 为什么用 特点：太阳能电池板 性能 部署



本项目应用YOLOv5、ConvNeXt等人工智能深度学习和边缘计算等技术对农村环境综合治理，对垃圾桶状态、粮食杂物堆占道、水库附近可疑人物等进行记录并实时警报。同时记录事件发生的时间地点等，实现大数据可视化展示，即时信息反馈。此外，项目还集成对环卫工人及水库管理人员的管理、考勤等功能。通过消融实验使模型有高性能同时具备边缘计算设备的低功耗、低成本、易部署、高扩展等特点，改善环境问题的处理流程并促进农村环境的美化与整洁。

## 设备

Jetson Nano 4GB

- 性能：472 GFLOPS

预计: FPS 23



## 选取的模型

Yolov5-Lite

- 15.6 GFLOPS





ConvNeXt-Tiny

- 4.5 GFLOPS





## 多GPU 训练



```bash
python -m torch.distributed.run --nproc_per_node 2 train.py --batch 60 --data cleaner.yaml --img 1280 --epochs 350 --weights yolov5s6.pt --device 0,1 --hyp hyp.custom.yaml 
```



| Image Size | Batch | GPUs | Memory Allocated |
| ---------- | ----- | ---- | ---------------- |
| 1280       | 50    | 2    | 18/24  20/24     |
| 1280       | 60    | 2    | 23/24  23/24     |
| 1280       | 60    | 3    |                  |
| 640        | 64    | 2    |                  |

```bash
python train.py --epochs 10 --data cleaner.yaml --weights v22-1280-midterm.pt --cache  --evolve 400
```

