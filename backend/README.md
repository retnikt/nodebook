# notebook/backend
The backend is written in [Python](https://python.org) using [FastAPI](https://fastapi.tiangolo.com) under [Uvicorn](https://uvicorn.org) and [Gunicorn](https://gunicorn.org) with a [PostgreSQL](https://www.postgresql.org) backend using [databases](https://encode.io/databases). You will need Python 3.8+, [Docker](https://docs.docker.com/get-docker/), [Docker Compose](https://docs.docker.com/compose/), and [Pipenv](https://pipenv.pypa.io) installed. Versions less than the current stable Python minor version, are not, and will never be, supported.

To get started, run `docker-compose up -d`. This will start all necessary containers, and the server will reload automatically when you make changes to the code, because the code is mounted as a Host volume. You can then access the backend API at http://localhost/api.

There is automatically generated API documentation using Swagger UI at http://localhost/api/docs.

Note that if you make changes to the project requirements (see Pipfile) or Dockerfile, the changes will not be reflected until you run `docker-compose up -d --build`.

[Pipenv](https://pipenv.pypa.io/) is used for package management. To install all dependencies including development dependencies, run `pipenv install -d`.

# File Structure
- `notebook/` - the root Python package of the backend API
- `scripts/` - contains useful scripts for development
- `setup.cfg` - contains configuration for tooling and packaging
- `Dockerfile` - the Docker file for the backend API
- `Pipfile` - contains information about the project's requirements (see https://pipenv.pypa.io/)
- `Pipfile.lock` - contains file integrity information about dependencies (see https://pipenv.pypa.io/)

# Code Style and Linting
Please read and adhere to [PEP-8](https://python.org/dev/peps/pep-0008/), and the [OpenStack StyleGuide](https://docs.openstack.org/hacking/latest/user/hacking.html). (except H301 which is stupid). Use strictly grammatical British English only.

The automatic tools used are, ordered from lowest to highest priority:
- [mypy](https://github.com/psf/mypy) is used for static type checking
- [flake8](https://flake8.pycqa.org) is used for general linting
  - [bugbear](https://github.com/PyCQA/flake8-bugbear) is a flake8 plugin used for finding likely bugs and design problems
  - [hacking](https://github.com/openstack/hacking) is a flake8 plugin used for enforcing the [OpenStack StyleGuide](https://docs.openstack.org/hacking/latest/user/hacking.html)
- [isort](https://github.com/timothycrosley/isort) is used for sorting imports
- [black](https://github.com/psf/black) is used for code formatting

Pull-requests may be closed silently if you have obviously not followed these rules.

Two scripts, `scripts/check` and `scripts/format`, are provided for respectively veriying and attempting to automatically correct the code style. Please run both before committing and fix any problems. (see also [Testing](#testing))

<!--
# Testing
Unit testing is done with [pytest](https://pytest.org). The `scripts/test` script will run all tests automatically for you. Please ensure all tests pass before committing, and add tests for new features and bug fixes to prevent regressions.

Coverage is done with [coverage.py](https://coverage.readthedocs.io/en/latest/); running it is included as part of the `scripts/test` script.

TODO(retnikt) uncomment and add tests!
-->

# Documentation
Documentation for end-users should be either in the root project [README](../README.md) if it is particularly notable, or the GitHub Wiki.

Documentation of code internals should be written in the docstrings.
