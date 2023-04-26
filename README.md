##

# yt-transcript

Get the transcript of a youtube video. This uses yt-dlp and OpenAI's whisper.

## Setup

Make a copy of the example environment variables file

```bash
$ cp .env.example .env
```

Add your [API key](https://beta.openai.com/account/api-keys) to the newly created `.env` file.

Install the requirements. Set up a python venv and run

```
pip install -r requirements.txt
```

## Usage

```
python3 yt_transcript.py "youtube-url"
```

## Acknowledgements

Written with GPT4.
