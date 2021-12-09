import datetime
import re
import pytz
import feedparser

BLOG_START_COMMENT = '<!-- START_SECTION:blog -->'
BLOG_END_COMMENT = '<!-- END_SECTION:blog -->'

DOUBAN_START_COMMENT = '<!-- START_SECTION:douban -->'
DOUBAN_END_COMMENT = '<!-- END_SECTION:douban -->'


def generate_blog(
    rss_link,
    limit,
    readme,
    time_format='%a, %d %b %Y %H:%M:%S %z',
    time_zone=pytz.timezone('Asia/Shanghai')) -> str:
    """Generate blog"""
    entries = feedparser.parse(rss_link)["entries"]
    # print(entries)
    arr = [
        {
            # "title": (entry["title"][0:20] + "...") if(len(entry["title"]) > 22) else entry["title"],
            "title":
            entry["title"],
            "url":
            entry["link"].split("#")[0],
            "published":
            format_time(entry["published"], time_format=time_format, time_zone=time_zone),
        } for entry in entries[:limit]
    ]

    content = "\n".join([
        "| {published} | <a href='{url}' target='_blank'>{title}</a> |".format(**item)
        for item in arr
    ])

    content = "| Date | Title |\n| :-: | :---: |\n" + content

    return generate_new_readme(BLOG_START_COMMENT, BLOG_END_COMMENT, content, readme)


def generate_douban(
    username,
    limit,
    readme,
    time_format='%a, %d %b %Y %H:%M:%S %Z',
    time_zone=pytz.timezone('Asia/Shanghai')) -> str:
    """Generate douban"""
    entries = feedparser.parse("https://www.douban.com/feed/people/" + username +
                               "/interests")["entries"]
    arr = [{
        "title":
        item["title"],
        "url":
        item["link"].split("#")[0],
        "published":
        format_time(item["published"], time_format=time_format, time_zone=time_zone),
    } for item in entries[:limit]]

    content = "\n".join([
        f"| {item['published']} | {item['title'][:2]}  <a href='{item['url']}' target='_blank'>{item['title'][2:]}</a> |"
        for item in arr
    ])

    content = "| Date | Title |\n| :-: | :---: |\n" + content

    return generate_new_readme(DOUBAN_START_COMMENT, DOUBAN_END_COMMENT, content, readme)


def generate_new_readme(start_comment: str, end_comment: str, content: str, readme: str) -> str:
    """Generate a new Readme.md"""
    pattern = f"{start_comment}[\\s\\S]+{end_comment}"
    repl = f"{start_comment}\n{content}\n{end_comment}"
    if re.search(pattern, readme) is None:
        print(
            f"can not find section in your readme, please check it, it should be {start_comment} and {end_comment}"
        )

    return re.sub(pattern, repl, readme)


def format_time(timestamp,
                time_format='%a, %d %b %Y %H:%M:%S %z',
                time_zone=pytz.timezone('Asia/Shanghai')) -> datetime:
    try:
        date_str = datetime.datetime.strptime(timestamp, time_format)
    except Exception as e:
        print(e)
        return timestamp
    date_str = date_str.replace(tzinfo=time_zone)
    return date_str.date()