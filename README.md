# LinkedIn Post Generator

A simple AI-powered LinkedIn post generator that creates new posts based on a user's existing writing style.

The user enters a public LinkedIn profile URL, the app fetches their posts using Apify, processes them with an LLM, and uses a few relevant posts as examples to generate a new post.

## Tech Stack

* Python
* Streamlit
* LangChain
* Groq
* Apify

## How it works

```text
LinkedIn Profile URL
        ↓
      Apify
        ↓
 LinkedIn Posts
        ↓
   Post Processing
        ↓
  Few-shot Examples
        ↓
     Groq LLM
        ↓
 Generated LinkedIn Post
```

## Run Locally

Clone the repository and install the dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file:

```env
GROQ_API_KEY=your_groq_api_key
GROQ_MODEL=openai/gpt-oss-20b

APIFY_API_TOKEN=your_apify_api_token
APIFY_ACTOR_ID=harvestapi~linkedin-profile-posts
APIFY_TIMEOUT=180
```

Run the app:

```bash
streamlit run main.py
```

## Note

The app works with publicly available LinkedIn profile content through Apify. API usage may depend on the respective Groq and Apify plans.

## Future Improvements

* Better personalization
* Post history
* Caching
* Automated testing
* CI/CD
* Deployment
