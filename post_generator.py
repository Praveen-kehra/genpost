from llm_helper import llm
from few_shot import FewShotPosts
from linkedin_scraper import fetch_linkedin_posts
from preprocess import process_posts_data


MAX_LINKEDIN_POSTS = 5


def get_length_str(length):
    if length == "Short":
        return "1 to 5 lines"

    if length == "Medium":
        return "6 to 10 lines"

    if length == "Long":
        return "11 to 15 lines"

    return None


def generate_post(length, language, tag, linkedin_profile_url):
    posts = fetch_linkedin_posts(
        linkedin_profile_url,
        max_posts=MAX_LINKEDIN_POSTS
    )

    if not posts:
        raise ValueError(
            "No LinkedIn posts were found for this profile."
        )

    processed_posts = process_posts_data(posts)

    if not processed_posts:
        raise ValueError(
            "LinkedIn posts were fetched, but none could be processed."
        )

    few_shot = FewShotPosts(processed_posts)

    prompt = get_prompt(
        length,
        language,
        tag,
        few_shot
    )

    response = llm.invoke(prompt)

    return response.content


def get_prompt(length, language, tag, few_shot):
    length_str = get_length_str(length)

    if length_str is None:
        raise ValueError(
            "Length must be Short, Medium, or Long."
        )

    prompt = f'''
    Generate a LinkedIn post using the below information. No preamble.

    1) Topic: {tag}
    2) Length: {length_str}
    3) Language: {language}

    If Language is Hinglish then it means it is a mix of Hindi and English.
    The script for the generated post should always be English.
    '''

    examples = few_shot.get_random_posts(
        length,
        language,
        tag,
        num_posts=2
    )

    if examples:
        prompt += '''
        
        4) Use the writing style as per the following examples.
        '''

        for i, post in enumerate(examples):
            post_text = post["text"]

            prompt += f'''
            
            Example {i + 1}:
            
            {post_text}
            '''

    return prompt


if __name__ == "__main__":
    profile_url = input("Enter LinkedIn profile URL: ")

    print(
        generate_post(
            "Medium",
            "English",
            "Mental Health",
            profile_url
        )
    )