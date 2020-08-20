from flask import Flask
import flask_restful
import datebase
import json

app=Flask(__name__)

api=flask_restful.Api(app)

class Movie(flask_restful.Resource):
    def get(self,rank):
        connection=datebase.connect_movie_database()
        movies_tuple=datebase.get_movie_from_database(connection,rank)
        movies_dict={
            'rank':movies_tuple[1],
            'movie_title':movies_tuple[2],
            'movie_pic':movies_tuple[3],
            'movie_director':movies_tuple[4],
            'movie_stars':movies_tuple[5],
            'movie_year':movies_tuple[6]
        }
        movies_json=json.dumps(movies_dict,ensure_ascii=False, indent=4, separators=(',', ':'))
        print(movies_json)
        
        return movies_json,200,{"content-type":"application/json;charset=UTF-8"}


api.add_resource(Movie,'/movie/<rank>')

if __name__=='__main__':
    app.run(debug=True)