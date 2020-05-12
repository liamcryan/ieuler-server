=============
ieuler server
=============

The server used in conjunction with the ieuler cli: https://github.com/liamcryan/ieuler.

::

    $ git pull https:github.com/ieuler-server.git
    $ cd ieuler-server
    $ pip install -r requirements.txt
    $ flask run

API
+++

GET /
~~~~~

Get the problems you have sent to IPE.

POST /
~~~~~~

Send the problems to IPE you want to save.

Authentication
~~~~~~~~~~~~~~

Authentication is using basic authentication.  Each request to the server will need your Project Euler username as well as the cookies from your last logged in session with the ieuler command line tool.  Using your username and the cookies, the server is able to tell if you are currently logged into Project Euler.  Only then will the server provide a response or receive data.

You username is saved to tie your problems and saved code.  Your password is not saved (neither are cookies, by the way) - take a look at app/models.py for more details on the sql schema.
