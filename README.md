# Chirp

## Requirements

Install the latest version of [Python](https://www.python.org/downloads/).

Install the latest version of [Redis](https://redis.io/docs/latest/operate/oss_and_stack/install/install-redis/) and launch the server with:

```
sudo systemctl start redis-server
```

## Installation

Create a virtual environment for Python:

```
python -m venv /path/to/new/virtual/environment
```

Activate it following the [documentation](https://docs.python.org/3/library/venv.html).

Install the required Python libraries:

```
pip install -r requirements.txt
```

## Running the application

### Load data

To load data, use the following command in the root directory of the project:

```
python main.py data
```

### Run web app

To launch the web application, use the following command in the root directory of the project:

```
python main.py website
```

If you have already loaded the data, you should see:

- The top 5 most recent chirps.
- The top 5 users with the most followers.
- The top 5 users who have posted the most chirps.

## How we stored data

The data is stored in Redis using a key-value model optimized for fast retrieval. Different Redis data structures are used for efficient indexing and querying:

- **User Data** is stored in a Redis Hash with keys formatted as `user:<user_id>`. Each user entry contains:

  - `username`: The user's display name.
  - `follower_count`: The number of followers the user has.
  - `following_count`: The number of users the user follows.
  - `chirps_count`: The total number of chirps the user has posted.

- **Chirp Data** is stored in a Redis Hash with keys formatted as `chirp:<chirp_id>`. Each chirp entry includes:

  - `user_id`: The ID of the user who posted the chirp.
  - `date_time`: The timestamp of when the chirp was created.
  - `content`: The text content of the chirp.

- **Indexes and Rankings** are maintained using Redis Sorted Sets (ZSETs):

  - `top_users_by_followers`: Stores user IDs sorted by follower count.
  - `top_users_by_chirps`: Stores user IDs sorted by the number of chirps they have posted.
  - `most_recent_chirps`: Stores chirp IDs sorted by timestamp to quickly retrieve the latest chirps.

## How we queried data

To efficiently retrieve and rank data, the application utilizes Redis commands optimized for sorted sets and hashes:

- **Retrieving User Data:**

  - The application queries user profiles using `HGETALL user:<user_id>`.

- **Fetching Recent Chirps:**

  - Retrieving Recent Chirps: The latest 5 chirps are fetched using `ZREVRANGE most_recent_chirps 0 4 WITHSCORES`, ensuring reverse chronological orde

- **Ranking Users by Followers and Chirps:**

  - The top 5 users by follower count are retrieved using `ZREVRANGE top_users_by_followers 0 4 WITHSCORES`.
  - The top 5 users by number of chirps are retrieved using `ZREVRANGE top_users_by_chirps 0 4 WITHSCORES`.

