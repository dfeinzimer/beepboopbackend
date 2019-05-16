# beepboopbackend

| Member           |
|------------------|
| Acevedo, Daniel  |
| Feinzimer, David |
| Roushdy, Yousef  |


## Setup:

Nginx configuration:  Replace code in `/etc/nginx/sites-enabled/default` with code in the `nginx-setup/sites-enabled-default` fileOnce foreman has started, compare the ports for each service with the ports in the upstream portion of the nginx config file.  Alter if necessary.

Start Scylla: `docker start scylla`
Create the databases: `cd db/cmd/ && python3 scylla_create_all.py`

Fill the databases: `cd db/cmd/ && python3 scylla_fill_all.py`

To delete database: `cd db/cmd/ && python3 scylla_destroy_all.py`


## Usage:

Start nginx: `sudo service nginx restart`

(OPTIONAL)Open a Scylla CQL session: `docker exec -it scylla cqlsh`

Start the services: `foreman start --formation all=3`

RSS: Check the api docs for the RSS feeder for what URLs to hit.



## Things To Be Installed:

[Things To Be Installed Wiki Page](https://github.com/kernelpop/beepboopbackend/wiki/Things-To-Be-Installed)
- `pip3 install tavern`

- `pip3 install foreman`

- `pip3 install flask-cassandra`

- `pip3 install cassandra-driver`

- `pip3 install httpcache`

- `sudo apt install python-pytest`

- `sudo apt install ruby-foreman`

- `sudo apt install --yes nginx-extras`

- `sudo apt install --yes python3-cassandra`

- `sudo pip3 install Flask-BasicAuth`

- `sudo apt install --yes docker.io`

- `sudo usermod -aG docker $USER`



## Resources

HTTP Status Codes

    https://www.restapitutorial.com/httpstatuscodes.html

Procfiles

    https://mattstauffer.com/blog/using-a-procfile-to-streamline-your-local-development/

Nginx auth_request module

    https://docs.nginx.com/nginx/admin-guide/security-controls/configuring-subrequest-authentication/
