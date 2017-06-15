import urllib.request
import sys
import ssl


def req(url, appcode):
    """
    aliyun API
    :param url:
    :param appcode:
    :return:
    """
    try:
        request = urllib.request.Request(url)

        request.add_header('Authorization', 'APPCODE ' + appcode)
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        try:
            response = urllib.request.urlopen(request, context=ctx)
        except urllib.error.HTTPError or urllib.error.URLError or TimeoutError:
            response = None
        content = response.read().decode("utf-8")
        if content:
            return content
        else:
            return None
    except ValueError:
        return None
