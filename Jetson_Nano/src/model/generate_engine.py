import tensorrt as trt
import pycuda.driver as cuda
import pycuda.autoinit
import common
import os
def build_engine(onnx_file_path,engine_file_path):
    """Takes an ONNX file and creates a TensorRT engine to run inference with"""
    TRT_LOGGER = trt.ILogger(trt.Logger.WARNING)
    with trt.Builder(TRT_LOGGER) as builder, builder.create_network(common.EXPLICIT_BATCH) as network, trt.OnnxParser(network, TRT_LOGGER) as parser:
        builder.max_workspace_size = 1 << 28 # 256MiB
        builder.max_batch_size = 1
        # Parse model file
        if not os.path.exists(onnx_file_path):
            print('ONNX file {} not found, please run yolov3_to_onnx.py first to generate it.'.format(onnx_file_path))
            exit(0)
        print('Loading ONNX file from path {}...'.format(onnx_file_path))
        with open(onnx_file_path, 'rb') as model:
            print('Beginning ONNX file parsing')
            if not parser.parse(model.read()):
                print ('ERROR: Failed to parse the ONNX file.')
                for error in range(parser.num_errors):
                    print (parser.get_error(error))
                return None
        print('Completed parsing of ONNX file')
        print('Building an engine from file {}; this may take a while...'.format(onnx_file_path))
        engine = builder.build_cuda_engine(network)
        print("Completed creating Engine")
        with open(engine_file_path, "wb") as f:
            f.write(engine.serialize())
        return engine
if __name__ =="__main__":
    onnx_path1 = '/home/jetson/xnc/model/lite-c.onnx'
    engine_path = '/home/jetson/xnc/model/lite-c.engine'
    build_engine(onnx_path1,engine_path)