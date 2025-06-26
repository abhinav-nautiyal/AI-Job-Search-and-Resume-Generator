import subprocess 
import os 

def compile_latex_to_pdf(latex_file_path): 
    #Check if the file exists 
    if not os.path.exists(latex_file_path): 
        print(f"{latex_file_path} does not exist.") 
        return 
    
    #Compile the LaTeX file into a PDF using pdflatex 
    try: 
        result = subprocess.run(
            ["pdflatex", "-interaction=nonstopmode", latex_file_path], 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE, 
            text=True, 
        ) 

        #Output any errors or status messages 
        print(result.stdout) 
        print(result.stderr) 

        if result.returncode == 0: 
            print(f"PDF successfully generated for {latex_file_path}") 
        else: 
            print(f"Failed to compile the LaTeX file. See above for details.")

    except Exception as e:
        print(f"Error while compiling LaTeX file: {e}")  

#Provide the path to your LaTeX file 
latex_file = "generated_resume.tex" # Replace with the actual path 
compile_latex_to_pdf(latex_file)