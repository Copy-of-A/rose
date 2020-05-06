from flask import Flask, jsonify, abort, make_response, url_for
import script

app = Flask(__name__)

cameras = [
    {
        'id': 1,
        'title': u'Горный курорт Роза Хутор. 1100м. "Горная Олимпийская деревня". Вид на подъёмник Ювента.',
        'cam_url': u'https://sochi.camera:8081/cam_242/video.m3u8',
    },
    {
        'id': 2,
        'title': u'Горный курорт Роза Хутор. 1100м. "Горная Олимпийская деревня". Вид на подъёмник Заповедный лес.',
        'cam_url': u'https://sochi.camera:8081/cam_349/video.m3u8',
    },
    {
        'id': 3,
        'title': u'Горный курорт Роза Хутор. 1350м. Верхняя станция подъёмника "Волчья скала"',
        'cam_url': u'https://sochi.camera:8081/cam_411/video.m3u8',
    }

]


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.route('/cameras/<int:cam_id>', methods=['GET'])
def get_cam(cam_id):
    cam = [cam for cam in cameras if cam['id'] == cam_id]
    if len(cam) == 0:
        abort(404)
    new_cam = {}
    for field in cam[0]:
        if field == 'cam_url':
            new_cam['people'] = script.count_people(cam[0]['cam_url'])
        else:
            new_cam[field] = cam[0][field]
    return jsonify({'cam': new_cam})


def make_public_cam(cam):
    new_cam = {}
    for field in cam:
        if field == 'id':
            new_cam['uri'] = url_for('get_cam', cam_id=cam['id'], _external=True)
        else:
            new_cam[field] = cam[field]
        new_cam['people'] = script.count_people(cam['cam_url'])
    return new_cam


@app.route('/cameras', methods=['GET'])
def get_cameras():
    return jsonify([make_public_cam(cam) for cam in cameras])


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
