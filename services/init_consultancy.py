from utils.consultant import generate_init_consultancy


def initialize_consultancy(bio_data_profile: str, emotion_engagement_profile: str) -> dict:
    return {
        "emotionistant": generate_init_consultancy(bio_data_profile, emotion_engagement_profile)
    }
