🧠 LaTeX Resume Tailoring with OpenAI GPT
This Python script helps you automatically tailor your LaTeX resume to match a specific job description using OpenAI's GPT models (like gpt-4o or gpt-3.5-turbo), while preserving formatting and ensuring professional, context-relevant modifications.

📌 Features
✅ Keeps LaTeX formatting and structure completely intact
✅ Focuses on Skills and Professional Summary sections only
✅ Leaves Work Experience untouched
✅ Supports model fallback logic (gpt-4o → gpt-4-turbo → gpt-3.5-turbo)
✅ Uses .env for secure API key management
✅ Outputs a new tailored .tex file for easy compile

📂 Project Structure
resume-tailor/
├── my_resume.tex           # Your LaTeX resume
├── job_description.txt     # Target job description text
├── tailored_resume.tex     # Generated resume tailored to the job
├── resume_tailor.py        # This Python script
├── .env                    # Contains your OpenAI API key
└── README.md               # You're reading this!

🔧 Setup Instructions
1. Clone the Repo or Copy the Files
You can either clone your GitHub repo or just copy the files into a directory.

2. Install Required Packages
Make sure Python 3.7+ is installed. Then install dependencies:
pip install openai python-dotenv

3. Add Your OpenAI API Key
Create a .env file in the same directory with your API key:
OPENAI_API_KEY=your-api-key-here
https://platform.openai.com/account/api-keys

4. Prepare Required Files
my_resume.tex: Your resume in LaTeX format. Must contain \begin{document} and \end{document}.
job_description.txt: A plain-text job description you're tailoring for.
⚠️ This script modifies only the Skills and Professional Summary sections. Ensure those are clearly labeled in your LaTeX file.

5. Run the Script
python resume_tailor.py
If everything is set correctly, a new file tailored_resume.tex will be generated.

⚙️ How It Works (Under the Hood)
Reads your resume and splits it into preamble and main content using LaTeX tags
Sends your resume + job description to GPT with strict tailoring rules
Validates API model access, tries the best available model
Outputs a new .tex file ready to compile or export as PDF

📄 Example Prompt to GPT
TASK: Tailor this LaTeX resume to the job description BELOW.
RULES:
1. PRESERVE ALL LaTeX FORMATTING
2. Modify only SKILLS and PROFESSIONAL SUMMARY
3. Do NOT change section order or commands
...

🧠 Tips for Best Results
Be specific in the job description — include required skills, tools, and responsibilities.
Your LaTeX file should clearly separate sections like \section*{Professional Summary} and \section*{Skills}.
Works best if your original resume already contains strong, relevant content.

🛠 Troubleshooting
Error                                    | Fix
API key missing                          | Add your OpenAI key in .env
LaTeX file must contain \begin{document} | Ensure your .tex file is valid
Rate limit exceeded                      | Wait a few minutes and try again
Model not available                      | Check your OpenAI account permissions

🤝 Contributing
Feel free to fork this and extend it — e.g., allow section detection, CLI flags, PDF export etc.

🙌 Acknowledgments
Thanks to OpenAI for the awesome API, and the LaTeX community for clean, consistent formatting.