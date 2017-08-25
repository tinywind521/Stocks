from django.http import HttpResponse


def hello(request):
    returnValue = '<!DOCTYPE html>' \
                  '<html>' \
                    '<head>' \
                        '<meta charset="utf-8">' \
                        '<title>道法自然</title>' \
                    '</head>' \
                    '<body>' \
                        '<h1>道法自然</h1>' \
                        '<p>Hello world ! </p>' \
                        '<p>Hello fromgc ! </p>' \
                        '<br>' \
                        '<img alt="" src="http://image.sinajs.cn/newchart/min/n/sh000001.gif"></img>' \
                        '<img alt="" src="http://image.sinajs.cn/newchart/daily/n/sh000001.gif"></img>' \
                  '</body>' \
                  '</html>'
    return HttpResponse(returnValue)
