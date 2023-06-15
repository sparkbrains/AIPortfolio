import torch
from PIL import Image
from django.conf import settings
import os


model = torch.hub.load(os.path.join(settings.BASE_DIR,"yollo/"),'custom',path='yollo/best.pt',source='local')

def yolo_detection(path,user_image):

    image = Image.open(path)
    classes=[]
    # Run object detection on the image
    results = model(image)
    detection_counts = dict(results.pandas().xyxy[0]['name'].value_counts())
    detect = []
    # Print the detected objects and their corresponding confidence scores
    for obj in results.pandas().xyxy[0].values:
        detect.append(obj)
    for detection in detect:
        if len(detect) != 0:
            classes.append(detection[6])
            # rect_coordinates = detection[:4]
            concatenated_image = Image.fromarray(results.render(image)[0])
            for i in range(1, len(results.render(image))):
                concatenated_image = Image.fromarray(concatenated_image.concat(results.render(image)[i]))
            concatenated_image.save(os.path.join(settings.BASE_DIR,"static/portfolio/")+user_image)
            path_to_replace = path
            replace_path = os.path.join(settings.BASE_DIR,"static/portfolio/")+user_image.replace(path_to_replace, '')
            path_save_image = str(replace_path)
            split_path = path_save_image.split('static/')
            str_image_path = str(split_path[1])
            return detection_counts, str_image_path


        else:
            return None
    # path_to_replace = path
    # replace_path = os.path.join(settings.BASE_DIR,"static/portfolio/")+user_image.replace(path_to_replace, '')
    # path_save_image = str(replace_path)
    # split_path = path_save_image.split('static/')
    # str_image_path = str(split_path[1])
    # return detection_counts, str_image_path

