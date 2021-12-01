# Movie Recommendation Website

# Overview

<img src="https://user-images.githubusercontent.com/86887626/144291368-50b79671-27c8-404f-b018-61a3d9190a26.jpg
" width="700" height="300">

# Introduction

The movie recommandation website is a flask app created using Python, HTML, CSS and JavaScript. The app recommends movies to the user based on the users selection. The app is also hosted on heroku.
The app has the following endpoints.

- GET /actors and /movies
- POST /actors and /movies and
- DELETE /actors/ and /movies/
- PATCH /actors/ and /movies/

# Tech Stack

The tech stack includes:

- **SQLAlchemy ORM** to be our ORM library of choice
- **PostgreSQL** as our database of choice
- **Python3** and **Flask** as our server language and server framework
- **Flask-Migrate** for creating and running schema migrations (locally)
- **Heroku**, **Auth0**, and **Unittest** for deployment and testing.

# Set up

1. Clone the project repository:

```
https://github.com/SreeramVipparla/Movie_Recommendation_Website.git
```

2. Initialize and activate a virtualenv:

```
$ python3 -m venv env
$ source env/bin/activate
```

2. Install the dependencies:

```
$ pip install -r requirements.txt
```

3. Replace setup.sh with your own data and run-

```
$ source setup.sh
```

4. Run the development server:

```
$ export FLASK_APP=app
$ export FLASK_ENV=development # enables debug mode
$ python3 app.py
```

5. Navigate to [http://localhost:5000](http://localhost:5000)

# Testing

To run the tests, run

```

python3 test_app.py

```

Expected result:
Ran 9 tests

OK

# JWT TOKENS

The JWT tokens are provided in the auth0.py file as follows:

"user" : `Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InNFNjFQV2hheGxBQmdKQndfWDdjdyJ9.eyJpc3MiOiJodHRwczovL2Rldi1wamR6bWJiOS51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjFhMzA3ODI5M2Q1NDAwMDY5YzdmZWI5IiwiYXVkIjoiaHR0cDovL2xvY2FsaG9zdDo1MDAwIiwiaWF0IjoxNjM4MzU1ODgwLCJleHAiOjE2Mzg0NDIyODAsImF6cCI6IkhQa0hRdmZEQUZvVEwzb3I0ZzFnVFNaTXBHODF6WTVuIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyJdfQ.RYw3Hm7bsne2BVTTxYD3fmwa6gmLpapdJXof_G0_RNHy9nak_j8c-HcAWZkM6brCbaMjEItR69tWvUktnmW-jSyQvLUikgQzXlADaETHbehdT8AyDhWRzmKbtXjb2OaINHHuPqk-7wenlASaYk_9LzX99ebNs66ZJqtHI27XVl7Vr9r4rWIeLAyJNzMojJedDP9bAn7MciAZQaddz-YGkit9G_oh-CxYpEka_yDZvE35vgZjFbkPk4JGgj6FU-YHaFdTy9xFiNk5tPw6LVfufNshjF920wNH2NSEZN3Kf7es8pYMI7dCTNBDw3lMSMgZBveLUHAW15XR8sOVEvjWtg"`

admin" : `Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InNFNjFQV2hheGxBQmdKQndfWDdjdyJ9.eyJpc3MiOiJodHRwczovL2Rldi1wamR6bWJiOS51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjFhMzA4MmFhYjc5YzkwMDcxM2Y0MzYwIiwiYXVkIjoiaHR0cDovL2xvY2FsaG9zdDo1MDAwIiwiaWF0IjoxNjM4MzU2MDA4LCJleHAiOjE2Mzg0NDI0MDgsImF6cCI6IkhQa0hRdmZEQUZvVEwzb3I0ZzFnVFNaTXBHODF6WTVuIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6bW92aWVzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwb3N0Om1vdmllcyJdfQ.g_33LXw-ByZHSill7HvNRWeoBeO5fvopAGz3HaUiA6J4w19ievjwfBlQZd6gi0O7Unc7RzJaCgeXMUUVxU9Ck-Zi4cR3NmYRS-elG6KNQD2YqWYdBWhGHAHmins4pQMaT_l7c0nQM5eDEXUks75N4e2y0XLODf_PgToFvejQVTpFb3B2tfzhF4s29pHlpIuR5y3AWhvC9d8eWkMY0c6XuXgyyyjmZss6n16S5k-y7pgL00OUzkjn6aZ4zoVQVhWmVslSiFytdgz9kazMF7O0n65WBdwJnseIJycic0CXdeRcUBf-eCPT9hKxyOUxadd-LYAVk3vRQkXd-CwVi3vSAg`
",

1. AUth0 JWT link:` https://dev-pjdzmbb9.us.auth0.com/authorize?audience=http://localhost:5000&response_type=token&client_id=HPkHQvfDAFoTL3or4g1gTSZMpG81zY5n&redirect_uri=http://localhost:8080/&state=STATE`
