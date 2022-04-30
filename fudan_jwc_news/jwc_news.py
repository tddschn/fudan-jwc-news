#!/usr/bin/env python3

# import sys
# from icecream import ic

# ic(sys.path)
from bs4 import BeautifulSoup as bs
import requests as req
import sys

jwc_url = 'http://www.jwc.fudan.edu.cn'
jwc_news_url = 'http://www.jwc.fudan.edu.cn/9397/list.htm'


def jwc_get_latest_news_from_news_url() -> dict:
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


def jwc_get_latest_news_from_main_site() -> dict:
    """
    get news from the jwc's main website
    date is not available on that site
    """
    jwc = req.get(jwc_url)
    jwc.encoding = 'utf-8'
    jwc_html = jwc.text
    jwc_soup = bs(jwc_html, 'html.parser')

    result = {}
    for i in range(1, 9):
        # there are 8 items in the news section.
        news_elem = jwc_soup.select(f'#wp_news_w45 tr:nth-child({i}) a')[0]
        result[i] = {
            # 'news': news_elem['title'],
            'news': news_elem.text,
            'link': jwc_url + news_elem['href']  # type: ignore
        }
    return result


def main(limit=14, file=sys.stdout, end='\n') -> None:
    print_kwargs = {'file': file, 'end': end}
    if not isinstance(limit, int):
        limit = 7
    elif limit > 14:
        limit = 14
    result = jwc_get_latest_news_from_news_url()
    # return result
    for i in range(1, limit):
        print(result[i]['news'], **print_kwargs)
        print(result[i]['link'], **print_kwargs)

        if i < limit - 1:
            print(**print_kwargs)


if __name__ == '__main__':
    main(limit=14)
