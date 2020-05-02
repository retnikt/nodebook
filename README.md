# Notebook

![Backend CI Status](https://github.com/retnikt/notebook/workflows/backend/badge.svg?branch=master)
[![Dependabot Status](https://api.dependabot.com/badges/status?host=github&repo=retnikt/notebook)](https://dependabot.com)
[![Code Style: Black](https://img.shields.io/badge/code_style-black-000000)](https://github.com/psf/black)
[![Licence: MIT](https://img.shields.io/badge/licence-MIT-green)](https://opensource.org/licenses/mit-license.html)

A notebook app.

Notebook is free and open source software licensed under the [MIT Licence](https://opensource.org/licenses/mit-license.html).

# Development
The whole project is orchestrated using Docker Compose and Docker Swarm, with a PostgreSQL
database and a Traefik load-balancer and router.

This project is loosely based on [full-stack-fastapi-postgresql](https://github.com/tiangolo/full-stack-fastapi-postgresql).

## File Structure
Each folder should contain a `README.md` file explaining the purpose of its direct children, and other development details for the contents of the folder. In the root project folder:

- `README.md` - overall documentation of the project
- `CONTRIBUTING.md` - guidelines for contributing to the project
- `LICENCE.md` - contains the [MIT Licence](https://opensource.org/licenses/mit-license.html)
- `LICENSE.md` - a [symlink](https://en.wikipedia.org/wiki/Symbolic_link) to LICENCE.md for people who [~~can't spell~~](https://www.grammarly.com/blog/licence-license/) speak American English
- `docker-compose.yml` - contains defaults for running the full application stack (see https://docs.docker.com/compose/)
- `docker-compose.override.yml` - contains useful overrides of values in docker-compose.yml for development (see https://docs.docker.com/compose/extends/#multiple-compose-files)
- `frontend/` - contains the Vue frontend source code
- `backend/` - contains the Python backend source code

<!--
## Frontend
The frontend is written in Vue.js with TypeScript, with Vuex for state, Vue router, and Vuetify for UI. You will need [Node.js](https://nodejs.org) 12 ([NVM](https://github.com/nvm-sh/nvm) is recommended), [Yarn](https://yarnpkg.com/), [Docker](https://docs.docker.com/get-docker/), and [Docker Compose](https://docs.docker.com/compose/). To begin development, run `yarn install` in the frontend directory, then `npm run serve`. To run the backend as well, use `docker-compose up --scale frontend=0 -d`. This starts all the necessary backend containers but disables the frontend, as live reloading using the [Webpack Dev Server](https://webpack.org/) is not (easily) possible in Docker.
-->
