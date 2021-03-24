import os
import cv2
import glob
import time
import darknet
import argparse
import numpy as np
import random

from Detector import Detector
from torch.utils.data import DataLoader


PATH = 'detectors/yolo4/'


class yolo4(Detector):

    def __init__(self, batch_size):

        super().__init__('yolo4', batch_size)

        CONFIG_FILE = PATH + 'cfg/yolov4.cfg'
        DATA_FILE   = PATH + 'cfg/coco.data'
        WEIGHTS     = PATH + 'yolov4.weights'

        # Load model (pretrained)
        network, class_names, class_colors = darknet.load_network(
            CONFIG_FILE,
            DATA_FILE,
            WEIGHTS,
            batch_size=self.batch_size
        )

        self.model = network
        self.class_names = class_names
        self.class_colors = class_colors


        self.thresh = 0.25
        self.label_permited = ['person']



    def eval_set(self, dataset, loader, device, verbose=0):
        '''Run evaluation over loaded data.
        '''

        dataloader = DataLoader(dataset, batch_size=self.batch_size, shuffle=False, num_workers=1)
        

        for i_batch, (images, y) in enumerate(dataloader):

            images = images.numpy()


            for i, image in enumerate(images):

                i_frame = (i_batch * self.batch_size) + i + 1


                # Detect objects
                detections = self.detect_image(image)

                # Preprocess output (detections)
                labels, scores, bboxes = yolo4.process_output(detections)

                loader.update(i_frame, bboxes, scores, labels, label_permited=self.label_permited, preprocess=False)


            break



    def detect_image(self, image):

        image = (image.transpose(1, 2, 0) * 255).astype(np.uint8)

        width = darknet.network_width(self.model)
        height = darknet.network_height(self.model)
        darknet_image = darknet.make_image(width, height, 3)

        image_resized = cv2.resize(image, (width, height), interpolation=cv2.INTER_LINEAR)
        darknet.copy_image_from_bytes(darknet_image, image_resized.tobytes())

        detections = darknet.detect_image(self.model, self.class_names, darknet_image, thresh=self.thresh)

        darknet.free_image(darknet_image)

        return detections


    @staticmethod
    def process_output(detections):

        detections = np.asarray(detections, dtype=object)

        labels = detections[:, 0]
        scores = detections[:, 1]
        bboxes = detections[:, 2]

        scores = scores.astype(np.float)
        bboxes = [list(b) for b in bboxes]


        return labels, scores, bboxes