import os

from dotenv import load_dotenv
from langfuse import Langfuse
from langfuse.decorators import observe
from langfuse.openai import OpenAI
from pydantic import BaseModel, Field

load_dotenv()

langfuse = Langfuse(
    public_key=os.getenv("LANGFUSE_PUBLIC_KEY"),
    secret_key=os.getenv("LANGFUSE_SECRET_KEY"),
    host=os.getenv("LANGFUSE_HOST"),
)


class CompanyProject(BaseModel):
    company_name: str
    project_name: str
    project_description: str
    project_status: str
    funding_sought: int


class Grant(BaseModel):
    grant_name: str
    grant_description: str
    max_grant_amount: int


class GrantMatch(BaseModel):
    score: int = Field(description="A score between 0 and 5, higher is a better match")
    reason: str = Field(description="A reason for the score")


MATCH_PROMPT = """
You are a grant expert. You are given a project and a grant.
You need to rate the match between the grant and the project.

Here is the project:
{project}

Here is the grant:
{grant}
"""


@observe()
def get_project_grant_match(Grant: str, CompanyProject: str) -> GrantMatch:
    """
    Rates the match between a grant and a project
    """
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    prompt = MATCH_PROMPT.format(project=str(CompanyProject), grant=str(Grant))

    response = client.beta.chat.completions.parse(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        response_format=GrantMatch,
    )
    match = response.choices[0].message.parsed
    return match


def main():
    project = CompanyProject(
        company_name="Robot Burger Flippers",
        project_name="R&D for Robot Burger Flippers",
        project_description="We are a new robotics company that is looking to raise money to develop our burger-flipping robots.",
        project_status="We are currently in the research and development phase.",
        funding_sought=100000,
    )

    grant = Grant(
        grant_name="R&D for food and catering robotics",
        grant_description="Funding for research and development of food and catering robotics.",
        max_grant_amount=200000,
    )

    match = get_project_grant_match(grant, project)
    print(f"Score: {match.score}")
    print(f"Reason: {match.reason}")


if __name__ == "__main__":
    main()
