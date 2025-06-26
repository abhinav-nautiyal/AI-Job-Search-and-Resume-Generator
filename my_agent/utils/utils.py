import textwrap
import os
from typing import List, Optional
from pydantic import BaseModel, Field


class Skill(BaseModel):
    name: str = Field(description="The name of the skill.")
    description: str = Field(description="The description of the skill.")
    level: int = Field(description="The level of the skill.")


class Education(BaseModel):
    institution: str = Field(description="The institution the person attended.")
    degree: str = Field(description="The degree the person earned.")
    start_date: str = Field(description="The start date of the education.")
    end_date: str = Field(description="The end date of the education.")
    gpa: Optional[float] = Field(description="The GPA of the person.")
    coursework: List[str] = Field(description="The coursework of the person.")


class Experience(BaseModel):
    title: str = Field(description="The title of the experience.")
    company: str = Field(description="The company of the experience.")
    location: str = Field(description="The location of the experience.")
    start_date: str = Field(description="The start date of the experience.")
    end_date: str = Field(description="The end date of the experience.")
    highlights: List[str] = Field(description="The highlights of the experience.")


class Project(BaseModel):
    title: str = Field(description="The title of the project.")
    description: str = Field(description="The description of the project.")
    start_date: str = Field(description="The start date of the project.")
    end_date: str = Field(description="The end date of the project.")
    link: Optional[str] = Field(description="The link to the project.")


class ResumeGenerationInput(BaseModel):
    name: str = Field(description="The name of the person to generate the resume for.")
    email: str = Field(
        description="The email of the person to generate the resume for."
    )
    professional_summary: str = Field(
        description="The professional summary of the person to generate the resume for."
    )
    education: List[Education] = Field(
        description="The education of the person to generate the resume for."
    )
    experience: List[Experience] = Field(
        description="The experience of the person to generate the resume for."
    )
    projects: List[Project] = Field(
        description="The projects of the person to generate the resume for."
    )
    skills: List[Skill] = Field(
        description="The skills of the person to generate the resume for."
    )


