from PIL import Image
import torch
import torchvision.transforms as T
import cv2
import numpy as np

class SkinEnhancement:
    def __init__(self):
        self.model = torch.hub.load('pytorch/vision:v0.10.0', 'deeplabv3_resnet101', pretrained=True)
        self.model.eval()

    def segment_skin(self, image):
        preprocess = T.Compose([
            T.ToTensor(),
            T.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ])

        input_tensor = preprocess(image)
        input_batch = input_tensor.unsqueeze(0)

        with torch.no_grad():
            output = self.model(input_batch)['out'][0]
        output_predictions = output.argmax(0)

        skin_mask = (output_predictions == 15).byte().cpu().numpy()

        return skin_mask

    def dodge_and_burn(self, image, mask):
        image_np = np.array(image)

        for channel in range(3):
            image_np[:, :, channel] = cv2.GaussianBlur(image_np[:, :, channel], (0, 0), 3)
            image_np[:, :, channel] = np.uint8(image_np[:, :, channel] * (1 - mask) + image_np[:, :, channel] * mask * 1.5)

        return Image.fromarray(image_np)

    def process_image(self, image):
        skin_mask = self.segment_skin(image)
        enhanced_image = self.dodge_and_burn(image, skin_mask)
        return enhanced_image