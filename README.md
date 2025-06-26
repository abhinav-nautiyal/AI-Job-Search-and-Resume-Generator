# AI-Powered Resume Generation Assistant

The Resume Generation Assistant is an AI-powered application that helps users create professional resumes and search for jobs. This project combines conversational AI with document generation to provide a seamless experience for job seekers.

## Table of Contents
- [Project Structure](#project-structure)
- [Features](#features)
- [Prerequisites & Installation](#prerequisites--installation)

## Project Structure

```bash
project-root/
├── langgraph-resume-generation/       # Backend AI components
│   ├── my_agent/
│   │   ├── agent.py                  # LangGraph agent definition
│   │   ├── utils/
│   │   │   ├── nodes.py              # Conversation nodes and logic
│   │   │   ├── tools.py              # Job search and resume generation tools
│   │   │   └── utils.py              # Resume template processing
│   ├── latex_to_pdf.py               # LaTeX to PDF converter
│   ├── latex_style_resume.tex        # Professional LaTeX resume template
│   └── langgraph.json                # LangGraph configuration
│
└── my-app/                           # Next.js frontend
    ├── app/                          # Next.js app router
    │   └── page.tsx                  # Main application page
    ├── components/                   # UI components
    │   ├── assistant/                # Assistant UI components
    │   │   ├── Thread.tsx            # Chat thread implementation
    │   │   └── TooltipIconButton.tsx # Custom tooltip buttons
    │   └── ui/                       # ShadCN UI components
    ├── lib/                          # Utility functions
    │   └── chatApi.ts                # API communication helpers
    └── public/                       # Static assets
```

## Features

### Conversational Interface
- Natural language interaction for resume building
- Guided prompts for collecting professional information
- Context-aware responses

### Job Search Integration
- Find relevant jobs based on skills and location
- Filter by salary requirements and posting date
- Direct links to job postings

### Professional Resume Templates
- LaTeX-based templates with customizable sections
- Multiple layout options (chronological, functional, hybrid)
- ATS-friendly formatting

### PDF Generation
- Automatic conversion to high-quality PDF
- Customizable styling options
- Downloadable output

### Responsive UI
- Clean, modern interface
- Dark/light mode support
- Mobile-friendly design

## Prerequisites 

### Prerequisites
- Node.js 18+
- Python 3.9+
- pdflatex (for PDF generation)
  - On Linux: `sudo apt-get install texlive-full`
  - On macOS: `brew install mactex`
  - On Windows: Install [MiKTeX](https://miktex.org/)
