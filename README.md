# Wiki API wrapper

The Wiki API wrapper for internal ETL project



## Requirements

- Python 3.8>
- Postgresql or/and Redis
- pipenv(pip)


## How to install?
- Install python 3.x (https://www.python.org/downloads/release/python-3xx/)
- Install pipenv
```
	pip install  pipenv
```	
- Clone repo to local disk
```
	https://github.com/pydeveloper-t/Wiki-API-wrapper.git . 
```	
- Set an environment variable to place virtual environment in the same folder
```
	set export PIPENV_VENV_IN_PROJECT=1
```	
-  Installing all neccessary packages
```
    cd <project_folder>
    pipenv install --ignore-pipfile
```	





### Edit configuration file (.env)
Set 
- the actual credentials(DSN) for POSTGRESQL or/and REDIS: REDIS_DSN, POSTGRES_DSN
- select the required type of used database: USE_DB
 

```
USE_DB = 'postgresql'
#USE_DB = 'redis'
REDIS_DSN = 'redis://localhost:6379'
POSTGRES_DSN = 'postgres://xxxxxxxx:xxxxxxxxx@xxx.xxx.xxx.xxx:5432/xxxxx'
```


### Run service
```
uvicorn run_wiki_cashe:app
```


