# Solution to Python Flask technical challenge 🚀

<!-- Shields -->
![Top language](https://img.shields.io/github/languages/top/RodolfoFerro/technical-test-w-flask?style=for-the-badge)
![Code size](https://img.shields.io/github/languages/code-size/RodolfoFerro/technical-test-w-flask?style=for-the-badge)
[![Last commit](https://img.shields.io/github/last-commit/RodolfoFerro/technical-test-w-flask?style=for-the-badge)](https://github.com/RodolfoFerro/technical-test-w-flask/commits/master)
[![License](https://img.shields.io/github/license/RodolfoFerro/technical-test-w-flask?style=for-the-badge)](https://github.com/RodolfoFerro/technical-test-w-flask/blob/master/LICENSE)
[![Twitter follow](https://img.shields.io/twitter/follow/FerroRodolfo?style=for-the-badge)](https://twitter.com/FerroRodolfo/)

<!-- Project description -->
This repository contains the solution for a particular challenge using Python + Flask to create a web platform with several functionalities.

### Challenge description

The whole challenge specs could be listed as follows:

1. [X] Create a new Python project using Flask 1.1.x.
2. [ ] Create a `User` model with properties:
  - `Integer ID PK` (_self-increasing_)
  - `String Name (30)`
  - `String First_Last_Name (30)`
  - `String Second_Last_Name (30)` (_optional_)
  - `String Email (80)`
  - `DateTime BirthDate`
  - `String Gender` (_Accepts_ `M`, `F`, `O`)
  - `String Password` (_Must be encrypted_)
3. [ ] Create needed methods for CRUD operations in the user model, using REST.
4. [ ] Create a login view with route `'/login'` asking for `Email` and `Password` (this field must have a mask). In case of correct login, the app must generate a session for the user.
5. [ ] Create a view with route `'/users'` which should show a table with all registered users. It must contain an action button to delete the user, and a column with an icon for the gender.
  - [Male icon](https://cdn3.iconfinder.com/data/icons/fatcow/32x32_0560/male.png)
  - [Female icon](https://cdn3.iconfinder.com/data/icons/fatcow/32/female.png)
  - [Other icon](https://cdn3.iconfinder.com/data/icons/i-am-who-i-am/100/3-256.png)
6. [ ] Create a view with route `'/users?filter={name}'` (`name` could be only text), which must show a table with registered users whose full name includes the sent characters by the `name` parameter.
7. [ ] Create a view with route `'/user/{id}'` (`id` could be only a number), which should show the datailed user corresponding to the `id` variable, _in case it exists_. Otherwise, return a `404` screen for that route.
8. [ ] Create a `Role` model with properties:
  - `Integer ID PK` (_self-increasing_)
  - `String Name (30)`
  - `String Description (20)` (_optional_)
9. [ ] Create two roles, `Administrator` and `Client`, directly in the database.
10. [ ] Add relation of `User` with `Role` 1-1.
11. [ ] Create view of _creation/edition_ of a user. The user could only access this view if the user is logged in and the user session must be validated.

#### Extra considerations

- Date must be in format `DD/MM/YYY`.
- The name must appear concatenated as follows: `{ Name } { First_Last_Name } { Second_Last_Name }`.
- The gender option must show the tags `Male`
 for `M`, `Female` for `F` and `Other` for `O` (_must use filter tag_).
- If the logged user has type `Administrator`, the user should be able to see a button to delete the user.


### Extra developments

In this section I'll list all the additional features developed in the project.

- The project has been Dockerized


## Prerequisities

Before you begin, ensure you have met the following requirements:

#### For only-Docker usage:
* You have a _Windows/Linux/Mac_ machine with the latest version of [Docker](https://www.docker.com/) installed.

#### For only-Python usage:
* You have a _Windows/Linux/Mac_ machine running [Python 3.6+](https://www.python.org/).
* You have installed the latest versions of [`pip`](https://pip.pypa.io/en/stable/installing/) and [`virtualenv`](https://virtualenv.pypa.io/en/stable/installation/) or `conda` ([Anaconda](https://www.anaconda.com/distribution/)).

For general purposes, why not installing prerequisites for both cases?


## Install/Run with only Python

If you want to install the dependencies and work locally using only Python, you can simply follow this steps. If you want to directly work using Docker, jump to the "[Install/Run with Docker](https://github.com/RodolfoFerro/docker-flask-api#installrun-with-docker)" section.

Clone the project repository:
```bash
git clone https://github.com/RodolfoFerro/technical-test-w-flask.git
cd technical-test-w-flask
```

To create and activate the virtual environment, follow these steps:

Using `conda`:
```bash
$ conda create -n docker-flask python=3.7

# Activate the virtual environment:
$ conda activate docker-flask

# To deactivate:
(docker-flask)$ conda deactivate
```

Using `virtualenv`:
```bash
# In this case I'm supposing that your latest python3 version is +3.6
$ virtualenv docker-flask --python=python3

# Activate the virtual environment:
$ source docker-flask/bin/activate

# To deactivate:
(docker-flask)$ deactivate
```

To install the requirements using `pip`, once the virtual environment is active:
```bash
(docker-flask)$ pip install -r requirements.txt
```

Finally, if you want to run the app locally, simply run:
```bash
$ python app.py
```

Now you should be able to test the API at <http://0.0.0.0:5000/>.

## Install/Run with Docker

If you want to install the dependencies and work using Docker, you can simply follow this steps. If you want to simply work locally using only Python, jump back to the "[Install/Run with only Python](https://github.com/RodolfoFerro/docker-flask-api#installrun-with-only-python)" section.

Clone the project repository:
```bash
git clone https://github.com/RodolfoFerro/technical-test-w-flask.git
cd docker-flask-api
```

To build the Docker image, simply run:

```bash
$ docker build -t technical-test-w-flask .
```

To run the Docker image, run the following:
```bash
$ docker run -it -p 5000:5000 -v $(pwd):/app technical-test-w-flask
```

Now you should be able to test the API at <http://localhost:5000/>.

To stop the Docker container:
```bash
$ docker ps
$ docker stop <container-id>
```

## Contributing

To contribute to <project_name>, follow these steps:

1. Fork this repository.
2. Create a branch: `git checkout -b <feature_branch_name>`.
3. Make your changes and commit them: `git commit -m '<commit_message>'`
4. Push to the original branch: `git push origin <project_name>/<location>`
5. Create a Pull Request.

Additionally you can see the GitHub documentation on [creating a Pull Request](https://help.github.com/en/github/collaborating-with-issues-and-pull-requests/creating-a-pull-request).


<!-- ## Contributors

Thanks to the following people who have contributed to this project:

* @RodolfoFerro 📖💻 -->


## Contact

If you want to contact me you can reach me at <rodolfoferroperez@gmail.com>. There, or through any other of my social profiles your can find at: <https://rodolfoferro.glitch.me/>


## License

This project uses an [MIT License](https://github.com/RodolfoFerro/docker-flask-api/blob/master/LICENSE).
