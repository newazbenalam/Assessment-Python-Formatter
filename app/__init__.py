import json
import os
from app.dictionary import annotation_objects_dict, annotation_attributes_dict

def annotationType(filePath):
    arr = ['png', 'json']
    if str(os.path.basename(filePath)).split('.')[-2] in arr:
        return 'image'
    return ""


def annotationObjects(dataObj):
    annotation_objects = {}

    points = dataObj.get("points", {})

    annotation_objects[dataObj.get("classTitle", "").lower().replace(" ", "_")] = {
        "presence": 1 if points.get("exterior", []) else 0,
        "bbox": [point for sublist in points.get("exterior", []) for point in sublist]
    }
    return annotation_objects


def annotationAttributes(dataObj):
    annotation_attributes = {}

    tags = dataObj.get("tags", [])
    for tag in tags:
        class_title = dataObj.get("classTitle", "").lower().replace(" ", "_")
        if class_title not in annotation_attributes:
            annotation_attributes[class_title] = {}

        annotation_attributes[class_title][tag.get("name", "")] = tag.get("value", "")

    return annotation_attributes


def formatJsonDoc(filePath):
    with open(filePath, 'r') as file:
        data = json.load(file)
        output = []

        output.append({
            "dataset_name": f"{os.path.basename(filePath)}",
            "image_link": "",
            "annotation_type": annotationType(filePath),
            "annotation_objects": [],
            "annotation_attributes": []
        })

        if "objects" in data:
            for dataObj in data["objects"]:
                output[0]["annotation_objects"].append(
                    annotationObjects(dataObj))
                output[0]["annotation_attributes"].append(
                    annotationAttributes(dataObj))
        else:
            output[0]["annotation_objects"] = annotation_objects_dict
            output[0]["annotation_attributes"] = annotation_attributes_dict

        # print(json.dumps(output, indent=4))
        return json.dumps(output, indent=4)
