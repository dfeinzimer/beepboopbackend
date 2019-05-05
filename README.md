# beepboopbackend

| Member           |
|------------------|
| Acevedo, Daniel  |
| Feinzimer, David |
| Roushdy, Yousef  |



## Usage:

Start nginx: `sudo service nginx restart`

Start Sylla: `docker start scylla`

Fill the databases: `python3 fill_all.py`

Start the services: `cd ../.. && foreman start --formation all=3`

RSS: Check the api docs for the RSS feeder for what URLs to hit.

Clean the databases: `cd db/cmd/ && python3 destroy_all.py`



## Setup:

Nginx configuration:  Replace code in `/etc/nginx/sites-enabled/default` with code in the `nginx-setup/sites-enabled-default` fileOnce foreman has started, compare the ports for each service with the ports in the upstream portion of the nginx config file.  Alter if necessary.

Create the databases: `cd db/cmd/ && python3 create_all.py`

Create the `beepboopbackend` keyspace for Cassandra. First run: `docker exec -it scylla cqlsh` followed by: `Create keyspace beepboopbackend with replication={'class':'SimpleStrategy','replication_factor': 3};`



## Things to install:

[Things To Be Installed Wiki Page](https://github.com/kernelpop/beepboopbackend/wiki/Things-To-Be-Installed)



## Resources

HTTP Status Codes

    https://www.restapitutorial.com/httpstatuscodes.html

Procfiles

    https://mattstauffer.com/blog/using-a-procfile-to-streamline-your-local-development/

Nginx auth_request module

    https://docs.nginx.com/nginx/admin-guide/security-controls/configuring-subrequest-authentication/
