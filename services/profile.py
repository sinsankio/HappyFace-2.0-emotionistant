from utils.profile import (
    generate_summarized_profile,
    generate_profiles_into_recommendation
)


def summarize_profile(profile: dict) -> dict:
    return {
        "profileSummary": generate_summarized_profile(profile)
    }


def summarize_profiles_into_recommendation(
        bio_data_profile: str,
        emotion_engagement_profile: str
) -> dict:
    return {
        "profileRecommendation": generate_profiles_into_recommendation(bio_data_profile, emotion_engagement_profile)
    }
