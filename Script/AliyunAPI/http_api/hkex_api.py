#   import urllib.request
#   import sys
#   import ssl

from http_api import hkex_request
from functions import function, getValue


def hkex(date, index):
    """
    获取hkex数据。
    :param date:
    :param index:
    :return:
    """
    a = date
    host = 'http://www.hkexnews.hk/sdw/search/mutualmarket_c.aspx?t=' + index
    Referer = 'http://www.hkexnews.hk/sdw/search/mutualmarket_c.aspx?t=' + index
    # path = '/timeline'
    method = 'GET'
    bodys = {'__VIEWSTATE': 'NbjyN0qT%2Bs6TAkkRZX2Xq2DY4Cj%2BMucdH8BIprboyRv2OjeFEjj%2BikaecTF8wZ%2F%2F1exwHz6Ar1ysWWzFydDaem8A7YcTPQwOEkdG4KlY%2Bt1nVEfwYi6VV5XaSIeAjRpwGcpYYwssdCaCnuq8zeodFzzw4y%2FT8vfgGWBBC86K4bB%2FQnM1Q%2FY2xJmX%2BMmpD8yzw6c8Kg%3D%3D',
             '__VIEWSTATEGENERATOR': 'EC4ACD6F',
             '__EVENTVALIDATION': 'tjnxSRuWaTZ4s5VyGZn%2BAHLf5GwczctSd0HvyKkwSptbzumTFpT3DblXGPf%2Bz1VdkBLV9HocIcb0jqmdm2Q2DRczgjaPq0k6uBTY4zgC1fDXR9MxdyqZUbErVS%2Fev4xOnulMEq4mi27oY3CVquYkwD%2FiIMMAXI%2FxHuggx1W1TAjKL7%2FAB7nbtZgHfSXFYV8wSAvdjCH9Mcq2slKuheEFpsYPkvAfHxTHDW7Jd7NJGXz%2BXq8%2B7OvzZi5x0wv6KO2qi30YlBLDJsp6MVDPY%2B1E61NCjeOKqVt6d59cCNRLKK%2BffBlVDlqYpLu%2Fjgl91PkkhA0WorfUO7Gh%2F0kIZRsWuJ62EABkl21qa7tHsLxa%2B%2BwP9573x66B%2FjLMxeV%2BfyF4HaKzrxQ%2BQsy%2F7PrAWv868UC3%2BVA2m7SCkutsOTraCXvJj3K20i2NQxabA8n4BHoSN%2B23gGidzGhXSiBCPbH0n06Cb9lZHkcFZ4HGBRjyyuFZ5YwKpyb%2FcHrI5Y0VsGYResCwDlchj3CMfBy7ZXwZJ%2BV6KInF03fjjTCbDchJnARf7JKVGqdjMT2My1fJKfgpINUPuvXl2u1keuTjjGTl5BVAtJDTvy%2B5zrotvyexfOk8xroduhYRrgVKHb1M4QDnm7WxLHhyLtzV5b8C%2ByTBP%2B3fB50O5Ymj%2BWx%2FTTjYde%2B%2BNyhKhXb6tIIKJv25ILNEIUuHr2ht0FAY1glYkHyU1NBeSyWrFiEm9ganQ5kbSuvsqyeTV3qveApgtqMRnw8vZwQhJlAnuEPOVJDvQsu9kswNdYilFCzM2KBcGcDYiaXO6wnTp3IPUWU10oJ9y6jRvLxkdCmzRB2L1Ini4otYRkziy%2FvQcA2zR3Sa%2BzV3GbQgMhVyu6JvaUv4JxrbKmzw3avlmtuBRPKjE1t6lFx8UAAOl2T2qdU8HU%2FOoChxkkjgUVdDYj6AkTWBvpotGEmZ2byHRqRCZL2mkf20OWMfXgN%2Fpt2%2FXkp0gFbKudsRoyTHaV115Mv99jyCTWChlkKOdbw6PR2zFaKGpcgZiCI3MEvmn6J%2BBfjpxAa8U9qqU6j98d%2Brrp4rNE557Nq8yrZHUGKE9Ho3BugoUHztRvUQrHSICUBPrfzZvV5M3oXjfYcO5tl1l35zh9KnUTJDCAyJ0svAQkLA%2FMiIRZCFzT160OB%2FTes%3D',
             'today': '20170628',
             'sortBy': '',
             'alertMsg': '',
             'ddlShareholdingDay': date[6:8],
             'ddlShareholdingMonth': date[4:6],
             'ddlShareholdingYear': date[0:4],
             'btnSearch.x': '37',
             'btnSearch.y': '6',
             }

    url = host

    content = hkex_request.req(url, bodys, Referer)
    return content
