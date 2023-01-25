扩容

/usr/lib/nvidia/resizefs/nvresizefs.sh



[05/25/2022-14:48:53] [I] === Trace details ===
[05/25/2022-14:48:53] [I] Trace averages of 10 runs:
[05/25/2022-14:48:53] [I] Average on 10 runs - GPU latency: 66.9466 ms - Host latency: 67.534 ms (end to end 67.5465 ms, enqueue 10.1917 ms)
[05/25/2022-14:48:53] [I] Average on 10 runs - GPU latency: 66.9211 ms - Host latency: 67.5046 ms (end to end 67.5172 ms, enqueue 10.1417 ms)
[05/25/2022-14:48:53] [I] Average on 10 runs - GPU latency: 66.9767 ms - Host latency: 67.5633 ms (end to end 67.5757 ms, enqueue 10.4922 ms)
[05/25/2022-14:48:53] [I] Average on 10 runs - GPU latency: 66.9613 ms - Host latency: 67.5461 ms (end to end 67.5585 ms, enqueue 10.5588 ms)
[05/25/2022-14:48:53] [I] 
[05/25/2022-14:48:53] [I] === Performance summary ===
[05/25/2022-14:48:53] [I] Throughput: 14.803 qps
[05/25/2022-14:48:53] [I] Latency: min = 67.2566 ms, max = 67.9812 ms, mean = 67.5408 ms, median = 67.4934 ms, percentile(99%) = 67.9812 ms
[05/25/2022-14:48:53] [I] End-to-End Host Latency: min = 67.2664 ms, max = 67.9937 ms, mean = 67.5531 ms, median = 67.5059 ms, percentile(99%) = 67.9937 ms
[05/25/2022-14:48:53] [I] Enqueue Time: min = 9.27643 ms, max = 14.1978 ms, mean = 10.3433 ms, median = 9.81689 ms, percentile(99%) = 14.1978 ms
[05/25/2022-14:48:53] [I] H2D Latency: min = 0.473389 ms, max = 0.507767 ms, mean = 0.479831 ms, median = 0.475342 ms, percentile(99%) = 0.507767 ms
[05/25/2022-14:48:53] [I] GPU Compute Time: min = 66.6689 ms, max = 67.3884 ms, mean = 66.9546 ms, median = 66.9139 ms, percentile(99%) = 67.3884 ms
[05/25/2022-14:48:53] [I] D2H Latency: min = 0.104736 ms, max = 0.110596 ms, mean = 0.106321 ms, median = 0.105957 ms, percentile(99%) = 0.110596 ms
[05/25/2022-14:48:53] [I] Total Host Walltime: 3.17502 s
[05/25/2022-14:48:53] [I] Total GPU Compute Time: 3.14687 s
[05/25/2022-14:48:53] [I] Explanations of the performance metrics are printed in the verbose logs.
[05/25/2022-14:48:53] [I] 
&&&& PASSED TensorRT.trtexec [TensorRT v8001] # trtexec --onnx=./lite-c.onnx --explicitBatch --saveEngine=output.engine --workspace=128 --fp16
[05/25/2022-14:48:53] [I] [TRT] [MemUsageChange] Init cuBLAS/cuBLASLt: CPU +0, GPU +0, now: CPU 904, GPU 3639 (MiB)