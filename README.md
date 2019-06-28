
# Sports Catalog Project
This is a web server for allowing access to a catalog of sports equipment 
It features:
* A catalog of sporting equipment.
* Oauth2 authentication.
* Ability for the user to add and edit entries they have created after authenticated.

------------------------------
## Prerequisites
* [Amazon Lightsail Server](https://aws.amazon.com/lightsail/) or another Ubuntu server
	* Install the Ubuntu operating system
* [Apache](https://www.apache.org)
* [Postgres](https://www.postgresql.org)
* [Flask](flask.pocoo.org)
* [Sqlalchemy](https://www.sqlalchemy.org)
* [Google OAuth credentials](https://console.developers.google.com)
* [Python](https://www.python.org)
------------------------------

## Installation
* `cd` to the home directory on your server
* `clone` this repository as "udacity-linux-configuration"
* `cd udacity-linux-configuration` 
* run `sudo nano /etc/apache2/sites-enabled/000-default.conf`
* add the line "WSGIScriptAlias / /home/ubuntu/udacity-linux-configuration/catalog.wsgi" within the VirtualHost tag
* save the changes and exit the file
* `sudo -u postgres psql`
* `postgres=# create database catalog;`
* `postgres=# create user catalog withpassword 'password';`
* `postgres=# grant all privileges on database catalog to catalog;`
* copy your OAuth credentials into the "udacity-linux-configuration" directory with the name "client_secrets.json"
* run `python catalog_database.py` to create the database.

-----------------------------------
## To see a running example

* visit the server in a browser at http://3.220.93.200.xip.io/.
* perform a `GET` at http://3.220.93.200.xip.io/api/v1 to recieve a json of all items in catalog.
* perform a `GET` at http://3.220.93.200.xip.io/api/v1/<category>/<item> to recieve a json of a single item.
* copy your rsakey.pub into your working directory
* ssh with `ssh grader@3.220.93.200 -p 2222 -i rsakey.pub`

------------------------------------
## Authors
Zachary Dumas - https://github.com/zacharydumas

----------------------------------
## Acknowledgements
Initial commit comes from [Zachary Dumas' Sports Catalog Project](https://github.com/zacharydumas/fullstack-nanodegree-vm)
Solution to pip error fount at [Stack Exchange](https://stackoverflow.com/questions/28253681/you-need-to-install-postgresql-server-dev-x-y-for-building-a-server-side-extensi)