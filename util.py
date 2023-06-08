import base64
import io
from PIL import Image

def getPreviewImage(dataset):
    if(dataset):
        img = Image.open("./data/previews/" + dataset + "/preview.jpg")
        rawBytes = io.BytesIO()
        img.save(rawBytes, "jpeg")
        rawBytes.seek(0)
        img_base64 = base64.b64encode(rawBytes.read())
        return img_base64.decode()
    return []