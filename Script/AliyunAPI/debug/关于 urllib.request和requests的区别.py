from bs4 import BeautifulSoup
import urllib.request
import requests

url = "http://finance.qq.com/gdyw.htm"

# 使用urllib.request的代码：
html = urllib.request.urlopen(url).read()
html = html.decode('gb2312', errors='ignore')
soup1 = BeautifulSoup(html, 'lxml')
lfls1 = str(soup1).split('<!-- 左侧列表 -->', 2)

# 使用requests的代码：
response = requests.get(url)
soup2 = BeautifulSoup(response.text, 'lxml')
lfls2 = str(soup2).split('<!-- 左侧列表 -->', 2)

print(lfls1[1][:500])
print('='*70)
print(lfls2[1][:500])



"""

Python中的urllib.request模块

Python 3.x版本后的urllib和urllib2


在Python 3以后的版本中，urllib2这个模块已经不单独存在（也就是说当你import urllib2时，系统提示你没这个模块），urllib2被合并到了urllib中，
叫做urllib.request 和 urllib.error 。
urllib整个模块分为urllib.request, urllib.parse, urllib.error。

例： 
其中urllib2.urlopen()变成了urllib.request.urlopen() 
urllib2.Request()变成了urllib.request.Request()

urllib和urllib2模块之间的区别

在python中，urllib和urllib2不可相互替代的。
整体来说，urllib2是urllib的增强，但是urllib中有urllib2中所没有的函数。
urllib2可以用urllib2.openurl中设置Request参数，来修改Header头。如果你访问一个网站，想更改User Agent（可以伪装你的浏览器），你就要用urllib2.
urllib支持设置编码的函数，urllib.urlencode,在模拟登陆的时候，经常要post编码之后的参数，所以要想不使用第三方库完成模拟登录，你就需要使用urllib。

urllib一般和urllib2一起搭配使用
urllib- - - - - - URL处理模块

源代码:Lib / urllib /

urllib是一个包,收集几个模块来处理网址:
urllib.request打开和浏览url中内容 
urllib.error包含从 urllib.request发生的错误或异常 
urllib.parse解析url 
urllib.robotparser解析 robots.txt文件

urllib.request
urllib.request — 为打开url提供的可扩展类库
源代码:Lib / urllib / request.py
urllib.request模块定义了方法和类,帮助打开url(主要是HTTP)在一个复杂的世界——基本和摘要式身份验证,重定向,cookies等等。

————-urllib.request模块定义了以下功能：—————–

urllib.request.urlopen()
urllib.request.urlopen(url, data=None, [timeout, ]*, cafile=None, capath=None, cadefault=False, context=None)
打开网址URL,这可以是一个字符串或一个 Request对象。
数据必须是一个字节对象指定额外的数据发送到服务器或 None。如果没有这样的数据是必要的，数据也可能是一个iterable对象而且在这种情况下必须在最开始时指定内容的长度。
目前HTTP是唯一一个这样请求数据的，当数据参数被提供时，HTTP请求将会执行POST请求而不是GET请求。
数据应该是一个缓冲的在标准应用程序中以 x-www-form-urlencoded的格式。 urllib.parse.urlencode()函数接受一个映射或序列集合,并返回一个ASCII文本字符串的格式。
它应该在被用作数据参数之前，被编码为字节。

urllib.request 模块 使用 HTTP/1.1协议，并且包括请求 Connection:close在HTTP请求头。
可选的第二个超时参数timeout，用于阻塞操作,比如连接请求(如果未指定,全球将使用默认超时设置)。这实际上只适用于HTTP、HTTPS和FTP连接。
如果context被指定，它必须是一个 ssl.SSLContext实例描述各种SSL选项。点击HTTPSConnection查看更多细节。
可选cafile和capath参数指定一组被HTTPS请求信任的CA证书。cafile应该指向一个文件包含CA证书的包,而capath应该指向一个散列的证书文件的目录。
点击ssl.SSLContext.load_verify_locations()查看更多的信息。

cadefault参数被忽略。
这个函数始终返回一个对象，像context（上下文） 管理者并提供这些方法

geturl()——返回URL的资源检索,常常重定向之后使用
info()——返回页面的元信息,如标题，组成 email.message_from_string(的)实例(见快速参考HTTP头)
getcode()——返回响应的HTTP状态代码。

为HTTP和HTTPS url，这个函数返回的一个 http.client.HTTPResponse对象略有不同。除了上面的三种新方法中，
这个message属性包含相同的信息像reason属性——由服务器返回的原因——而不是响应头,因为它在文档中指定 HTTPResponse。
FTP、文件和数据请求url和显式地处理 URLopener和 FancyURLopener类，这个函数返回一个 urllib.response.addinfourl对象。

urllib.request.urlopen()会在 URLError中抛出协议错误。
请注意,，可能返回None，这在没有处理程序处理请求(尽管全球默认安装 OpenerDirector并使用 UnknownHandler以确保这不会发生)时发生。
此外，如果检测到代理设置(例如,当一个 *_proxy环境变量如 http_proxy已经被设定),，ProxyHandler默认安装并确保请求都通过代理来处理。
遗留的 urllib.urlopen从Python 2.6和更早已经被中断;；urllib.request.urlopen()对应于旧的 urllib2.urlopen。
代理处理,是通过字典参数完成的 urllib.urlopen可以使用 ProxyHandler对象。

3.2版本的变化：cafile和capath被补充。
3.2版本的变化：如果可能的话，现在支持HTTPS虚拟主机(也就是说，如果 ssl.HAS_SNI是真的)。

在新的3.2版本：数据可以是一个iterable对象。
3.3版本的变化：cadefault被补充。
3.4.3版本的变化：context被补充。

urllib.request.install_opener(opener)
安装一个 OpenerDirector实例作为全球默认的opener 。安装一个opener 必要的,如果你想让urlopen使用这个opener ;
否则,简单地调用 OpenerDirector.open()而不是 urlopen()。这样代码不会检查一个真实的 OpenerDirector并且任何类的适当的接口都可以运作。

urllib.request.build_opener([handler, …])
返回一个顺序的链的处理程序 OpenerDirector的实例。处理程序可以是BaseHandler的实例,或者 BaseHandler的子类(在这种情况下,必须调用没有参数的构造函数)。
下面这些类的实例将提前处理程序,除非处理程序包含它们，或者它们子类的实例：ProxyHandler(如果检测到代理设置), 
UnknownHandler, HTTPHandler, HTTPDefaultErrorHandler, HTTPRedirectHandler, FTPHandler, FileHandler, HTTPErrorProcessor.
如果Python安装SSL支持(即如果 ssl模块可以被导入)， HTTPSHandler也将被添加。
一个 BaseHandler子类也可以通过改变它的 handler_order属性来修改它再处理程序列表中的位置。

urllib.request.pathname2url(path)
将路径名转换成路径，从本地语法形式的路径中使用一个URL的路径组成部分。这不会产生一个完整的URL。它将返回引用 quote()函数的值。

urllib.request.url2pathname(path)
将路径组件转换为本地路径的语法。这个不接受一个完整的URL。这个函数使用 unquote()解码的通路。

urllib.request.getproxies()
这个helper函数返回一个日程表dictionary 去代理服务器的URL映射。扫描指定的环境变量 _proxy大小写不敏感的方法,对所有的操作系统，当它不能找到它，
从Mac OS X的Mac OSX系统配置和Windows系统注册表中寻找代理信息。如果两个大写和小写环境变量存在(或不一样)，小写优先。

请注意，如果环境变量 REQUEST_METHOD已被设置,这通常表明你在CGI脚本运行环境,此时环境变量 HTTP_PROXY(大写 _PROXY)将被忽略。
这是因为该变量可以被客户端使用注射“代理:”HTTP头。如果你需要使用一个HTTP代理在CGI环境中,要么使用 ProxyHandler明确,或者确保变量名小写(或至少是 _proxy后缀)。

——提供以下类：—————————————

类 urllib.request.Request(url, data=None, headers={}, origin_req_host=None, unverifiable=False, method=None)
这个类是一个抽象的URL请求。
url应该是一个字符串包含一个有效的url。
数据必须是一个字节对象指定额外的数据发送到服务器或 None。如果没有这样的数据是必要的，数据也可能是一个iterable对象而且在这种情况下必须在最开始时指定内容的长度。
目前HTTP是唯一一个这样请求数据的，当数据参数被提供时，HTTP请求将会执行POST请求而不是GET请求。

数据应该是一个缓冲的在标准应用程序中以 x-www-form-urlencoded的格式。 urllib.parse.urlencode()函数接受一个映射或序列集合,并返回一个ASCII文本字符串的格式。
它应该在被用作数据参数之前，被编码为字节。
headers 应该是一个字典，如果 add_header()被称为与每个键和值作为参数。这通常是用来“恶搞” User-Agent头的值，
因为使用一个浏览器识别本身——一些常见HTTP服务器只允许请求来自浏览器而不是脚本。
例如，Mozilla Firefox可能识别本身 “Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11”。
而 urllib默认的用户代理字符串 是”Python-urllib/2.6”在Python 2.6（）。

一个Content-Type header的例子 用数据论证将发送一个字典 {“Content-Type”:”application/x-www-form-urlencoded”}。
最后两个参数只是正确处理第三方HTTP cookie：
origin_req_host应该请求原始的主机交易，就像定义的RFC 2965。它默认为 http.cookiejar.request_host(self)。
这是原始请求的主机名或IP地址，由用户发起。例如。如果请求是一个图像在HTML文档中，这应该是请求的请求主机包含图像的页面。

无法核实的表明是否应该请求是无法核实的，这由RFC 2965定义。它默认为 False。一个无法核实的请求的URL的用户没有允许的选择。
例如，如果请求是一个图像在一个HTML文档,和用户没有选择通过图像的自动抓取，这应该是正确的。

这个方法应该是一个字符串,表示将使用(如HTTP请求方法。 ‘HEAD’)。
如果提供，其值是存储在 method属性和使用 get_method()。通过设置子类可能表明一个默认的方法 method类本身的属性。
3.3版本的变化:：Request.method参数是添加到请求类。
3.4版本的变化：默认的 Request.method可能会显示在类级别。


类urllib.request.OpenerDirector
OpenerDirector类打开url并通过 BaseHandler连接在一起。它管理处理程序的连接,和恢复错误。

类 urllib.request.BaseHandler
这是对于所有已注册的处理程序的基类

类 urllib.request.HTTPRedirectHandler
一个类来处理重定向

类urllib.request.HTTPCookieProcessor(cookiejar=None)
一个类来处理HTTP cookie。

类 urllib.request.ProxyHandler(proxies=None)
导致请求通过一个代理。如果代理是给定的，它必须是一个字典的代理协议名称映射到url。默认值是从环境变量的列表 _proxy中读取代理。
如果没有代理设置环境变量，那么在Windows环境中代理设置了从注册表部分的网络设置，在Mac OS X环境代理信息检索的OS X系统配置框架。
禁用一个代理传递一个空的字典。
no_proxy环境变量可以被用来指定主机不能通过代理；如果设置,它应该是一个以逗号分隔的主机名后缀。可选 ：port附加为例 cern.ch,ncsa.uiuc.edu,some.host:8080.
请注意HTTP_PROXY如果一个变量将被忽略 REQUEST_METHOD设置;参见文档 getproxies().

类 urllib.request.HTTPPasswordMgr
保持一个数据库 (realm, uri) -> (user, password)映射。

类 urllib.request.HTTPPasswordMgrWithDefaultRealm
保持一个数据库 (realm, uri) -> (user, password)映射。一个领域 None被认为是一个全方位领域,如果没有其他搜索领域

类 urllib.request.HTTPPasswordMgrWithPriorAuth
一个变体 HTTPPasswordMgrWithDefaultRealm还有一个数据库 uri -> is_authenticated的映射。
可以使用BasicAuth处理程序来确定当发送身份验证凭证立即而不是等待 401响应。

类 urllib.request.AbstractBasicAuthHandler(password_mgr=None)
这是mixin类,帮助与HTTP身份验证,远程主机和代理。果有password_mgr,应该是兼容 HTTPPasswordMgr的。
请参阅部分 HTTPPasswordMgr对象必须支持的接口信息。
如果passwd_mgr还提供了 is_authenticated和 update_authenticated方法(见 HTTPPasswordMgrWithPriorAuth对象),
然后处理程序将使用 is_authenticated结果对于一个给定的URI来决定是否发送请求的身份验证凭证。如果 is_authenticated返回 TrueURI,凭证发送。
如果 is_authenticated是 False凭证不发送,然后如果 401收到响应请求发送身份验证凭证。
如果身份验证成功, update_authenticated被称为设置 is_authenticated TrueURI,这样后续请求的URI或任何super-URIs将自动包括身份验证凭证。
在新的3.5版本:添加 is_authenticated支持。

类 urllib.request.HTTPBasicAuthHandler(password_mgr=None)
与远程主机处理身份验证。如果有password_mgr，应该是兼容HTTPPasswordMgr的。请参阅部分 HTTPPasswordMgr对象必须支持的接口信息。
HTTPBasicAuthHandler将提高 ValueError当面对一个错误的身份验证方案。

类 urllib.request.ProxyBasicAuthHandler(password_mgr=None)
处理与代理身份的验证。如果有password_mgr,应该是兼容 HTTPPasswordMgr的。请参阅部分 HTTPPasswordMgr对象必须支持的接口信息。

类urllib.request.AbstractDigestAuthHandler(password_mgr=None)
这是mixin类,帮助与HTTP身份验证,远程主机和代理。password_mgr,如果有,应该是兼容的 HTTPPasswordMgr;请参阅部分 HTTPPasswordMgr对象必须支持的接口信息

类urllib.request.HTTPDigestAuthHandler(password_mgr=None)
与远程主机处理身份验证。如果有password_mgr，应该是兼容 HTTPPasswordMgr的；请参阅部分 HTTPPasswordMgr对象必须支持的接口信息。
摘要式身份验证处理程序和基本身份验证处理器都是补充说,摘要式身份验证总是尝试第一次。如果主机返回一个40 x再次回应,它发送到基本身份验证处理程序来处理。
这个处理程序方法将提高 ValueError当面对除了消化或基本身份验证方案。
3.3版本的变化:提高 ValueError不支持的身份验证方案。

类urllib.request.ProxyDigestAuthHandler(password_mgr=None)
处理与代理身份验证。如果有password_mgr，应该是兼容 HTTPPasswordMgr的；请参阅部分 HTTPPasswordMgr对象必须支持的接口信息

类 urllib.request.HTTPHandler
一个类来处理HTTP url

类 urllib.request.HTTPSHandler(debuglevel=0, context=None, check_hostname=None)
一个类来处理开放的HTTPS url。在context 文和check_hostname有相同的意义 http.client.HTTPSConnection.
3.2版本的变化:context and check_hostname被补充。

类 urllib.request.FileHandler
打开本地文件

类 urllib.request.DataHandler
开放数据的url

类 urllib.request.FTPHandler
开放的FTP url

类 urllib.request.CacheFTPHandler
打开FTP url,保持打开的FTP连接缓存来减少延迟

类 urllib.request.UnknownHandler
全方位类处理未知的url。

类 urllib.request.HTTPErrorProcessor
HTTP错误响应过程。

"""
