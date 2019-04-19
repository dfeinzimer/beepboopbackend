# beepboopbackend

| Member           |
|------------------|
| Acevedo, Daniel  |
| Feinzimer, David |
| Roushdy, Yousef  |



## Usage:

Create the databases: `cd db/cmd/ && python3 create_all.py`

Fill the databases: `python3 fill_all.py`

Start the services: `cd ../.. && foreman start --formation all=3`

Nginx configuration:  Replace code in `/etc/nginx/sites-enabled/default` with code in the `nginx-setup/sites-enabled-default` file
                      Once foreman has started, compare the ports for each service with the ports in the upstream portion of the nginx config file.  Alter if necessary.

Start nginx: `sudo service nginx restart`

RSS: Check the api docs for the RSS feeder for what URLs to hit.

Clean the databases: `cd db/cmd/ && python3 destroy_all.py`



## Things to install:

- `pip3 install tavern`

- `pip3 install foreman`

- `sudo apt install python-pytest`

- `sudo apt install ruby-foreman`

- `sudo apt install --yes nginx-extras`

- `sudo pip3 install Flask-BasicAuth`



## Resources

HTTP Status Codes

    https://www.restapitutorial.com/httpstatuscodes.html

Procfiles

    https://mattstauffer.com/blog/using-a-procfile-to-streamline-your-local-development/

Nginx auth_request module

    https://docs.nginx.com/nginx/admin-guide/security-controls/configuring-subrequest-authentication/
