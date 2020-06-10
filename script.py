import os
import time
# import imutils as imutils
import cv2
from cv2 import *
urls_stub = {
    'https://sochi.camera:8081/cam_242/video.m3u8': 10,
    'https://sochi.camera:8081/cam_349/video.m3u8': 20,
    'https://sochi.camera:8081/cam_411/video.m3u8': 30
}


def video_streamer(path, cam_id, width=600, height=None):
    stream = cv2.VideoCapture(path)
    stream.grab()
    (grabbed, frame) = stream.read()

    if not grabbed:
        return

    # Меняем размер изображения
    # frame = imutils.resize(frame, width=width, height=height)
    res = bytearray(cv2.imencode(".jpeg", frame)[1])
    new_file = open("shots/camera_" + cam_id + ".jpeg", "wb")
    new_file.write(res)


def count_people(url, cam_id):
    cam_id = str(cam_id)
    video_streamer(url, cam_id)
    start = time.monotonic()
    # os.system("cd darknet && ./darknet detector test ./cfg/coco.data ./cfg/yolov3.cfg yolov3.weights -dont_show "
    #           "../shots/camera_" + cam_id + ".jpg > ../shots/result_" + cam_id + ".txt")
    os.system("cd darknet && ./darknet detector test ./cfg/coco.data ./cfg/yolov3.cfg yolov3.weights "
              "../shots/camera_" + cam_id + ".jpeg > ../shots/result_" + cam_id + ".txt")
    end = time.monotonic()
    print('span  : {:>9.2f}'.format(end - start))
    people_count = 0
    with open("shots/result_" + cam_id + ".txt", "r") as f:
        data = f.readlines()
        for line in data:
            if line.find("person") == 0:
                people_count += 1
    f.close()
    # os.remove("shots/camera_" + cam_id + ".jpg")
    # os.remove("shots/result_" + cam_id + ".txt")
    return urls_stub.get(url)
    # return people_count


count_people(next(iter(urls_stub.keys())), 1)
