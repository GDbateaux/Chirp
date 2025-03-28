# Chirp


## Requirements

Install latest version of [Python](https://www.python.org/downloads/).

Install latest version of [Redis](https://redis.io/docs/latest/operate/oss_and_stack/install/install-redis/) and lauch the server with ```sudo systemctl start redis-server```
 

## Installation

Create a virtual environment for Python : 
```
python -m venv /path/to/new/virtual/environment
```

Activate it following the [documentation](https://docs.python.org/3/library/venv.html).

Install the python libraries : 
```
pip install -r requirements.txt
```

## Running the application

### Load data
To load data use the following command in the root directory of the project:
```
python main.py data
```

### Run webapp
To launch the webapp use the following command in the root directory of the project:
```
python main.py website
```
If you already load the data you should see the top 5 most recent Chips, the top 5 users with most followers and the top 5 users with more chips.

## How we stored data

## How we queried data
