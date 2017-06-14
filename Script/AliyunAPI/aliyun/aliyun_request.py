import urllib.request
import sys
import ssl


def req(url, appcode):

    try:
        request = urllib.request.Request(url)
#   由于使用了urllib.request，Request需要大写

        request.add_header('Authorization', 'APPCODE ' + appcode)
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        response = urllib.request.urlopen(request, context=ctx)
        content = response.read().decode("utf-8")

        if content:
            return content
        else:
            return None

    except ValueError:
        return None
