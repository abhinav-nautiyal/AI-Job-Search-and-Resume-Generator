from langchain_community.tools.tavily_search import TavilySearchResults
from typing import Optional, Type

from langchain_core.callbacks import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field
import dotenv
import os
import requests
import json

from my_agent.utils.utils import generate_latex_resume


dotenv.load_dotenv("langgraph-example/.env.example")


class JobSearch(BaseModel):
    """
    keywords: str = The keywords to search for in the job listings.
    location: str = The location to search for jobs in.
    salary: The minimum salary for the job.
    age: The maximum age of job listings to return.
    """

    keywords: str = Field(description="The keywords to search for in the job listings.")
    location: str = Field(description="The location to search for jobs in.")
    salary: Optional[int] = Field(10 ,description="The minimum salary for the job.",)
    age: Optional[int] = Field(
        None, description="The maximum age of job listings to return.",
    )


class JobSearchInput(BaseModel):
    job_search: JobSearch




class JobSearchTool(BaseTool):
    name: str = "Job_Search"
    description: str = "Help users find job"
    args_schema: Type[BaseModel] = JobSearchInput
    # return_direct: bool = True

    def _run( 
        self, 
        job_search: JobSearch, 
        run_manager: Optional[CallbackManagerForToolRun] = None, 
    ) -> str:
        """Use the tool.""" 
        BASE_URL = os.getenv("JOOBLE_BASE_URL") 
        API_KEY = os.getenv("JOOBLE_API_KEY") 

        payload = job_search.model_dump(exclude_unset=True) 
        print(payload) 

        # call the API with the job_search_params 
        #return the results 
        headers = {"Content-Type": "application/json"} 
        results = requests.post( 
            f"{BASE_URL}{API_KEY}", 
            json=payload, 
            headers=headers, 
        ) 
        return results
    

class Education(BaseModel):
    institution: str = Field(description="The institution the person attended.") 
    degree: str = Field(description="The degree the person earned.") 
    start_date: str = Field(description="The start date of the education.") 
    end_date: str = Field(description="The end date of the education.") 
    gpa: Optional [float] = Field(description="The GPA of the person.") 
    coursework: list = Field(description="The coursework of the person.") 


class Experience(BaseModel):
    title: str = Field(description="The title of the experience.") 
    company: str = Field(description="The company of the experience.") 
    location: str = Field(description="The location of the experience.") 
    start_date: str = Field(description="The start date of the experience.") 
    end_date: str = Field(description="The end date of the experience.") 
    highlights: list = Field(description="The highlights of the experience.")


class Project(BaseModel):
    title: str = Field(description="The title of the project.") 
    description: str = Field(description="The description of the project.") 
    start_date: str = Field(description="The start date of the project.") 
    end_date: str = Field(description="The end date of the project.") 
    link: Optional[str] = Field(description="The link to the project.") 


class Technology(BaseModel):
    skills: list = Field(description="The skills of the person.") 
    languages: list = Field(description="The languages of the person.")



class ResumeGenerationInput (BaseModel): 
    name: str = Field(
        description="The name of the person to generate the resume for."
    ) 
    email: str = Field( 
        description="The email of the person to generate the resume for." 
    ) 
    professional_summary: str = Field( 
        description="The professional summary of the person to generate the resume for." 
    ) 
    education: list[Education] = Field( 
        description="The education of the person to generate the resume for." 
    ) 
    experience: list[Experience] = Field( 
        description="The experience of the person to generate the resume for." 
    )
    projects: list[Project] = Field( 
        description="The projects of the person to generate the resume for." 
    ) 
    Technologies: Technology = Field( 
        description="The skills of the person to generate the resume for." 
    ) 

class ResumeGenerationTool(BaseTool): 
    name: str = "Resume Generation" 
    description: str = "Helps users generate resumes." 
    args_schema: Type [BaseModel] = JobSearchInput 
    return_direct: bool = True 

    def _run(
        self, 
        resume_generator_params: ResumeGenerationInput,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        """Use the tool."""
        # Get a resume template based on the requested style.
        # Return the resume
        latex_output = generate_latex_resume(resume_generator_params)
        with open("generated_resume.tex", "w") as f:
            f.write(latex_output)
        
        print("Resume generated successfully!")

# tool =  [TravilySearchResults(max_result=1)]

if __name__ == "__main__": 

    sample_input = ResumeGenerationInput( 
        name="Abhinav", 
        email="abhinav@example.com", 
        professional_summary="Experiences ai engineer with a passion for creating efficient and scalable applications.", 
        education=[ 
            Education( 
                institution="University of India", 
                degree="Bachelor of Science in Computer Science", 
                start_date="Sept 2016", 
                end_date="May 2020", 
                gpa=3.8, 
                coursework=["Data Structures", "Algorithms", "Machine Learning"], 
            )
        ], 
        experience=[ 
            Experience( 
                title="Software Engineer", 
                company="Tech Corp", 
                location="Bangalore, IN", 
                start_date="June 2020", 
                end_date="Present", 
                highlights=[ 
                    "Developed and maintained high-performance web applications", 
                    "Implemented CI/CD pipelines, reducing deployment time by 50%",
                ],
            )
        ],
        projects=[
            Project(
                title="Personal Website", 
                description="Designed and developed a responsive personal website using React and Node.js", 
                start_date="Jan 2025", 
                end_date="Mar 2025", 
                link="https://abhi.com" 
            )
        ],
        technologies=Technology(
            languages=["Python", "JavaScript", "React", "Node.js", "Docker"],
        ),
    )

    tool = ResumeGenerationTool()
    tool.run(
        resume_generation_params=sample_input,
    )

tools = [JobSearchTool(), ResumeGenerationTool()]
