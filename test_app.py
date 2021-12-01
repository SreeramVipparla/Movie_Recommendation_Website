import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from datetime import date

from app import create_app
from models import setup_db, Actors, Movies
from auth0 import bearer_tokens


class TestCases(unittest.TestCase):


    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "testapp"
        self.database_path = "postgresql://{}/{}".format(
            'postgres:myPassword@localhost:5432', self.database_name)

        setup_db(self.app, self.database_path)
        
        self.assistant_auth_header = {
            'Authorization': '{}'.format(bearer_tokens['casting_assistant'])}
        self.producer_auth_header = {'Authorization': '{}'.format(
            bearer_tokens['executive_producer'])}
        self.director_auth_header = {
            'Authorization': '{}'.format(bearer_tokens['casting_director'])}

    # --------------------------------------------- #
    # ACTOR DATA
    # --------------------------------------------- #

        self.new_actor = {
            'name': 'Tom Holland',
            'age': 23,# Random value
            'gender': 'male'
        }

        self.update_actor = {
            'name': 'Tom Hanks',
            'age': 23,# Random value
            'gender': 'male'
        }

        self.update_actor_fail = {
            'age': 'ABC'# Random value
        }
    # --------------------------------------------- #
    # MOVIE DATA
    # --------------------------------------------- #

        self.new_movie = {
            'id':2,
            'title': 'Avengers',
            'release_date': '2012-06-22',# Random value
            'country': 'USA'
        }
       
        self.update_movie = {
            'title': 'Avengers',
            'country': 'UK'
        }
        self.new_movie_fail = {
            'title': 'Avengers',
            'release_date': 1,
            'country': 'Global'
        }

        self.update_movie_fail = {
            'country': 632652572
        }
    # --------------------------------------------- #
    # APP BINDING AND CREATING TABLES
    # --------------------------------------------- #

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()

    
    def tearDown(self):
        """Executed after each test"""
        pass
    
    # --------------------------------------------- #
    # CASTING ASSISTANT TESTS
    # --------------------------------------------- #


    def casting_assistant_get_actors(self):
        res = self.client().get('/actors',
                                headers=self.assistant_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])
    
    def casting_assistant_get_movies(self):
        res = self.client().get('/movies', headers=self.assistant_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])
    
    def casting_assistant_delete_actor(self):
        res = self.client().delete('/actors/5',
                                   headers=self.assistant_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Permission not found.')
    
    def casting_assistant_create_new_movie(self):
        res = self.client().post('/movies', json=self.new_movie,
                                 headers=self.assistant_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Permission not found.')
    
    def casting_assistant_create_update_movie(self):
        res = self.client().post('/movies', json=self.update_movie,
                                 headers=self.assistant_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Permission not found.')
    
        

    # --------------------------------------------- #
    # EXECUTIVE PRODUCER TESTS
    # --------------------------------------------- #

    def executive_producer_get_actors(self):
        res = self.client().get('/actors', headers=self.producer_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])

    def executive_producer__unique_actor(self):
        res = self.client().get('/actors/1', headers=self.producer_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Method Not Allowed')

    def test_get_movies(self):
        res = self.client().get('/movies', headers=self.producer_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])

    def test_404_sent_requesting_unique_movie(self):
        res = self.client().get('/movies/1', headers=self.producer_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Method Not Allowed')

    def test_delete_movie(self):
        res = self.client().delete('/movies/1',
                                   headers=self.producer_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['delete'], 1)

    def test_404_if_movie_does_not_exist(self):
        res = self.client().delete('/movies/1000',
                                   headers=self.producer_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not found')
    def test_if_movie_creation_fails(self):
        res = self.client().post('/movies', json=self.new_movie_fail,
                                 headers=self.producer_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)

    def executive_producer_create_new_movie(self):
        res = self.client().post('/movies', json=self.new_movie,
                                 headers=self.producer_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])


    def test_update_movie_exist(self):
        res = self.client().patch('/movies/5', json=self.update_movie,
                                  headers=self.producer_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)



    # --------------------------------------------- #
    # CASTING DIRECTOR TESTS
    # --------------------------------------------- #

    def test_get_actors(self):
        res = self.client().get('/actors', headers=self.director_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])


    def test_create_new_actor(self):
        res = self.client().post('/actors', json=self.new_actor,
                                 headers=self.director_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])
    def casting_director_update_movie_exist(self):
        res = self.client().patch('/movies/5', json=self.update_movie,
                                  headers=self.director_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])

    def test_create_new_movie(self):
        res = self.client().post('/movies', json=self.new_movie,
                                 headers=self.director_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Permission not found.')

    def test_delete_movie(self):
        res = self.client().delete('/movies/9',
                                   headers=self.director_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Permission not found.')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
