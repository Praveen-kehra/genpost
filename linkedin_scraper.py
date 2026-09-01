import os

import requests
from dotenv import load_dotenv


load_dotenv()


APIFY_API_TOKEN = os.getenv("APIFY_API_TOKEN")
APIFY_ACTOR_ID = os.getenv(
    "APIFY_ACTOR_ID",
    "harvestapi~linkedin-profile-posts"
)
APIFY_TIMEOUT = int(
    os.getenv("APIFY_TIMEOUT", "180")
)


def fetch_linkedin_posts(profile_url, max_posts=5):
    """
    Fetch public LinkedIn posts for a profile using Apify.
    """

    if not APIFY_API_TOKEN:
        raise ValueError(
            "APIFY_API_TOKEN is missing from .env"
        )

    if not profile_url:
        raise ValueError(
            "LinkedIn profile URL is required."
        )

    if "linkedin.com/in/" not in profile_url:
        raise ValueError(
            "Invalid LinkedIn profile URL."
        )

    if max_posts < 1:
        raise ValueError(
            "max_posts must be at least 1."
        )

    url = (
        f"https://api.apify.com/v2/actors/"
        f"{APIFY_ACTOR_ID}/run-sync-get-dataset-items"
    )

    payload = {
        "targetUrls": [profile_url],
        "maxPosts": max_posts,
        "maxReactions": 0,
        "maxComments": 0,
    }

    try:
        response = requests.post(
            url,
            params={"token": APIFY_API_TOKEN},
            json=payload,
            timeout=APIFY_TIMEOUT,
        )

        response.raise_for_status()

    except requests.exceptions.Timeout as exc:
        raise RuntimeError(
            "Apify request timed out. Please try again."
        ) from exc

    except requests.exceptions.RequestException as exc:
        raise RuntimeError(
            f"Unable to fetch LinkedIn posts from Apify: {exc}"
        ) from exc

    try:
        posts = response.json()
    except ValueError as exc:
        raise RuntimeError(
            "Apify returned an invalid response."
        ) from exc

    if not isinstance(posts, list):
        raise RuntimeError(
            "Unexpected response format from Apify."
        )

    return posts