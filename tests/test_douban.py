#!/usr/bin/env python
# -*- encoding: utf-8 -*-
""" 
@File    :   tests\test_douban.py 
@Time    :   2021-12-10 17:29:38 
@Author  :   Bingjie Yan 
@Email   :   bj.yan.pa@qq.com 
@License :   Apache License 2.0 
"""

import social
import pytz


class TestDouban(object):
    def test_generate_douban(self):
        DOUBAN_NAME = "179948994"
        DOUBAN_LIMIT = 5
        TIME_ZONE = "Asia/Shanghai"
        tz = pytz.timezone(TIME_ZONE)

        old_readme = (
            social.DOUBAN_START_COMMENT + "old_content" + social.DOUBAN_END_COMMENT
        )
        new_readme = old_readme

        print("DOUBAN_NAME:" + DOUBAN_NAME)
        print("DOUBAN_LIMIT:" + str(DOUBAN_LIMIT))
        new_readme = social.generate_douban(
            DOUBAN_NAME, DOUBAN_LIMIT, new_readme, time_zone=tz
        )
        print("new_readme:")
        print(new_readme)
        assert old_readme != new_readme
        # assert 1 == 0
