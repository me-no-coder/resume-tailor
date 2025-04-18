import openai
import re
import os
from typing import Tuple
from dotenv import load_dotenv
import sys

# --- Configuration ---
RESUME_PATH = "my_resume.tex"          # Path to your LaTeX resume
JOB_DESC_PATH = "job_description.txt"  # Path to the job description text file
OUTPUT_PATH = "tailored_resume.tex"    # Where the tailored resume will be saved
MODEL = "gpt-4o"                       # Preferred model (fallbacks are handled)

# --- Initialize OpenAI with Secure Key Loading ---
def initialize_openai():
    """Loads API key securely and checks access."""
    load_dotenv()  # Load environment variables from .env file
    api_key = os.getenv("OPENAI_API_KEY")  # Get the API key from environment

    # Stop if the API key is missing
    if not api_key:
        raise ValueError(
            "❌ API key missing. Please:\n"
            "1. Get a key from https://platform.openai.com/api-keys\n"
            "2. Add it to a `.env` file as: OPENAI_API_KEY=your_key_here"
        )

    client = openai.OpenAI(api_key=api_key)  # Create OpenAI client instance

    # Check if API key is valid by listing models
    try:
        client.models.list()
    except openai.AuthenticationError:
        raise ValueError("Invalid API key. Please check your credentials.")

    return client

# --- LaTeX Processing ---
def extract_latex_content(resume_path: str) -> Tuple[str, str]:
    """
    Safely extracts LaTeX content while preserving formatting.
    Returns (preamble, main_content)
    """
    try:
        # Read the LaTeX resume content
        with open(resume_path, 'r', encoding='utf-8') as file:
            latex_content = file.read()

        # Check for essential LaTeX tags
        if r'\begin{document}' not in latex_content:
            raise ValueError("LaTeX file must contain \\begin{document}")
        if r'\end{document}' not in latex_content:
            raise ValueError("LaTeX file must contain \\end{document}")

        # Split LaTeX into preamble and content
        preamble, _, remainder = latex_content.partition(r'\begin{document}')
        main_content, _, _ = remainder.partition(r'\end{document}')

        return preamble.strip(), main_content.strip()

    except FileNotFoundError:
        raise FileNotFoundError(f"Resume file not found at {resume_path}")

# --- AI Tailoring with Model Fallbacks ---
def tailor_resume(client, job_desc: str, resume_content: str) -> str:
    """Generates a tailored resume, trying multiple models if needed."""
    models_to_try = [
        "gpt-4o",         # Latest and most capable (free tier eligible)
        "gpt-4-turbo",    # Previous GPT-4 version
        "gpt-3.5-turbo"   # Fallback for free-tier users
    ]

    # Prompt instructing the AI on tailoring rules
    prompt = f"""
    TASK: Tailor this LaTeX resume to the job description BELOW.
    
    RULES:
    1. PRESERVE ALL LaTeX FORMATTING (no changes to commands or structure)
    2. Only modify text to better match the job description
    3. KEEP the same SECTIONS and LENGTH
    4. KEEP the WORK EXPERIENCE intact and only UPDATE SKILLS and PROFESSIONAL SUMMARY sections according to JOB DESCRIPTION
    5. DO NOT MODIFY the CODE BEFORE the comment "content begins here"
    6. OUTPUT the ENTIRE NEW LaTex content
    
    JOB DESCRIPTION:
    {job_desc}
    
    RESUME CONTENT:
    {resume_content}
    """

    last_error = None  # Store the last encountered error

    for model in models_to_try:
        try:
            print(f"⚙️ Trying model: {model}...")
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": "You are a resume expert who strictly preserves LaTeX formatting."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3  # Slight creativity while staying relevant
            )

            # Extract plain LaTeX output (strip markdown markers)
            tailored_content = response.choices[0].message.content
            return re.sub(r'^```(?:latex)?\n|\n```$', '', tailored_content).strip()

        except openai.NotFoundError as e:
            # Model not available — try next one
            last_error = f"Model {model} unavailable: {str(e)}"
            continue
        except openai.RateLimitError:
            # Rate limit reached — stop script
            raise RuntimeError("API rate limit exceeded. Please wait before retrying.")

    # If all models fail, show available models and last error
    available_models = [m.id for m in client.models.list().data]
    raise RuntimeError(
        f"❌ No working model. Last error: {last_error}\n"
        f"Your available models: {', '.join(available_models)}"
    )

# --- Main Execution ---
def main():
    try:
        # Initialize OpenAI client with credentials
        client = initialize_openai()

        # Read job description text file
        try:
            with open(JOB_DESC_PATH, 'r', encoding='utf-8') as file:
                job_desc = file.read()
        except FileNotFoundError:
            raise FileNotFoundError(f"Job description file not found at {JOB_DESC_PATH}")

        # Extract LaTeX preamble and main content
        preamble, resume_content = extract_latex_content(RESUME_PATH)

        # Generate a job-specific tailored resume
        print("✂️ Tailoring resume...")
        tailored_content = tailor_resume(client, job_desc, resume_content)

        # Write the updated content to a new LaTeX file
        with open(OUTPUT_PATH, 'w', encoding='utf-8') as file:
            file.write(preamble)
            file.write(r'\begin{document}' + '\n')
            file.write('\n' + tailored_content + '\n')
            file.write(r'\end{document}')

        print(f"✅ Success! Tailored resume saved to {OUTPUT_PATH}")

    except Exception as e:
        # Print any errors to standard error and exit
        print(f"❌ Error: {str(e)}", file=sys.stderr)
        sys.exit(1)

# Run the main function if this script is executed
if __name__ == "__main__":
    main()