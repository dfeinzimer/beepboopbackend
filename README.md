# beepboopbackend

Python: `Python 3.7`

Flask: `Flask 1.0.2`

Acevedo, Daniel: ?@csu.fullerton.edu

Feinzimer, David: dfeinzimer@csu.fullerton.edu

Roushdy, Yousef: ?@csu.fullerton.edu

Updated: March 11, 2019 7:30 PM
              
## Usage:

`foreman start`


## Architecture:

    foreman ->

              Procfile ->

                         articles.sh ->

                                       Configure & run Flask app

                                       Run Tavern test yaml

                         Repeat for each api


## Possible Problem Solutions:

- `chmod +x api/articles/articles.sh`

- `chmod +x api/comments/comments.sh`

- `chmod +x api/tags/tags.sh`

- `chmod +x api/users/users.sh`

- `pip3 install foreman`

- `pip3 install tavern`

- `pip3 freeze > requirements.txt`

- `pip3 install -r requirements.txt`

- `sudo apt install ruby-foreman`

- Validate Procfile format: `foreman check`

- `sudo pip3 install Flask-BasicAuth`


## Simple curl Tests:

1) `curl -i http://localhost:5000/users/`

2) `curl -i http://localhost:5000/articles/1`


## Resources

https://mattstauffer.com/blog/using-a-procfile-to-streamline-your-local-development/
