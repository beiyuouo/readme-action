import base64
import os
import sys
from github import Github, GithubException

import pytz

import social

REPOSITORY = os.getenv("INPUT_REPOSITORY")
GHTOKEN = os.getenv("INPUT_GH_TOKEN")

COMMIT_MESSAGE = os.getenv("INPUT_COMMIT_MESSAGE")

BLOG_RSS_LINK = os.getenv("INPUT_BLOG_RSS_LINK")
BLOG_LIMIT = int(os.getenv("INPUT_BLOG_LIMIT"))

DOUBAN_NAME = os.getenv("INPUT_DOUBAN_NAME")
DOUBAN_LIMIT = int(os.getenv("INPUT_DOUBAN_LIMIT"))

BLOG_TIME_FORMAT = os.getenv("INPUT_BLOG_TIME_FORMAT")

TIME_ZONE = os.getenv("INPUT_TIME_ZONE")

GITHUB_NAME = os.getenv("INPUT_GITHUB_NAME")
GITHUB_LIMIT = int(os.getenv("INPUT_GITHUB_LIMIT"))


def decode_readme(data: str) -> str:
    """Decode the contents of old readme"""
    decoded_bytes = base64.b64decode(data)
    return str(decoded_bytes, "utf-8")


if __name__ == "__main__":
    g = Github(GHTOKEN)
    try:
        repo = g.get_repo(REPOSITORY)
    except GithubException:
        print(
            "Authentication Error. Try saving a GitHub Token in your Repo Secrets or Use the GitHub Actions Token, which is automatically used by the action."
        )
        sys.exit(1)
    contents = repo.get_readme()

    old_readme = decode_readme(contents.content)
    new_readme = old_readme

    tz = pytz.timezone(TIME_ZONE)

    if BLOG_RSS_LINK is not None and BLOG_LIMIT > 0:
        print("BLOG_RSS_LINK:" + BLOG_RSS_LINK)
        print("BLOG_LIMIT:" + str(BLOG_LIMIT))
        new_readme = social.generate_blog(
            BLOG_RSS_LINK, BLOG_LIMIT, new_readme, BLOG_TIME_FORMAT, tz
        )

    if DOUBAN_NAME is not None and DOUBAN_LIMIT > 0:
        print("DOUBAN_NAME:" + DOUBAN_NAME)
        print("DOUBAN_LIMIT:" + str(DOUBAN_LIMIT))
        new_readme = social.generate_douban(
            DOUBAN_NAME, DOUBAN_LIMIT, new_readme, time_zone=tz
        )

    if GITHUB_NAME is not None and GITHUB_LIMIT > 0:
        print("GITHUB_NAME:" + GITHUB_NAME)
        print("GITHUB_LIMIT:" + str(GITHUB_LIMIT))
        new_readme = social.generate_github(
            GITHUB_NAME, GITHUB_LIMIT, new_readme, time_zone=tz
        )

    if new_readme == old_readme:
        print("nothing changed")
    else:
        print("readme change, start update...")
        repo.update_file(
            path=contents.path,
            message=COMMIT_MESSAGE,
            content=new_readme,
            sha=contents.sha,
        )
        print("your readme update completed!")
