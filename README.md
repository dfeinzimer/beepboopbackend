# beepboopbackend

| Member           |
|------------------|
| Acevedo, Daniel  |
| Feinzimer, David |
| Roushdy, Yousef  |



## Usage:

Start nginx: `sudo service nginx restart`

Start Scylla: `docker start scylla`

Create Syllca tables(in db/cmd): `python3 scylla_create_all.py`

Fill the databases(in db/cmd): `python3 scylla_fill_all.py`

Open a Scylla CQL session: `docker exec -it scylla cqlsh`

Start the services: `foreman start --formation all=3`

RSS: Check the api docs for the RSS feeder for what URLs to hit.

For authorization use credentials username:"test@email.com" and password:"test@email.com".

Check database contents: `select * from users; select * from tags; select * from comments; select * from articles;`

Clean the databases(in db/cmd): `python3 scylla_destroy_all.py`



## Setup:

Nginx configuration:  Replace code in `/etc/nginx/sites-enabled/default` with code in the `nginx-setup/sites-enabled-default` fileOnce foreman has started, compare the ports for each service with the ports in the upstream portion of the nginx config file.  Alter if necessary.

Create the databases: `cd db/cmd/ && python3 scylla_create_all.py`

Create the `beepboopbackend` keyspace for Cassandra. First run: `docker exec -it scylla cqlsh` followed by: `CREATE KEYSPACE IF NOT EXISTS beepboopbackend WITH REPLICATION = {'class':'SimpleStrategy','replication_factor': 3};`



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
    
## Siege Test Results
From Project 2
    Results from project 2 All 3 urls from rss
    
    siege -t 1M  http://localhost/syndication/summary, http://localhost/syndication/full, http://localhost/syndication/comments -c 25 
    ** SIEGE 4.0.4
    ** Preparing 25 concurrent users for battle.
    The server is now under siege...
    Lifting the server siege...
    Transactions:		         749 hits
    Availability:		      100.00 %
    Elapsed time:		       59.14 secs
    Data transferred:	        0.32 MB
    Response time:		        1.94 secs
    Transaction rate:	       12.66 trans/sec
    Throughput:		        0.01 MB/sec
    Concurrency:		       24.51
    Successful transactions:         749
    Failed transactions:	           0
    Longest transaction:	        2.60
    Shortest transaction:	        1.31
 
From Project 3
    Results from project 3 All 3 urls from rss

    siege -t 1M  http://localhost/syndication/summary, http://localhost/syndication/full, http://localhost/syndication/comments -c 25 
    ** SIEGE 4.0.4
    ** Preparing 25 concurrent users for battle.
    The server is now under siege...
    Lifting the server siege...
    Transactions:		         510 hits
    Availability:		      100.00 %
    Elapsed time:		       59.10 secs
    Data transferred:	        0.26 MB
    Response time:		        2.82 secs
    Transaction rate:	        8.63 trans/sec
    Throughput:		        0.00 MB/sec
    Concurrency:		       24.31
    Successful transactions:         510
    Failed transactions:	           0
    Longest transaction:	        4.77
    Shortest transaction:	        1.06
