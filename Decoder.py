import base64
import numpy as np
import cv2

global IMG_SPLASH
global IMG_NODATA

def b64_to_array(uri):
    nparr = np.frombuffer(base64.b64decode(uri), np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_GRAYSCALE)
    return img

def unpack_images():
    global IMG_NODATA, IMG_SPLASH
    image_file = open(".\\images\\utils.tz","rb")
    IMG_SPLASH = image_file.read(457956)
    no_data = image_file.read(1636) 
    IMG_NODATA = b64_to_array(no_data)

def unpack_icons():
    global ICO_ERASE, ICO_EXPORT1, ICO_EXPORT2, ICO_EXPORT_MERGE, ICO_IMGANAL
    global ICO_LOAD, ICO_NEXT, ICO_PREVIOUS, ICO_QUIT, ICO_REFRESH, ICO_RESET
    global ICO_RESET, ICO_RUBIK, ICO_SETTINGS

    icons_file = open(".\\images\\icons\\icons.tz","rb")
    ICO_ERASE = icons_file.read(1944)
    ICO_EXPORT1 = icons_file.read(4548)
    ICO_EXPORT2 = icons_file.read(4512)
    ICO_EXPORT_MERGE = icons_file.read(4664)
    ICO_IMGANAL = icons_file.read(2416)
    ICO_LOAD = icons_file.read(2184)
    ICO_NEXT = icons_file.read(4020)
    ICO_PREVIOUS = icons_file.read(4064)
    ICO_QUIT = icons_file.read(2476)
    ICO_REFRESH = icons_file.read(5848)
    ICO_RESET = icons_file.read(2184)
    ICO_RUBIK = icons_file.read(4348)
    ICO_SETTINGS = icons_file.read(3624)

unpack_images()
unpack_icons()

