import datetime
import re
import pytz
import feedparser

BLOG_START_COMMENT = "<!-- START_SECTION:blog -->"
BLOG_END_COMMENT = "<!-- END_SECTION:blog -->"

DOUBAN_START_COMMENT = "<!-- START_SECTION:douban -->"
DOUBAN_END_COMMENT = "<!-- END_SECTION:douban -->"

GITHUB_START_COMMENT = "<!-- START_SECTION:github -->"
GITHUB_END_COMMENT = "<!-- END_SECTION:github -->"

douban_emoji = {
    "在看": "👀",
    "看过": "😎",
    "想看": "🤔",
    "想听": "🎈",
    "听过": "😋",
    "在听": "🎧",
}

douban_star = {
    "力荐": "⭐⭐⭐⭐⭐",
    "推荐": "⭐⭐⭐⭐",
    "还行": "⭐⭐⭐",
    "较差": "⭐⭐",
    "很差": "⭐",
}

github_activity = {
    "PushEvent": "📌",
    "CreateEvent": "📁",
    "WatchEvent": "⭐",
    "ForkEvent": "🍴",
    "IssuesEvent": "📝",
    "PullRequestEvent": "📦",
    "ReleaseEvent": "🎉",
    "CommitCommentEvent": "💬",
    "DeleteEvent": "🗑",
    "DownloadEvent": "📁",
    "FollowEvent": "👤",
    "GistEvent": "📝",
    "IssueCommentEvent": "💬",
    "PublicEvent": "📝",
}


def generate_blog(
    rss_link,
    limit,
    readme,
    time_format="%a, %d %b %Y %H:%M:%S %z",
    time_zone=pytz.timezone("Asia/Shanghai"),
) -> str:
    """Generate blog"""
    entries = feedparser.parse(rss_link)["entries"]

    # get the latest $limit items sorted by published date
    arr = [
        {
            # "title": (entry["title"][0:20] + "...") if(len(entry["title"]) > 22) else entry["title"],
            "title": entry["title"],
            "url": entry["link"].split("#")[0],
            "published": format_time(
                entry["published"], time_format=time_format, time_zone=time_zone
            ),
        }
        for entry in entries
    ]

    arr = sorted(arr, key=lambda x: x["published"], reverse=True)
    arr = arr[:limit]

    content = "\n".join(
        [
            "| {published} | <a href='{url}' target='_blank'>{title}</a> |".format(
                **item
            )
            for item in arr
        ]
    )

    content = "| Date | Title |\n| :-: | :---: |\n" + content

    return generate_new_readme(BLOG_START_COMMENT, BLOG_END_COMMENT, content, readme)


def generate_douban(
    username,
    limit,
    readme,
    time_format="%a, %d %b %Y %H:%M:%S %Z",
    time_zone=pytz.timezone("Asia/Shanghai"),
) -> str:
    """Generate douban"""
    entries = feedparser.parse(
        "https://www.douban.com/feed/people/" + username + "/interests"
    )["entries"]
    arr = [
        {
            "title": item["title"],
            "url": item["link"].split("#")[0],
            "published": format_time(
                item["published"], time_format=time_format, time_zone=time_zone
            ),
            "desc": item["description"],
        }
        for item in entries[:limit]
    ]

    content = "\n".join(
        [
            f"| {item['published']} | {item['title'][:2]}{get_emoji(item['title'][:2])} "
            f"<a href='{item['url']}' target='_blank'>{item['title'][2:]}</a> {get_star(item['desc'])} |"
            for item in arr
        ]
    )

    content = "| Date | Title |\n| :-: | :---: |\n" + content

    return generate_new_readme(
        DOUBAN_START_COMMENT, DOUBAN_END_COMMENT, content, readme
    )


def generate_github(
    username: str,
    limit: int,
    readme: str,
    time_format='"%Y-%m-%dT%H:%M:%SZ"',
    time_zone=pytz.timezone("Asia/Shanghai"),
) -> str:
    """Generate github"""
    entries = feedparser.parse("https://github.com/" + username + ".atom")["entries"]
    # print(entries)
    print(limit, type(limit))
    arr = [
        {
            "title": item["title"],
            "url": item["link"],
            "tag": item["id"].split(":")[-1].split("/")[0],
            "published": item["published"].split("T")[0],
        }
        for item in entries[:limit]
    ]

    print(arr)

    content = "\n".join(
        [
            f"| {item['published']} | {' '.join(item['title'].split(' ')[1:-1])} "
            f"{get_activity_emoji(item['tag'])} [{item['title'].split(' ')[-1]}]({item['url']}) |"
            for item in arr
        ]
    )

    content = "| Date | Title |\n| :-: | :---: |\n" + content

    return generate_new_readme(
        GITHUB_START_COMMENT, GITHUB_END_COMMENT, content, readme
    )


def generate_new_readme(
    start_comment: str, end_comment: str, content: str, readme: str
) -> str:
    """Generate a new Readme.md"""
    pattern = f"{start_comment}[\\s\\S]+{end_comment}"
    repl = f"{start_comment}\n{content}\n{end_comment}"
    if re.search(pattern, readme) is None:
        print(
            f"can not find section in your readme, please check it, it should be {start_comment} and {end_comment}"
        )

    return re.sub(pattern, repl, readme)


def get_activity_emoji(tag: str) -> str:
    """Get activity emoji"""
    return github_activity.get(tag, "")


def get_emoji(title: str) -> str:
    """Get emoji for title"""
    if title[:2] in douban_emoji:
        return douban_emoji[title[:2]]
    return ""


def get_star(description: str) -> int:
    pattern = r"<p>推荐: (n|.)*</p>"
    if re.search(pattern, description) is None:
        return ""
    star = re.search(pattern, description).group(0).split(": ")[1].split("</p>")[0]
    return douban_star[star]


def format_time(
    timestamp,
    time_format="%a, %d %b %Y %H:%M:%S %z",
    time_zone=pytz.timezone("Asia/Shanghai"),
) -> datetime:
    try:
        date_str = datetime.datetime.strptime(timestamp, time_format)
    except Exception as e:
        print(e)
        return timestamp
    date_str = date_str.replace(tzinfo=time_zone)
    return date_str.date()
