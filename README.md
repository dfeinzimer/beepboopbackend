# beepboopbackend

| Member           | Role  | Ownership                               |
|------------------|-------|-----------------------------------------|
| Acevedo, Daniel  | DEV 2 | Tags, Comments, Flask CLI DB commands   |
| Feinzimer, David | OPS   | Procfile, Foreman, Tuffix, Tavern tests |
| Roushdy, Yousef  | DEV 1 | Articles, Users, HTTP Basic Auth.       |



## Usage:

Create the databases: `cd db/cmd/ && python3 create_all.py`

Fill the databases: `python3 fill_all.py`

Start the services: `cd ../.. && foreman start`

Run the tests: `py.test`

Clean the databases: `cd db/cmd/ && python3 destroy_all.py`



## Things to install:

- `pip3 install tavern`

- `pip3 install foreman`

- `sudo apt install python-pytest`

- `sudo apt install ruby-foreman`

- `sudo apt install --yes nginx-extras`

- `sudo pip3 install Flask-BasicAuth`



## Possible Problem Solutions:

- `foreman check`

- `pip3 freeze > requirements.txt`

- `pip3 install -r requirements.txt`

- `sudo service nginx restart`



## Resources

HTTP Status Codes

    https://www.restapitutorial.com/httpstatuscodes.html

Procfiles

    https://mattstauffer.com/blog/using-a-procfile-to-streamline-your-local-development/

Nginx auth_request module

    https://docs.nginx.com/nginx/admin-guide/security-controls/configuring-subrequest-authentication/
