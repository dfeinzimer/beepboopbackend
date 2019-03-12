# beepboopbackend

Python: `Python 3.7`

Flask: `Flask 1.0.2`

Acevedo, Daniel: ?@csu.fullerton.edu

Feinzimer, David: dfeinzimer@csu.fullerton.edu

Roushdy, Yousef: ?@csu.fullerton.edu

Updated: March 11, 2019 7:30 PM
              
## Usage:

`foreman start`


## Possible Problem Solutions:

- `chmod +x api/articles/articles.sh`

- `chmod +x api/comments/comments.sh`

- `chmod +x api/tags/tags.sh`

- `chmod +x api/users/users.sh`

## Deprecated Usage: (Refactor & Removal In Progress)

1) `export FLASK_APP=app.py`

2) `export FLASK_ENV=development`

3) If anything was added to /requirements.txt

    3a) `pip freeze > requirements.txt`
    
    3b) `pip install -r requirements.txt`

4) `pip3 install foreman`

   `pip3 install tavern`

5) `sudo apt install ruby-foreman`

6) `flask run` or
   
   `python -m flask run` or 
   
   `python3 -m flask run` or

## Running tests (Deprecated):

1) `curl -i http://localhost:5000/users/`

2) `curl -i http://localhost:5000/articles/1`

3) Validate Procfile format using command `foreman check`


## Resources

https://mattstauffer.com/blog/using-a-procfile-to-streamline-your-local-development/
