import time

from http_api import hkex_request


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
    bodys = {'__VIEWSTATE': 'onZZDwBRCYdbXKyKg497ArWTTn1CmhmBjj27%2FdsrM6HNek5itqJOsCeN02776VyFDH%2F5al9cL91EofyTlpTzhILdCmCCeHzDRlXS2HM1QP97%2B4ZPJdUKhWfgbGIKswICw%2BCvzgrlWGtR8fSuTnp%2BGftjStSZucGQwbhbXtTC0bdM3EKnm5hf%2FgVTZkVzF5rCAazMeA%3D%3D',
             '__VIEWSTATEGENERATOR': 'EC4ACD6F',
             '__EVENTVALIDATION': 'B8c%2BhcQ6GFYUzBV%2F403wBajaTt7GUYy%2FTHlO12E%2FMwCyt3Jt6Iv8DWDc2KeFNd6Fpa%2BCgqrBNiOJ8jEtkXJTshoSotb%2FJ5xlS0ZJ0ULttyOnf3dI3Axmr8weh1nrAbYQJGG5URVWp8V27h5R%2BVD3%2BosZyXhTKrYQ2GFy8bhUdAlcfpAF1WEW6DFygZAOmrqGTsAFoaeQt%2F%2FDOxLlZ7ZAtUQw3x6AqBOH%2FieCvmbavg6bwh9GQGwza4qFwjAH0UEDcxCz%2FvRaF4lCJQgQq53w4PRm%2BlTURbA4kVttL3UZy%2B09zqh%2F1NJmK5cU1fRlvsO6SlpKhOupzXQXfd9rwVMlxTMoDB6Wz5A551oRKC0SWfjUWRLNEYcDH8a8BibVvJcCEoSAyncPt9IALjVT9SSgev0pFVSMxtxHU17kDdhIe6WtYEWDJNjjlrhFDuUVdjFke5u51pArdN4B4WlwPmSzviBOk3m3YaJEXAPQS4m1mAu6RF0POampgKbAEl4GCTxV%2FrRevVSEsjZwpyVAqkdzTqu6Eotz48hlb5B2mYSdEpCrsG7QgHre0lIOsN1K%2Bb6LUQYfTE4y6s55zjTAFYPdEmDY5ZmICnYo9kC9Msk2M8wQvddnQpprJc6GybmJBMaTZJEG58dYaObzW2qgI3hYCyPV%2BtpTF0GUQtaxIFxS9qJJ3v1POf2rdmkY1vfkK%2F2Rq7A3HkgtUj%2B2%2FhAYE7q7%2B%2FWza%2FZd4yWbUfv20hR9AqTW1LdhnN2dV4RbQ%2FkR1DQQgoHV4PDtfek0DJ55b5SNc88j%2FYtQjR0QpIRkg0CL2mpcxSE52eK%2BZ9Qit8%2FYDogg7e6t5Xahp9NMBa2jcwKJn0uxVK1k7X%2BH8FzVakuri06zvuPtbVt%2Bw%2BHNa7NalArtgLcshdmg2d91kPxdE3F4%2BS9CdBmi4x4%2BHf%2B4GdvExF6saYAtheifj7Pk8r8CykQDvatbREaYNEJjz5W7dltwKVIg5rSZOAXsbYobEmadhbMEzesy2Km4la%2FF%2Fly%2F4LQEUyvufltmvxfFhS5%2BDi1bwde9lmlegkOGeqlHxkK0MAhcU4f3WRoAvHzpo6Y9vFaiDPHIX8tFeP9Mt%2F5VFlY38yUwMyfHVh9CZqCS%2Bt9mNvcWIIRPdugsH9hDdV3k4tD840DNoq9AhcIuW2CSNXrGiPCODio%3D',
             'today': '20170317',
             'sortBy': '',
             'alertMsg': '',
             'ddlShareholdingDay': date[6:8],
             'ddlShareholdingMonth': date[4:6],
             'ddlShareholdingYear': date[0:4],
             'btnSearch.x': '24',
             'btnSearch.y': '4',
             }

    url = host

    content = hkex_request.req(url, bodys, Referer)
    time.sleep(1)
    return content
