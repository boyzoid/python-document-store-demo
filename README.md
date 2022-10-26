# Python Demo with MySQL Document Store

A demo for using Python to access a MySQL Document Store

## Setup

This setup assumes you already have [Python 3.10](https://www.python.org/) and [MySQL Shell](https://dev.mysql.com/downloads/shell/) installed and have access to a MySQL database.

* Open MySQL Shell and connect to your MySQL instance using the following command: `\c {user}:{password}@{host}:33060`

  * Where `{user}` is the username, `{password}` is the password, and `{host}` is the server domain name or IP address of your MySQL instance.
* In MySQL Shell, run the command `session.createSchema('py_demo')` to create the new schema.
* In MySQL Shell, run the following command: `util.importJson( '/absolute/path/to/project/data/scores.json', {schema: 'py_demo', collection: 'scores'})`

  * If the process runs successfully, you will see output similar to this:
    `Processed 12.65 MB in 17477 documents in 4.7405 sec (3.69K documents/s)  Total successfully imported documents 17477 (3.69K documents/s)`
* In the project root directory, copy the `.env_template` file to `.env` and fill in the values for the port Node will listen on and the database information.
* __Install Falcon__ - From a command prompt, run `pip install falcon`.
* __Install MySQL Connector__ - From a command prompt, run `pip install mysql-connector-python`.
* __Install DotEnv__ - From a command prompt, run `pip install python-dotenv`.
* __Install Waitress__ - From a command prompt, run `pip install waitress`.

___NOTE:__ On OSX, you may need to use `pip3`_

## Start Server

* From a command prompt, run `waitress-serve --listen=127.0.0.1:3001 api:api` in the project root directory.
* In a browser window, or at tool such as Postman, make a `GET` request to [http://localhost:3001/](http://localhost:3001/)

  * You should see the following result: `{"message":"Python Demo main endpoint"}`
