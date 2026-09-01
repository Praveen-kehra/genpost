from langchain_core.exceptions import OutputParserException
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate

from llm_helper import llm


MAX_POST_LENGTH_FOR_ANALYSIS = 4000


def extract_metadata(post):
    """
    Extract metadata from a LinkedIn post.

    Line count is calculated locally.
    Language and tags are extracted using the LLM.
    """

    if not post or not post.strip():
        raise ValueError("Post content is empty.")

    post = post.strip()

    # Calculate line count locally instead of using the LLM.
    line_count = len(post.splitlines())

    # Prevent very large LinkedIn posts from exceeding
    # the model's context window.
    post_for_analysis = post[:MAX_POST_LENGTH_FOR_ANALYSIS]

    template = """
    You are given a LinkedIn post.

    Extract the following information:

    1. Return a valid JSON object. No preamble.
    2. The JSON object must contain exactly two keys:
       - language
       - tags
    3. "tags" must be an array containing a maximum of two
       relevant topic tags.
    4. "language" must be either "English" or "Hinglish".
    5. Hinglish means a mixture of Hindi and English.

    LinkedIn post:

    {post}
    """

    prompt = PromptTemplate.from_template(template)

    chain = prompt | llm

    response = chain.invoke(
        {"post": post_for_analysis}
    )

    try:
        parser = JsonOutputParser()
        metadata = parser.parse(response.content)

    except OutputParserException as exc:
        raise ValueError(
            "Unable to extract metadata from LinkedIn post."
        ) from exc

    # Validate the expected response structure.
    language = metadata.get("language")
    tags = metadata.get("tags")

    if language not in ("English", "Hinglish"):
        language = "English"

    if not isinstance(tags, list):
        tags = []

    # Keep only non-empty string tags.
    tags = [
        tag.strip()
        for tag in tags
        if isinstance(tag, str) and tag.strip()
    ][:2]

    return {
        "line_count": line_count,
        "language": language,
        "tags": tags,
    }


def process_posts_data(posts):
    """
    Process LinkedIn posts fetched from Apify.

    Each post is processed independently so that one failed
    post does not prevent the remaining posts from being used.
    """

    enriched_posts = []

    for post in posts:
        text = post.get("content", "").strip()

        if not text:
            continue

        try:
            metadata = extract_metadata(text)

            enriched_posts.append(
                {
                    "text": text,
                    **metadata,
                }
            )

        except Exception as exc:
            print(
                f"Skipping post because metadata extraction failed: "
                f"{exc}"
            )

    return enriched_posts