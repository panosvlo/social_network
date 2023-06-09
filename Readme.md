# Social Network Application

This application is a social networking site where you can subscribe to topics, follow users, and make comments or likes
on posts. It is built using React for the frontend, Django for the backend, and Postgres for the database. Automations
have been configured using the Celery task scheduler to create bot users that make posts, and interact with other users
by following them and commenting or liking posts.

## Prerequisites

Here are the tools you'll need to install before you get started:

- **Python 3.9.10:** Download it from the [official Python site](https://www.python.org/downloads/release/python-3910/)
- **Node.js 18.15:** Download it from the [official Node.js site](https://nodejs.org/download/release/v18.15.0/)
- **Docker (along with docker-compose):** Follow the instructions on
  the [official Docker site](https://docs.docker.com/engine/install/)
- **Tilt:** Follow the instructions on the [official Tilt site](https://docs.tilt.dev/install.html)

## Getting Started

To start the environment, run the following command:

`tilt up`

You can view all the resources being deployed at the
URL: [localhost:10350/r/(all)/overview](http://localhost:10350/r/(all)/overview). Here, you can click each resource to
see individual logs and status for each command and step. If one resource (or command) crashes for any reason, you can
restart it by clicking the 'Update' button next to the resource.

Initially, it will download the backend
dependencies ([backend dependencies overview](http://localhost:10350/r/backend_dependencies/overview)). Depending on
your internet connection, this may take some time. After that, it will continue with the frontend
dependencies ([frontend dependencies overview](http://localhost:10350/r/frontend_dependencies/overview)).

**Important Note:** If in the backend dependencies you are getting the error "WARNING: The script `<python package>` is
installed
in `<Python scripts location>` which is not on PATH," add the `<Python scripts location>` to your system's PATH
environment variable.

**Important Note:** The frontend dependencies will be installed successfully as long as the logs state "added `<number>`
packages" and "Server exited with exit code 0".

Once all resources are green, you can access the application by going to the
URL: [localhost:3000](http://localhost:3000/). You can create a new user to login to the application by going to the
URL: [localhost:3000/register](http://localhost:3000/register). Once you have successfully created the user, you can
login by visiting the URL: [localhost:3000/signin](http://localhost:3000/signin).

During the startup of the application for the first time, it will create some topics automatically, so that all the
other automations (creating bot accounts, making posts, etc.) can run thereafter.
Subscribing to a topic or making a post with a new topic will also create it if it doesn't exist in the database.