def generate_latex_resume(input_data: ResumeGenerationInput) -> str:
    # Read the template file
    template_path = "latex_style_resume.tex"
    try:
        with open(template_path, "r") as f:
            template = f.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"Template file {template_path} not found.")

    # Replace header information
    template = template.replace("John Doe", input_data.name)
    template = template.replace("youremail@yourdomain.com", input_data.email)
    template = template.replace("pdftitle={John Doe's CV}", f"pdftitle={{{input_data.name}'s CV}}")
    template = template.replace("pdfauthor={John Doe}", f"pdfauthor={{{input_data.name}}}")
    template = template.replace(
        "\\color{gray}\\textit{\\small John Doe - Page \\thepage{} of \\pageref*{LastPage}}",
        f"\\color{{gray}}\\textit{{\\small {input_data.name} - Page \\thepage{{}} of \\pageref*{{LastPage}}}}"
    )

    # Replace last updated date
    template = template.replace(
        "\\small\\color{gray}\\textit{Last updated in September 2024}",
        f"\\small\\color{{gray}}\\textit{{Last updated in May 2025}}"
    )
    
    # Find the sections and replace them
    
    # Replace welcome section with professional summary
    welcome_section_start = template.find("\\section{Welcome to RenderCV!}")
    welcome_section_end = template.find("\\section{Quick Guide}")
    
    if welcome_section_start != -1 and welcome_section_end != -1:
        professional_summary = f"""
    \\section{{Professional Summary}}

        
        \\begin{{onecolentry}}
            {input_data.professional_summary}
        \\end{{onecolentry}}
        """
        
        template = template[:welcome_section_start] + professional_summary + template[welcome_section_end:]
    
    # Remove quick guide section
    quick_guide_start = template.find("\\section{Quick Guide}")
    quick_guide_end = template.find("\\section{Education}")
    
    if quick_guide_start != -1 and quick_guide_end != -1:
        template = template[:quick_guide_start] + template[quick_guide_end:]
    
    # Replace education section
    education_section_start = template.find("\\section{Education}")
    education_section_end = template.find("\\section{Experience}")
    
    if education_section_start != -1 and education_section_end != -1:
        education_content = "\\section{Education}\n\n"
        
        for edu in input_data.education:
            education_content += f"""
        \\begin{{twocolentry}}{{
            
            
        \\textit{{{edu.start_date} – {edu.end_date}}}}}
            \\textbf{{{edu.institution}}}

            \\textit{{{edu.degree}}}
        \\end{{twocolentry}}

        \\vspace{{0.10 cm}}
        \\begin{{onecolentry}}
            \\begin{{highlights}}
"""
            if edu.gpa:
                education_content += f"                \\item GPA: {edu.gpa:.1f}/4.0\n"
            
            if edu.coursework and len(edu.coursework) > 0:
                education_content += f"                \\item \\textbf{{Coursework:}} {', '.join(edu.coursework)}\n"
                
            education_content += """            \\end{highlights}
        \\end{onecolentry}

"""
        
        template = template[:education_section_start] + education_content + template[education_section_end:]
    
    # Replace experience section
    experience_section_start = template.find("\\section{Experience}")
    experience_section_end = template.find("\\section{Projects}")
    
    if experience_section_start != -1 and experience_section_end != -1:
        experience_content = "\\section{Experience}\n\n"
        
        for i, exp in enumerate(input_data.experience):
            experience_content += f"""
        \\begin{{twocolentry}}{{
        \\textit{{{exp.location}}}    
            
        \\textit{{{exp.start_date} – {exp.end_date}}}}}
            \\textbf{{{exp.title}}}
            
            \\textit{{{exp.company}}}
        \\end{{twocolentry}}

        \\vspace{{0.10 cm}}
        \\begin{{onecolentry}}
            \\begin{{highlights}}
"""
            for highlight in exp.highlights:
                experience_content += f"                \\item {highlight}\n"
                
            experience_content += """            \\end{highlights}
        \\end{onecolentry}

"""
            if i < len(input_data.experience) - 1:
                experience_content += "        \\vspace{0.2 cm}\n\n"
        
        template = template[:experience_section_start] + experience_content + template[experience_section_end:]
    
    # Replace projects section
    projects_section_start = template.find("\\section{Projects}")
    projects_section_end = template.find("\\section{Technologies}")
    
    if projects_section_start != -1 and projects_section_end != -1:
        projects_content = "\\section{Projects}\n\n"
        
        for i, proj in enumerate(input_data.projects):
            link_text = proj.link if proj.link else "github.com/name/repo"
            
            projects_content += f"""
        \\begin{{twocolentry}}{{
            
            
        \\textit{{\\href{{{proj.link if proj.link else '#'}}}{{{link_text}}}}}}}
            \\textbf{{{proj.title}}}
        \\end{{twocolentry}}

        \\vspace{{0.10 cm}}
        \\begin{{onecolentry}}
            \\begin{{highlights}}
                \\item {proj.description}
            \\end{{highlights}}
        \\end{{onecolentry}}

"""
            if i < len(input_data.projects) - 1:
                projects_content += "        \\vspace{0.2 cm}\n\n"
        
        template = template[:projects_section_start] + projects_content + template[projects_section_end:]
    
    # Replace technologies section with skills
    tech_section_start = template.find("\\section{Technologies}")
    tech_section_end = template.find("\\end{document}")
    
    if tech_section_start != -1 and tech_section_end != -1:
        skills_content = "\\section{Skills}\n\n"
        
        # Group skills by type
        all_skills = ", ".join([f"{skill.name} ({skill.level}/10)" for skill in input_data.skills])
        
        skills_content += f"""
        \\begin{{onecolentry}}
            {all_skills}
        \\end{{onecolentry}}
"""
        
        template = template[:tech_section_start] + skills_content + template[tech_section_end:]
    
    return template


# Example usage
if __name__ == "__main__":
    sample_input = ResumeGenerationInput(
        name="John Doe",
        email="john.doe@example.com",
        professional_summary="Experienced software engineer with a passion for creating efficient and scalable applications.",
        education=[
            Education(
                institution="University of Example",
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
        skills=[
            Skill(
                name="Python", description="Proficient in Python development", level=9
            ),
            Skill(
                name="JavaScript", description="Proficient in JavaScript development", level=8
            )
        ]
    )

    latex_output = generate_latex_resume(sample_input)
    print(latex_output)

    # Optionally, save to a file
    with open("generated_resume.tex", "w") as f:
        f.write(latex_output)

