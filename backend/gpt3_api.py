# Import required modules
import os
import openai
from config import OPENAI_API_KEY  # Ensure the API key is stored in a separate config file

# Initialize OpenAI API Key
openai.api_key = OPENAI_API_KEY

def generate_summary(paper_text):
    """
    Function to generate a summary of a given academic paper using GPT-3.5 Turbo 16K API.
    
    Parameters:
        paper_text (str): The text content of the academic paper.
        
    Returns:
        str: A summarized version of the academic paper.
    """
    completion = openai.ChatCompletion.create(
      model="gpt-3.5-turbo-16k",
      messages=[
        {"role": "system", "content": "You are an assistant specialized in summarizing academic papers."},
        {"role": "user", "content": f"Please summarize the following academic paper: {paper_text}"}
      ],
      stream=True
    )

    summary = "".join(chunk.choices[0].delta["content"] for chunk in completion)
    return summary

def identify_trends(paper_text):
    """
    Function to identify trends in a given academic paper using GPT-3.5 Turbo 16K API.
    
    Parameters:
        paper_text (str): The text content of the academic paper.
        
    Returns:
        str: Trends identified within the academic paper.
    """
    completion = openai.ChatCompletion.create(
      model="gpt-3.5-turbo-16k",
      messages=[
        {"role": "system", "content": "You are an assistant specialized in identifying research trends."},
        {"role": "user", "content": f"Identify the research trends in the following academic paper: {paper_text}"}
      ],
      stream=True
    )

    trends = "".join(chunk.choices[0].delta["content"] for chunk in completion)
    return trends
