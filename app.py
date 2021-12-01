import os
from flask import Flask, request, jsonify, abort
import json
from flask_cors import CORS, cross_origin
from models import setup_db, Actors, Movies
from auth.auth import AuthError, requires_auth


def create_app(test_config=None):

    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    @app.route('/', methods=['GET'])
    def get_api_request(*args, **kwargs):
        try:

            return jsonify({
                'Message': 'Welcome to the Casting Agency ',
                'success': True
            })

        except AttributeError:
            abort(422)  

    # --------------------------------------------- #
    # ACTORS-ENDPOINTS(GET,POST,PATCH,DELETE)
    # --------------------------------------------- #
    @app.route('/actors', methods=['GET'])
    @requires_auth('get:actors')
    def get_actors(payload):

        actors = Actors.query.order_by(Actors.id).all()
        if actors is None:
            abort(404)
        try:
            actors_format = [actor.format() for actor in actors]
            response = {
                "success": True,
                "actors": actors_format
            }

        except BaseException:
            abort(404)

        return jsonify(response)

    @app.route('/actors', methods=['POST'])
    @requires_auth('post:actors')
    def post_actors(payload):
        body = request.get_json()
        try:
            req_name = body.get("name", None)
            req_age = int(body.get('age', None))
            req_gender = body.get('gender', None)
            actor = Actors(
                name=req_name,
                age=req_age,
                gender=req_gender
            )

            actor.insert()

            return jsonify({
                'success': True,
                'actors': actor.id
            }), 200
        except BaseException:
            abort(422)


    @app.route('/actors/<int:actor_id>', methods=['PATCH'])
    @requires_auth('patch:actors')

    def update_actor(id):
        actor = Actors.query.filter(Actors.id == id).one_or_none()
        if actor is None:
            abort(404)
        body = request.get_json()
        actor.name = body.get('name', actor.name)
        actor.age = body.get('age', actor.age)
        actor.gender = body.get('gender', actor.gender)
        actor.update()
        actors = Actors.query.all()
        formatted_actors = [actor.format() for actor in actors]

        return jsonify ({
          'success': True ,
          'actors' : formatted_actors ,
          'modified_actor' : id 
          })


    @app.route('/actors/<int:actor_id>', methods=['DELETE'])
    @requires_auth('delete:actors')

    def delete_actors(payload, actor_id):
        actor = Actors.query.filter(Actors.id == actor_id).one_or_none()

        if actor is None:
            abort(404)
        try:
            actor.delete()
            return jsonify({
                "success": True,
                "delete": actor_id
            }), 200
        except BaseException:
            abort(500)
    
    # --------------------------------------------- #
    # MOVIES-ENDPOINTS(GET,POST,PATCH,DELETE)
    # --------------------------------------------- #

    @app.route('/movies', methods=['GET'])
    @requires_auth('get:movies')
    def get_movies(*args, **kwargs):
        try:
            movie = Movies.query.order_by(Movies.id).all()
            movies = [abc.format() for abc in movie]

            if len(movies) == 0:
                abort(404)

            return jsonify({
                'success': True,
                'movies': movies
            })

        except BaseException:
            abort(422)

    @app.route('/movies', methods=['POST'])
    @requires_auth('post:movies')
    def post_movies(payload):
    
        body = request.get_json()
    
        title = body.get('title', None)
        country=body.get('country', None)
        release_date = body.get('release_date', None)

        movie = Movies(
            title=title,
            country=country,
            release_date=release_date
        )

        try:
            movie.insert()
            response = {
                "success": True,
                "movie": movie.format()
            }
        except BaseException:
            abort(422)

        return jsonify(response)


    @app.route('/movies/<int:movie_id>', methods=['PATCH'])
    @requires_auth('patch:movies')
    def update_movie(payload, movie_id):

        body = request.get_json()

        try:
            movie = Movies.query.filter(Movies.id == movie_id).one_or_none()
            if movie is None:
                abort(404)

            if 'title' in body:
                movie.title = body.get('title')
            if 'country' in body:
                movie.country = body.get('country')
            if 'release_date' in body:
                movie.release_date = body.get('release_date')

            movie.update()
            movie_updated = Movies.query.filter(
            Movies.id == movie_id).one_or_none()

            return jsonify({
                'success': True,
                'movies': [movie_updated.format()]
            }), 200

        except Exception:
            abort(500)

    @app.route('/movies/<int:movie_id>', methods=['DELETE'])
    @requires_auth('delete:movies')
    def delete_movie(payload, movie_id):

        movie = Movies.query.get(movie_id)

        if not movie:
            abort(404)
        title = movie.title
        Movies.delete(movie)

        return jsonify({
            "success": True,
            'message': 'Movie ' + title + ' successfully deleted.'
        }), 200
   
    '''
    Error handling for various errors
    '''

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": 'Bad Request'
        }), 400


    @app.errorhandler(401)
    def unauthorised(error):
        return jsonify({
            "success": False,
            "error": 401,
            "message": 'Unauthorised'
        }), 401

    @app.errorhandler(403)
    def forbidden(error):
        return jsonify({
            "success": False,
            "error": 403,
            "message": 'Forbidden'
        }), 403
    @app.errorhandler(404)
    def Not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Not found"
        }), 404
    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": 'Method Not Allowed'
        }), 405

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(500)
    def server_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "Server Error"
        }), 500

    '''
    AuthError

    '''

    @app.errorhandler(AuthError)
    def auth_error(error):
        return jsonify({
            "success": False,
            "error": error.status_code,
            "message": error.error['description']
        }), error.status_code



    return app


app = create_app()

if __name__ == '__main__':
    app.run()
