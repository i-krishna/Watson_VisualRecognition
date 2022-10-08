#call Watson Visual recognition

import json
from watson_developer_cloud import VisualRecognitionV3

visual_recognition = VisualRecognitionV3(
    '20xx-0x-xx',
     api_key='jyfhvgukjh' 
)

def call_watson(path):
    try:
        with open(path, 'rb') as images_file:
            classes = visual_recognition.classify(
                images_file,
                parameters=json.dumps({
                    "classifier_ids": ["barcode"],
                    "threshold": 0.0
                }))
            new_dict={}
            for i in classes['images'][0]['classifiers'][0]['classes']:
                new_dict[i['class']] = i['score']
            if new_dict['barcode'] > 0.45:
                return 'yes'
            else:
                return 'no'
            
    except Exception as e:
        return False
