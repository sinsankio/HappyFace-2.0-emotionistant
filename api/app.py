import uvicorn
from fastapi import FastAPI, Body, HTTPException, status

from api.models import *
from services.init_consultancy import *
from services.profile import *
from services.query_consultancy import *

app = FastAPI(root_path="/happyface/v2/emotionistant")


@app.post(
    "/init-consultancy",
    response_description="consultancy initialization",
    status_code=status.HTTP_200_OK,
    response_model=InitConsultancy)
async def invoke_initialize_consultancy(init_consultancy_input: InitConsultancyInput = Body(...)) -> dict:
    if consultancy := initialize_consultancy(
            init_consultancy_input.bio_data_profile,
            init_consultancy_input.emotion_engagement_profile
    ):
        return consultancy
    raise HTTPException(status_code=status.HTTP_400_NOT_FOUND, detail="consultancy generation failed")


@app.post(
    "/summary",
    response_description="profile summarization",
    status_code=status.HTTP_200_OK,
    response_model=SummarizedProfile)
async def invoke_summarize_profile(summarize_profile_input: SummarizeProfileInput = Body(...)) -> dict:
    if summarized_profile := summarize_profile(summarize_profile_input.profile):
        return summarized_profile
    raise HTTPException(status_code=status.HTTP_400_NOT_FOUND, detail="profile summarization failed")


@app.post(
    "/recommendation",
    response_description="profile summarizations into recommendation",
    status_code=status.HTTP_200_OK,
    response_model=SummarizeProfilesIntoRecommendation)
async def invoke_summarize_profiles_into_recommendation(
        summarize_profile_input: SummarizeProfilesIntoRecommendationInput = Body(...)
) -> dict:
    if profile_recommendation := summarize_profiles_into_recommendation(
            summarize_profile_input.bio_data_profile,
            summarize_profile_input.emotion_engagement_profile
    ):
        return profile_recommendation
    raise HTTPException(status_code=status.HTTP_400_NOT_FOUND, detail="profiles into recommendation failed")


@app.post(
    "/query-consultancy",
    response_description="query consultation",
    status_code=status.HTTP_200_OK,
    response_model=QueryConsultancy)
async def invoke_talk_to_agent(query_consultancy_input: QueryConsultancyInput = Body(...)) -> dict:
    if consultancy := talk_to_agent(
            query_consultancy_input.query,
            query_consultancy_input.organization_name,
            query_consultancy_input.employee_id,
            query_consultancy_input.profile_recommendation,
            query_consultancy_input.chat_history
    ):
        return consultancy
    raise HTTPException(status_code=status.HTTP_400_NOT_FOUND, detail="consultancy generation failed")


if __name__ == "__main__":
    uvicorn.run(app, port=5003)
