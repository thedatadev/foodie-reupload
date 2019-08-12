import os
import io
from google.cloud import vision
from google.cloud.vision import types
import urllib.request as ure
import requests
import json

def not_general(label):
    general_labels = ["dish", "cuisine", "appetizer", "fork", "spoon", "knife", "bowl", "napkin", "cup", "food", "european food", "asian food", "italian food"]
    for g in general_labels:
        if g in label:
            return False
    return True

def get_image_labels(image_uri):

    request_body = {
    "requests":[
        {
        "image":{
            "source":{
            "imageUri": image_uri
            }
        },
        "features":[
            {
            "type":"LABEL_DETECTION",
            "maxResults": 7
            }
        ]
        }
    ]
    }

    key = os.environ('GOOGLE_VISION_KEY')

    if not key:
        raise Exception("You need a key to proceed with image recognition")

    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = key

    # download image
    ure.urlretrieve(image_uri, "img/00000001.jpg")
    image = "img/00000001.jpg"

    client = vision.ImageAnnotatorClient()

    with io.open(image, 'rb') as image_file:
        content = image_file.read()
        image = types.Image(content=content)

    response = client.label_detection(image=image)
    labels = response.label_annotations
    list = sorted(labels, reverse=True, key=lambda x: x.score)
    list = [label.description for label in list if not_general(label.description)]
    return list

