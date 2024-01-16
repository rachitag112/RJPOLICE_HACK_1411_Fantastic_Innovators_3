from flask import Flask
from flask_restful import Resource, Api

app = Flask("VideoAPI")
api = Api(app)

videos = {
    'video1': {'title': 'Murder happening in Bikaner'},
    'video2': {'title': 'Car accident in Jaipur'}
}

class Video(Resource):
    def get(self):
        return videos
    
api.add_resource(Video, '/')

if __name__ == '__main__':
    app.run()
