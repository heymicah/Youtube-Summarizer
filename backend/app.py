import requests
from youtube_transcript_api import YouTubeTranscriptApi

def main():
    VIDEOID = 'dFCzfkf1x7g'
    response = YouTubeTranscriptApi.get_transcript(VIDEOID)
    print(response)

if __name__ == __name__:
    main()