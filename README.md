# readme-action

## How to use

A simple example.

```yaml
- uses: beiyuouo/readme-action@main
    with:
    blog_rss_link: https://blog.bj-yan.top/index.xml
    douban_name: 179948994
```

A full example.

```yaml
name: Build Readme

on:
  schedule:
    - cron: "0 0 * * *"
  workflow_dispatch:
  push:
    branches: [main]

jobs:
  update-social:
    runs-on: ubuntu-latest
    steps:
      - uses: beiyuouo/readme-action@main
        with:
          blog_rss_link: https://blog.bj-yan.top/index.xml
          blog_limit: 5
          blog_time_format: "%a, %d %b %Y %H:%M:%S %z"
          douban_name: 179948994
          douban_limit: 5
          commit_message: Updated README Profile by readme action
          time_zone: "Asia/Shanghai"
```

# Reference

- Thanks to [zylele](https://github.com/zylele/social-readme) for their great work.