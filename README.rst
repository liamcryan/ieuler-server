=============
ieuler server
=============

The server used in conjunction with the ieuler cli: https://github.com/liamcryan/ieuler.

::

    $ git pull https:github.com/ieuler-server.git
    $ cd ieuler-server
    $ pip install -r requirements.txt
    $ flask run

Authentication
~~~~~~~~~~~~~~

Authentication is using basic authentication.  Each request to the server will need your Project Euler username as well as the cookies from your last logged in session with the ieuler command line tool.  Using your username and the cookies, the server is able to tell if you are currently logged into Project Euler.  Only then will the server provide a response or receive data.

You username is saved to tie your problems and saved code.  Your password is not saved (neither are cookies, by the way) - take a look at app/models.py for more details on the sql schema.


Usage
~~~~~

You can run the server locally::

    $ flask run -p 2718

If you don't have a mysql db running, then a sqlite file will be created for you.

MySQL can also be used.  With mysql running, create a database and user::

    $ mysql
    Welcome to the MySQL monitor. Commands end with ; or \g
    ...
    mysql> create database db
    mysql> create user 'user@localhost' identified by 'somepass'
    mysql> grant all privelages on * . * to 'user@localhost'

The above is for reference, you can google how to create a database and set up a user - the database connection details expect a user and password.

Create environment variables::

    $ export MYSQL_USER=db
    $ export MYSQL_PASSWORD=somepass
    $ export MYSQL_DATABASE=db


Now, when you run `flask run -p 2718`, you MySQL database will be used.

Docker
~~~~~~

A simpler setup for MySQL would be to use the docker-compose.yml file.  The docker-compose.yml specifies a .env file.  Put the above MYSQL_USER=db, etc in this file.  Then::

    $ docker-compose up -d
