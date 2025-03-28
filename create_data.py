from datetime import datetime

import redis
import json
import os


def get_json_paths(source_path: str) -> list[str]:
    res = []


    for _, _, filenames in os.walk(source_path):
        for filename in filenames:
            if filename.lower().endswith("json"):
                res.append(os.path.join(source_path, filename))
    return res

def process_file(filename: str, redis_db: redis.Redis)-> dict:
    with open(filename, 'r') as file:
        while line := file.readline():
            line_data = json.loads(line)

            datas_filters = ["created_at", "lang"]
            if all(key in line_data for key in datas_filters) and line_data.get("lang") == "en":
                create_db_entry_from_line_data(line_data, redis_db)

def create_db_entry_from_line_data(line_data: dict, redis_db: redis.Redis) -> None:
    user = line_data["user"]
    user_id = user['id_str']
    user_key = f'user:{user_id}'
    chirps_id = line_data["id_str"]
    chirps_key = f'chirp:{chirps_id}'

    if redis_db.exists(user_key):
        chirps_count = int(redis_db.hget(user_key, "chirps_count"))

        redis_db.hset(user_key, "chirps_count", str(chirps_count + 1))
    else:
        chirps_count = 1
        user_structure = {
            'username': user["screen_name"],
            'follower_count': user["followers_count"],
            'following_count': user["friends_count"],
            'chirps_count': chirps_count
        }

        redis_db.hset(user_key, mapping=user_structure)
        redis_db.zadd('top_users_by_number_of_followers', {user_id: user["followers_count"]})

    message_date_time = datetime.strptime(line_data["created_at"], "%a %b %d %H:%M:%S %z %Y")
    chirps_structure = {
        'user_id': user["id_str"],
        "date_time": message_date_time.strftime("%Y-%m-%d %H:%M:%S"),
        'content': line_data["text"],
    }
    redis_db.hset(chirps_key, mapping=chirps_structure)
    redis_db.zadd('most_recent_chirps', {chirps_id: message_date_time.microsecond})
    redis_db.zadd('top_users_by_number_of_chirp', {user_id: chirps_count})

if __name__ == "__main__":
    r = redis.Redis(host='localhost', port=6379, decode_responses=True)
    r.flushall()

    json_files = get_json_paths("./data")

    for json_file in json_files:
        process_file(json_file, r)
        print(f"Finished processing file: {json_file}")

    print("Finished processing files")