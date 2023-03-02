import social
import pytz


class TestBlog(object):
    def test_generate_blog(self):
        BLOG_RSS_LINK = "https://blog.bj-yan.top/index.xml"
        BLOG_LIMIT = 5
        TIME_FORMAT = "%a, %d %b %Y %H:%M:%S %z"
        TIME_ZONE = "Asia/Shanghai"
        tz = pytz.timezone(TIME_ZONE)

        old_readme = social.BLOG_START_COMMENT + "old_content" + social.BLOG_END_COMMENT
        new_readme = old_readme

        print("BLOG_RSS_LINK:" + BLOG_RSS_LINK)
        print("BLOG_LIMIT:" + str(BLOG_LIMIT))
        new_readme = social.generate_blog(
            BLOG_RSS_LINK, BLOG_LIMIT, new_readme, time_format=TIME_FORMAT, time_zone=tz
        )
        print("new_readme:")
        print(new_readme)
        assert old_readme != new_readme
        # assert 1 == 0
