from pydantic import BaseModel


class StatisticsResponse(BaseModel):
    total_activities: int
    total_execution_periods: int
