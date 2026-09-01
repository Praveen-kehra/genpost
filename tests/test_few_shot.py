from few_shot import FewShotPosts


def test_get_filtered_posts_matches_length_language_and_tag():
    posts = [
        {
            "text": "Test post",
            "line_count": 7,
            "language": "English",
            "tags": ["Technology"],
        },
        {
            "text": "Another post",
            "line_count": 3,
            "language": "English",
            "tags": ["Technology"],
        },
    ]

    few_shot = FewShotPosts(posts)

    result = few_shot.get_filtered_posts(
        "Medium",
        "English",
        "Technology"
    )

    assert len(result) == 1
    assert result[0]["text"] == "Test post"


def test_get_filtered_posts_is_case_insensitive_for_tag():
    posts = [
        {
            "text": "Test post",
            "line_count": 8,
            "language": "English",
            "tags": ["technology"],
        }
    ]

    few_shot = FewShotPosts(posts)

    result = few_shot.get_filtered_posts(
        "Medium",
        "English",
        "Technology"
    )

    assert len(result) == 1


def test_get_filtered_posts_returns_empty_when_no_match():
    posts = [
        {
            "text": "Test post",
            "line_count": 8,
            "language": "English",
            "tags": ["Technology"],
        }
    ]

    few_shot = FewShotPosts(posts)

    result = few_shot.get_filtered_posts(
        "Medium",
        "English",
        "Mental Health"
    )

    assert result == []