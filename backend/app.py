
import os
from openai import OpenAI
from youtube_transcript_api import YouTubeTranscriptApi
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

def parse_link(video_link):
    return video_link.split('v=')[-1]

@app.route("/ask", methods=["POST"])
def ask():
    data = request.json
    link = data.get('link')
    if not link:
        return jsonify({"error": "No link provided"}), 400
    videoID = parse_link(link)
    response = YouTubeTranscriptApi.get_transcript(videoID)
    message = ''
    for i in response:
        message = message + i['text'] + ' '
    try:
        response = client.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        messages=[
            {
            "role": "system",
            "content": '''You are an assistant that gets the key points of the passed in message and 
                        returns a summary of what is said.  Skip any introductory or unimportant parts 
                        in your summary.  The summary should contain facts and tips mentioned in the 
                        message.  Only use what's in the message for the summary.\n\nIf the message contains 
                        a recipe, list out a full description of steps.  At the top of your summary you 
                        should also list out the ingredient names and amounts.  Format it like a recipe print out.  
                        Only return the recipe and no other commentary in the message.\n\nIf the message contains 
                        a tutorial of how to do a certain task or skill, list out all the steps in an orderly manner.
                        \n\nEvery summary should be well crafted and only contain material from the initial message 
                        and should not contain any information not relating to the main theme of the message.  
                        For example, do not include advertisements, only instructions or events that pertain to the 
                        original message. There should also be a title. Add a tips section as well if the message details
                        them.'''
            },
            {
            "role": "user",
            "content": message
            }
        ],
        temperature=0.7,
        max_tokens=3000,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
        )
        return jsonify({"summary": response.choices[0].message.content})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run()