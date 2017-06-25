import urllib.request
import urllib.error
import time
import sys
import ssl


def req(url):
    content = ''
    try:
        try:
            request = urllib.request.Request(url)
            # 由于使用了urllib.request，Request需要大写
            # request.add_header('Authorization', 'APPCODE ' + appcode)
            # ctx = ssl.create_default_context()
            # ctx.check_hostname = False
            # ctx.verify_mode = ssl.CERT_NONE
            response = urllib.request.urlopen(request)
            temp = response.read()
            content = temp.decode("GBK")
            # print(content)
            if content:
                return content
            else:
                return ''
        except ValueError or TimeoutError or urllib.error.URLError:
            print(url)
            try:
                print('QQ_request.req Error! Time sleep 5S!')
                time.sleep(5)
                request = urllib.request.Request(url)
                # 由于使用了urllib.request，Request需要大写
                # request.add_header('Authorization', 'APPCODE ' + appcode)
                # ctx = ssl.create_default_context()
                # ctx.check_hostname = False
                # ctx.verify_mode = ssl.CERT_NONE
                response = urllib.request.urlopen(request)
                temp = response.read()
                content = temp.decode("GBK")
                # print(content)
                if content:
                    return content
                else:
                    return ''
            except ValueError or TimeoutError or urllib.error.URLError:
                return ''
    finally:
        return content
