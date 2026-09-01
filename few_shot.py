import random


class FewShotPosts:
    def __init__(self, posts):
        self.posts = posts

    def get_filtered_posts(self, length, language, tag):
        filtered_posts = []

        if length == "Short":
            min_lines, max_lines = 1, 5
        elif length == "Medium":
            min_lines, max_lines = 6, 10
        elif length == "Long":
            min_lines, max_lines = 11, 15
        else:
            return filtered_posts

        for post in self.posts:
            line_count = post.get("line_count", 0)

            if (
                post.get("language") == language
                and min_lines <= line_count <= max_lines
                and tag.lower() in [
                    t.lower() for t in post.get("tags", [])
                ]
            ):
                filtered_posts.append(post)

        return filtered_posts

    def get_random_posts(self, length, language, tag, num_posts=2):
        filtered_posts = self.get_filtered_posts(
            length,
            language,
            tag
        )

        if len(filtered_posts) <= num_posts:
            return filtered_posts

        return random.sample(filtered_posts, num_posts)