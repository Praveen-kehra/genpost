import streamlit as st
from post_generator import generate_post


st.title("LinkedIn Post Generator")


linkedin_profile_url = st.text_input(
    "LinkedIn Profile URL",
    placeholder="https://www.linkedin.com/in/your-profile/"
)


col1, col2, col3 = st.columns(3)


with col1:
    length = st.selectbox(
        "Length",
        ("Short", "Medium", "Long")
    )


with col2:
    language = st.selectbox(
        "Language",
        ("English", "Hinglish")
    )


with col3:
    tag = st.selectbox(
        "Topic",
        (
            "Mental Health",
            "Job Search",
            "Motivation",
            "Productivity",
            "Programming",
            "Leadership",
            "Technology",
            "Career"
        )
    )


if st.button("Generate Post"):

    if not linkedin_profile_url:
        st.error("Please enter a LinkedIn profile URL.")

    elif "linkedin.com/in/" not in linkedin_profile_url:
        st.error("Please enter a valid LinkedIn profile URL.")

    else:
        try:
            with st.spinner(
                "Fetching LinkedIn posts and generating your post..."
            ):
                post = generate_post(
                    length,
                    language,
                    tag,
                    linkedin_profile_url
                )

            st.subheader("Generated Post")
            st.write(post)

        except Exception as e:
            st.error(f"Unable to generate post: {e}")