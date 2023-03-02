#!/usr/bin/env python
# -*- encoding: utf-8 -*-
""" 
@File    :   tests\test_github.py 
@Time    :   2021-12-10 17:29:16 
@Author  :   Bingjie Yan 
@Email   :   bj.yan.pa@qq.com 
@License :   Apache License 2.0 
"""

import social
import pytz


class TestGitHub(object):
    def test_generate_github(self):
        GITHUB_NAME = "beiyuouo"
        GITHUB_LIMIT = 5
        TIME_ZONE = "Asia/Shanghai"
        tz = pytz.timezone(TIME_ZONE)

        old_readme = (
            social.GITHUB_START_COMMENT + "old_content" + social.GITHUB_END_COMMENT
        )
        new_readme = old_readme

        print("GITHUB_NAME:" + GITHUB_NAME)
        print("GITHUB_LIMIT:" + str(GITHUB_LIMIT))
        new_readme = social.generate_github(
            GITHUB_NAME, GITHUB_LIMIT, new_readme, time_zone=tz
        )
        print("new_readme:")
        print(new_readme)
        assert old_readme != new_readme
        # assert 1 == 0
