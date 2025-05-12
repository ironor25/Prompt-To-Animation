


# from langchain_ollama import ChatOllama
from google import genai
from dotenv import load_dotenv
import os
load_dotenv()
import subprocess
import sys
from fastapi import FastAPI
from pydantic import BaseModel

class PromptRequest(BaseModel):
    prompt: str

app = FastAPI()

# llm = ChatOllama(model="llama3.2")
msg =""" You are a Python Manim coding assistant.  
User will describe an animation idea.  
Write complete runnable Python code using the Manim library.  
Output only pure Python code, no explanations, comments, headings, or extra text.  
Start with import statements.  
Define a Scene class and implement the animation properly indented.  
Here is the user's animation idea:

"""

# print(llm.invoke(prompt+msg).content)

# # file = open("backend\manim_setup.py","r")


async def llm_call(prompt):
       max_try = 3
       attempt = 0
       error =  False 
       while not error and attempt<= max_try:
            
            try:
                print(prompt)
                client = genai.Client(api_key= os.getenv("GEMINI_API"))
                response =  client.models.generate_content(
                    model="gemini-2.0-flash", contents= msg+prompt
                )
                code = response.text
                file = open("../frontend/anim_file/manim_setup.py", mode="w")
                code = code.replace("python","").replace("```","")
                file.write(code)
                file.close()
                print(response.text)

            # Run the command

                command = [sys.executable,"-m","manim", "-pqh","../frontend/anim_file/manim_setup.py"]
                subprocess.run(command ,
                            check=True,        # <-- raise error automatically if command fails
                            capture_output=True,
                            text=True).stdout
                error = True
                break
                        
            except subprocess.CalledProcessError as e:
                    print("Subprocess failed!")
                    print(f"Return code: {e.returncode}")
                    print(f"Error output: {e.stderr}")
                    prompt = f"Task:{msg + prompt}. The following code caused an error: {code} . Error message: {e.stderr}. Fix the code to complete the task successfully. Reply with only the corrected code, no explanation or extra text."
                    attempt+=1