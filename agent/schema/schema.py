from typing import Optional
from pydantic import BaseModel, ConfigDict, Field


class File(BaseModel):
    model_config = ConfigDict(extra="forbid")

    path: str = Field(description="The path of the file to be created")
    purpose: str = Field(
        description="The purpose of the file, e.g. 'main.py', 'README.md', etc."
    )


class Plan(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str = Field(description="The name of app to be built")
    description: str = Field(
        description="A one-line description of the app to be built"
    )
    techstack: str = Field(
        description="The tech stack to be used, e.g. 'Python, FastAPI, PostgreSQL'"
    )
    features: list[str] = Field(
        description="Features the app should have, e.g. 'user authentication'"
    )
    files: list[File] = Field(
        description="Files to be created, each with a path and purpose"
    )


class ImplementationTask(BaseModel):
    model_config = ConfigDict(extra="forbid")

    filepath: str = Field(
        description="Relative path within the project root, e.g. 'src/main.py' (not absolute)"
    )
    task_description: str = Field(
        description="Detailed description of the task to perform on the file"
    )


class TaskPlan(BaseModel):
    model_config = ConfigDict(extra="forbid")

    implementation_steps: list[ImplementationTask] = Field(
        description="Ordered steps to implement the project"
    )

class CoderState(BaseModel):
    task_plan: TaskPlan = Field(description="The plan for the task to be implemented")
    current_step_idx: int = Field(0, description="The index of the current step in the implementation steps")
    current_file_content: Optional[str] = Field(None, description="The content of the file currently being edited or created")