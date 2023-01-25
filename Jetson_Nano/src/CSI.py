from jetcam.csi_camera import CSICamera
from PIL import Image

camera = CSICamera(capture_device=0, width=224, height=224, capture_width=1280, capture_height=720, capture_fps=30)

image = camera.read()



image.swapaxes(2,0)

print(image.shape)

pil_image = Image.fromarray(image, mode="RGB")

pil_image.save('./test.jpg')