#!/usr/bin/env python3

from . import __app_name__, logger
import io, json, time
from pathlib import Path
from bs4 import BeautifulSoup as bs
import requests as req
import typer  # type: ignore

app = typer.Typer(name='jwc-news')

jwc_url = 'http://www.jwc.fudan.edu.cn'
jwc_news_url = 'http://www.jwc.fudan.edu.cn/9397/list.htm'
cache_dir = Path.home() / '.cache' / __app_name__
cache_file = cache_dir / 'data.json'


def jwc_get_latest_news_from_news_url() -> dict[int, dict[str, str]]:
    """
    get news from the jwc's news website
    date is available on that site
    """
    jwc = req.get(jwc_news_url)
    jwc.encoding = 'utf-8'
    jwc_html = jwc.text
    jwc_soup = bs(jwc_html, 'html.parser')

    result = {}
    for i in range(1, 15):
        # there are 8 items in the news section.
        news_elem = jwc_soup.select(f'#wp_news_w14 tr:nth-child({i}) a')[0]
        # news_date: 2020-01-01
        # date: 01-01
        news_date = jwc_soup.select(
            f'tr:nth-child({i}) tr td + td')[0].text.strip()
        date_list = news_date.split('-')
        date = '-'.join(date_list[1:3])
        result[i] = {
            # 'news': news_elem['title'],
            'news': f'{date} {news_elem.text.strip()}',
            'link': jwc_url + news_elem['href']  # type: ignore
        }
    return result


def update_cache():
    """
    example json cache:
    {
        "last_updated_at": 1651331622,
        "1": {
            "news": "2020-01-01 新闻标题",
            "link": "http://www.jwc.fudan.edu.cn/9397/list.htm"
        },
        "2": {
            "news": "2020-01-01 新闻标题",
            "link": "http://www.jwc.fudan.edu.cn/9397/list.htm"
        }
    }
    """
    logger.info('updating cache...')
    cache_dir.mkdir(exist_ok=True)
    cache = {}
    cache.update(last_updated_at=int(time.time()))
    cache.update(jwc_get_latest_news_from_news_url())
    with io.open(cache_file, 'w', encoding='utf-8') as f:
        json.dump(cache, f, ensure_ascii=False, indent=4)


def check_if_cache_expired(expiration: int) -> bool:
    if not cache_file.exists():
        return True
    with io.open(cache_file, 'r', encoding='utf-8') as f:
        cache = json.load(f)
    if 'last_updated_at' not in cache:
        return True
    return int(time.time()) - cache['last_updated_at'] > expiration


def read_cache_content(limit: int = 14) -> str:
    logger.info('reading cache...')
    with io.open(cache_file, 'r', encoding='utf-8') as f:
        cache = json.load(f)
    out = io.StringIO()
    for i in range(1, limit + 1):
        print(cache[str(i)]['news'], file=out)
        print(cache[str(i)]['link'], file=out)
        if i < limit:
            print(file=out)
    return out.getvalue()


@app.command()
def jwc_news(
    limit: int = typer.Option(14,
                              '--limit',
                              '-l',
                              help='limit the number of news',
                              max=14),
    output: Path = typer.Option(None,
                                '--output',
                                '-o',
                                help='output file, default is stdout'),
    force_update: bool = typer.Option(
        False,
        '--force-update',
        '-f',
        help='do not use cache and force update'),
) -> None:
    if force_update or check_if_cache_expired(expiration=60 * 60 * 12):
        update_cache()
    out = read_cache_content(limit=limit)
    if output is None:
        print(out)
    else:
        output.write_text(out)


def main() -> None:
    app()


if __name__ == '__main__':
    main()
