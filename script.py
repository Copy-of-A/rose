import os
urls_stub = {
    'https://sochi.camera:8081/cam_242/video.m3u8': 10,
    'https://sochi.camera:8081/cam_349/video.m3u8': 20,
    'https://sochi.camera:8081/cam_411/video.m3u8': 30
}


def count_people(url, cam_id):
    cam_id = str(cam_id)
    os.system("ffmpeg -y -i " + url + " -vframes 1 shots/camera_" + cam_id + ".jpg")
    os.system("cd darknet && ./darknet detector test ./cfg/coco.data ./cfg/yolov3.cfg yolov3.weights -dont_show "
              "../shots/camera_" + cam_id + ".jpg > ../shots/result_" + cam_id + ".txt")
    people_count = 0
    with open("shots/result_" + cam_id + ".txt", "r") as f:
        data = f.readlines()
        for line in data:
            if line.find("person") == 0:
                people_count += 1
    f.close()
    os.remove("shots/camera_" + cam_id + ".jpg")
    os.remove("shots/result_" + cam_id + ".txt")
    # return urls_stub.get(url)
    return people_count
