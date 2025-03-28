import redis
import streamlit as st

def get_top_n_elements_for_attribute(n: int, element:str, attribute: str, redis_db: redis.Redis) -> list[dict]:

    try:
        top_elements_by_attribute = redis_db.zrevrange(attribute, 0, n)

        res: list[dict] = []
        for element_id in top_elements_by_attribute:
            key = f'{element}:{element_id}'
            top_element = redis_db.hgetall(key)
            res.append(top_element)

        return res
    except redis.exceptions.ResponseError:
        pass


if __name__ == "__main__":
    r = redis.Redis(host='localhost', port=6379, decode_responses=True)

    st.markdown("""
        <style>
            body {
                background-color: #f4f4f4;
                font-family: 'Arial', sans-serif;
            }
            .title {
                text-align: center;
                color: white;
                font-size: 36px;
                font-weight: bold;
                margin-bottom: 20px;
            }
            .header {
                font-size: 24px;
                text-align: center;
                color: white;
                margin-top: 20px;
                border-bottom: 2px solid #3498db;
                padding-bottom: 5px;
            }
        </style>
    """, unsafe_allow_html=True)

    top_5_chirps_by_most_recent = get_top_n_elements_for_attribute(5, "chirp", "most_recent_chirps", r)
    top_5_users_by_number_followers = get_top_n_elements_for_attribute(5, "user", "top_users_by_number_of_followers", r)
    top_5_users_by_number_chirps = get_top_n_elements_for_attribute(5, "user", "top_users_by_number_of_chirp", r)

    st.markdown('<div class="title">🐦 Chirp Analytics Dashboard</div>', unsafe_allow_html=True)

    st.markdown('<div class="header">📢 Top 5 Most Recent Chirps</div>', unsafe_allow_html=True)
    top_chirps = get_top_n_elements_for_attribute(5, "chirp", "most_recent_chirps", r)
    for chirp in top_chirps:
        user_id = chirp.get('user_id')
        user_key = f"user:{user_id}"
        user_username = r.hget(user_key, "username")
        st.write(f"**{user_username}**: {chirp.get('content')} ({chirp.get('date_time')})")

    st.markdown('<div class="header">👥 Top 5 Users by Followers</div>', unsafe_allow_html=True)
    top_users_followers = get_top_n_elements_for_attribute(5, "user", "top_users_by_number_of_followers", r)
    for user in top_users_followers:
        st.write(f"**{user.get('username')}** - {user.get('follower_count')} Followers")

    st.markdown('<div class="header">📝 Top 5 Users by Number of Chirps</div>', unsafe_allow_html=True)
    top_users_chirps = get_top_n_elements_for_attribute(5, "user", "top_users_by_number_of_chirp", r)
    for user in top_users_chirps:
        st.write(f"**{user.get('username')}** - {user.get('chirps_count')} Chirps")