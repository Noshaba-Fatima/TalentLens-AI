
from enum import Enum
from pydantic import BaseModel, Field
from pydantic import model_validator

class SkillCategory(str, Enum):
    PROGRAMMING = "programming"
    FRAMEWORK = "framework"
    DATABASE = "database"
    CLOUD = "cloud"
    DEVOPS = "devops"
    DATA_SCIENCE = "data_science"
    SOFT_SKILL = "soft_skill"
    OTHER = "other"


class ProficiencyLevel(str, Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXPERT = "expert"


class Skill(BaseModel):
    name: str
    category: SkillCategory
    proficiency: ProficiencyLevel
    is_required: bool = True


class JobDescription(BaseModel):
    job_title: str

    experience_min: float | None = Field(default=None, ge=0)
    experience_max: float | None = Field(default=None, ge=0)

    responsibilities: list[str]

    required_skills: list[Skill]
    preferred_skills: list[Skill]

    education: str | None = None

    additional_requirements: list[str] = Field(
        default_factory=list
    )

@model_validator(mode="after")
def validate_experience_range(self):
    if (
        self.experience_min is not None
        and self.experience_max is not None
        and self.experience_max < self.experience_min
    ):
        raise ValueError(
            "Maximum experience cannot be less than minimum experience"
        )
    return self