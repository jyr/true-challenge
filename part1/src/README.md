# realstate Docker Compose

|Service| Service Name | Host | Port |
|---|---|---|---|
| Db | db | db.realstate-dev.com | 5432 |
| Api | api | api.realstate-dev.com | 8000 |

## Setting everything up

1. Add the following entries to your `/etc/hosts` file.

  ```
  # Services

  127.0.0.1  db.realstate-dev.com
  127.0.0.1  api.realstate-dev.com
  ```

2. Install docker https://www.docker.com/get-docker
3. Install docker-compose https://docs.docker.com/compose/install/
4. Start the **docker-compose** service.

## Basic Usage

- Enter in compose `cd build`

- Build db service `docker-compose up db --build`
- Build api service `docker-compose up api --build`

- Start all services `docker-compose up`

- Stop all services `docker-compose stop`

- Open the shell `docker-compose exec api /bin/sh`

## Data

**create a backup database**

```
docker-compose exec api /bin/sh -c -l "./manage.py dumpdata --natural-foreign --exclude auth.permission --exclude contenttypes --indent 2 > data/initial_to_dev.json""
```

**load initial data**

```
docker-compose exec api /bin/sh -c -l "./manage.py loaddata data/initial_to_dev.json"
```

## Django tests
```
$ docker-compose exec api /bin/sh -c -l "./manage.py test apis.client.tests.apis.versioned.v1.miniprofiles.test_endpoints.MiniProfileDetailEndpointTest"
$ docker-compose exec api /bin/sh -c -l "./manage.py test apis.client.tests.apis.versioned.v1.miniprofiles.test_endpoints"
$ docker-compose exec api /bin/sh -c -l "./manage.py test apis"
$ docker-compose exec api /bin/sh -c -l "./manage.py test backend"
```

## Connect to postgresql
```
$ docker-compose exec db /bin/sh -c -l "psql -h localhost -U docker -p 5432 realstate"
```
**Note**: Default postgresql user is 'docker' with password 'docker'.

## Deploy to AWS
```
$ docker-compose exec api /bin/sh -c -l ". env/bin/activate; cd realstate; zappa init"
$ docker-compose exec api /bin/sh -c -l ". env/bin/activate; zappa deploy dev -s realstate/zappa_settings.json; zappa tail -s realstate/zappa_settings.json"
$ docker-compose exec api /bin/sh -c -l ". env/bin/activate; zappa undeploy -s realstate/zappa_settings.json;"
```

## Database chores on AWS
```
$ psql -U postgres -h my_host.awsamazon.com
postgres=> create database realstate;
$ zappa manage staging showmigrations -s realstate/zappa_settings.json
$ zappa manage staging makemigrations -s realstate/zappa_settings.json
$ zappa manage staging migrate -s realstate/zappa_settings.json
```

## Docs

* **realstate API** - https://documenter.getpostman.com/view/1848785/SWLYAWAb?version=latest
* **HTTP Status Codes** - https://www.restapitutorial.com/httpstatuscodes.html

## Commitizen

1. Install Commitizen https://github.com/commitizen/cz-cli#installing-the-command-line-tool
2. Initialize the Commitize on project

```
$ cd $HOME
$ npm init --yes
$ npm install commitizen -g
$ commitizen init cz-conventional-changelog --save-dev --save-exact
```
3. Run commitizen after create a new changes on the project

```
$ git add .
$ git cz
```
