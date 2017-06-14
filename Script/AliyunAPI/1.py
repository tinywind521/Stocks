from functions import getValue
from aliyun import aliyun_api

aliyun_input = {"showapi_res_code":0,"showapi_res_error":"","showapi_res_body":{"dataList":[{"min":"9.0400","minute":"201706141500","open":"9.0600","volumn":"93032","max":"9.0900","close":"9.08"},{"min":"9.0500","minute":"201706141400","open":"9.0600","volumn":"66627","max":"9.0700","close":"9.0600"},{"min":"9.0500","minute":"201706141130","open":"9.0800","volumn":"88800","max":"9.0900","close":"9.0700"},{"min":"9.0600","minute":"201706141030","open":"9.1000","volumn":"117548","max":"9.1300","close":"9.0700"},{"min":"9.1100","minute":"201706140930","open":"9.1200","volumn":"9437","max":"9.1300","close":"9.1100"},{"min":"9.1000","minute":"201706131500","open":"9.1200","volumn":"121434","max":"9.1400","close":"9.1200"},{"min":"9.0900","minute":"201706131400","open":"9.1100","volumn":"85849","max":"9.1200","close":"9.1200"},{"min":"9.0700","minute":"201706131130","open":"9.0700","volumn":"83360","max":"9.1200","close":"9.1100"},{"min":"9.0500","minute":"201706131030","open":"9.1200","volumn":"153102","max":"9.1200","close":"9.0700"},{"min":"9.1100","minute":"201706130930","open":"9.1100","volumn":"4689","max":"9.1200","close":"9.1100"},{"min":"9.1100","minute":"201706121500","open":"9.1200","volumn":"72065","max":"9.1400","close":"9.1100"},{"min":"9.1100","minute":"201706121400","open":"9.1200","volumn":"73444","max":"9.1600","close":"9.1200"},{"min":"9.1000","minute":"201706121130","open":"9.1800","volumn":"131214","max":"9.1900","close":"9.1200"},{"min":"9.1000","minute":"201706121030","open":"9.1400","volumn":"207499","max":"9.1900","close":"9.1900"},{"min":"9.1200","minute":"201706120930","open":"9.1500","volumn":"20356","max":"9.1600","close":"9.1500"},{"min":"9.1200","minute":"201706091500","open":"9.1300","volumn":"105456","max":"9.1500","close":"9.1500"},{"min":"9.1300","minute":"201706091400","open":"9.1400","volumn":"72853","max":"9.1600","close":"9.1400"},{"min":"9.1300","minute":"201706091130","open":"9.1800","volumn":"151273","max":"9.2000","close":"9.1400"},{"min":"9.1400","minute":"201706091030","open":"9.1400","volumn":"348848","max":"9.2100","close":"9.1900"},{"min":"9.1400","minute":"201706090930","open":"9.1500","volumn":"7038","max":"9.1500","close":"9.1400"},{"min":"9.0900","minute":"201706081500","open":"9.1100","volumn":"108761","max":"9.1500","close":"9.1300"},{"min":"9.0900","minute":"201706081400","open":"9.1100","volumn":"65902","max":"9.1200","close":"9.1100"},{"min":"9.0900","minute":"201706081130","open":"9.1000","volumn":"100367","max":"9.1200","close":"9.1100"},{"min":"9.0800","minute":"201706081030","open":"9.1100","volumn":"107974","max":"9.1200","close":"9.1000"},{"min":"9.0900","minute":"201706080930","open":"9.1100","volumn":"7632","max":"9.1100","close":"9.1000"},{"min":"9.0900","minute":"201706071500","open":"9.0900","volumn":"121792","max":"9.1300","close":"9.1300"},{"min":"9.0800","minute":"201706071400","open":"9.0800","volumn":"135705","max":"9.1400","close":"9.0900"},{"min":"9.0600","minute":"201706071130","open":"9.1100","volumn":"135107","max":"9.1200","close":"9.0800"},{"min":"9.0100","minute":"201706071030","open":"9.0200","volumn":"253119","max":"9.1500","close":"9.1000"},{"min":"9.0100","minute":"201706070930","open":"9.0200","volumn":"8172","max":"9.0200","close":"9.0200"},{"min":"8.9900","minute":"201706061500","open":"9.0000","volumn":"104106","max":"9.0400","close":"9.0400"},{"min":"8.9900","minute":"201706061400","open":"9.0100","volumn":"88478","max":"9.0300","close":"8.9900"},{"min":"9.0100","minute":"201706061130","open":"9.0300","volumn":"48888","max":"9.0400","close":"9.0100"},{"min":"9.0000","minute":"201706061030","open":"9.0100","volumn":"113869","max":"9.0600","close":"9.0300"},{"min":"9.0000","minute":"201706060930","open":"9.0100","volumn":"5657","max":"9.0200","close":"9.0100"},{"min":"9.0100","minute":"201706051500","open":"9.0400","volumn":"69489","max":"9.0500","close":"9.0300"},{"min":"8.9900","minute":"201706051400","open":"9.0300","volumn":"69620","max":"9.0500","close":"9.0400"},{"min":"9.0000","minute":"201706051130","open":"9.0400","volumn":"140151","max":"9.0500","close":"9.0300"},{"min":"8.9900","minute":"201706051030","open":"9.1300","volumn":"354872","max":"9.1700","close":"9.0400"},{"min":"9.1300","minute":"201706050930","open":"9.1300","volumn":"13843","max":"9.1700","close":"9.1600"},{"min":"9.1500","minute":"201706021500","open":"9.1700","volumn":"120506","max":"9.1900","close":"9.1700"},{"min":"9.1500","minute":"201706021400","open":"9.2200","volumn":"119318","max":"9.2300","close":"9.1700"},{"min":"9.1900","minute":"201706021130","open":"9.2700","volumn":"173697","max":"9.2700","close":"9.2200"},{"min":"9.1400","minute":"201706021030","open":"9.1800","volumn":"357236","max":"9.2900","close":"9.2700"},{"min":"9.1600","minute":"201706020930","open":"9.1800","volumn":"6582","max":"9.1900","close":"9.1600"},{"min":"9.1600","minute":"201706011500","open":"9.1700","volumn":"224392","max":"9.2100","close":"9.1900"},{"min":"9.1200","minute":"201706011400","open":"9.1400","volumn":"110115","max":"9.1800","close":"9.1700"},{"min":"9.1400","minute":"201706011130","open":"9.1800","volumn":"57646","max":"9.1900","close":"9.1400"},{"min":"9.1400","minute":"201706011030","open":"9.2000","volumn":"174029","max":"9.2300","close":"9.1900"},{"min":"9.1700","minute":"201706010930","open":"9.2000","volumn":"10516","max":"9.2000","close":"9.1800"}],"ret_code":0,"market":"sz","count":"50","name":"平安银行","code":"000001"}}


def get_realtimeValue(aliyun_input):
    realtimeValue = aliyun_input['showapi_res_body']['dataList']
    return realtimeValue
s = get_realtimeValue(aliyun_input)
s.reverse()
print(len(s))
for element in s:
    print(element)

s = getValue.get_dateList('20170101', 10)
print(s)
a = aliyun_api.realtime('000001', s[0], '60')
print(a)



# print(c)

# def ss(string=[]):
#     for s in string:
#         print(s)
#     return None
# try:
#     d = input('Input Reference: ')
#     dd = list(d)
#     print(dd)
#     ss(dd)
# except:
#     print('Ref Error!')