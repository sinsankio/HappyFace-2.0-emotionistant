from pydantic import Field, BaseModel


class InitConsultancy(BaseModel):
    emotionistant_response: str = Field(..., alias="emotionistant")


class InitConsultancyInput(BaseModel):
    bio_data_profile: str = Field(..., alias="bioDataProfile")
    emotion_engagement_profile: str = Field(..., alias="emotionEngagementProfile")


class SummarizeProfileInput(BaseModel):
    profile: dict = Field(...)


class SummarizedProfile(BaseModel):
    profile_summary: str = Field(..., alias="profileSummary")


class SummarizeProfilesIntoRecommendationInput(BaseModel):
    bio_data_profile: str = Field(..., alias="bioDataProfile")
    emotion_engagement_profile: str = Field(..., alias="emotionEngagementProfile")


class SummarizeProfilesIntoRecommendation(BaseModel):
    profile_recommendation: str = Field(..., alias="profileRecommendation")


class QueryConsultancyInput(BaseModel):
    query: str = Field(...)
    organization_name: str = Field(..., alias="organizationName")
    employee_id: str | int = Field(..., alias="employeeId")
    profile_recommendation: str = Field(..., alias="profileRecommendation")
    chat_history: list = Field(..., alias="chatHistory")


class QueryConsultancy(BaseModel):
    friend_query: str = Field(..., alias="friend")
    agent_response: str = Field(..., alias="emotionistant")
