from flask import Flask
from flask_restful import Api, Resource, reqparse, abort
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)
api = Api(app)
db = SQLAlchemy(app)


video_put_args = reqparse.RequestParser() #An instanciation
video_put_args.add_argument("name", type=str, help="Name of video is required", required = True)
video_put_args.add_argument("views", type=int, help="Views of video", required = True)
video_put_args.add_argument("likes", type=int, help="Likes of video", required = True)

videos = {}

def empty_dict_error(video_id):
    if video_id not in videos:
        abort(404, message = "The list you are trying to access is empty")

def id_already_exist_error(video_id):
    if video_id in videos:
        abort(409, message = "The id of the entry already exists")


class Video(Resource):
    def get(self, video_id):
        empty_dict_error(video_id) 
        return videos[video_id] 

    def put(self, video_id): 
        id_already_exist_error(video_id)
        args = video_put_args.parse_args()
        videos[video_id] = args
        return videos[video_id], 201 

    def delete(self, video_id):
        empty_dict_error(video_id)
        del videos[video_id]
        return "", 204


api.add_resource(Video, "/video/<int:video_id>")


if __name__ == "__main__":
    app.run(debug = True, port = 5005) 