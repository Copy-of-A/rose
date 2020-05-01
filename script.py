urls_stub = {
    'https://sochi.camera:8081/cam_242/video.m3u8': 10,
    'https://sochi.camera:8081/cam_349/video.m3u8': 20,
    'https://sochi.camera:8081/cam_411/video.m3u8': 30
}


def count_people(url):
    return urls_stub.get(url)
