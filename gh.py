from locale import DAY_1
import requests 
import datetime
from time import strftime
import json
import logging
from pypushdeer import PushDeer

def queryCureRemainInfo(webId):
    # init variable
    hostURI = 'http://gzpt.massage-hospital.com/intelligenthospitalBjAmyy//Cure/cureRemainQuery'

    headers = {
        "Host": "gzpt.massage-hospital.com",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "zh-CN,zh-Hans;q=0.9",
        "Origin": "http://gzpt.massage-hospital.com",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) MicroMessenger/6.8.0(0x16080000) MacWechat/3.5.5(0x13050510) Safari/605.1.15 NetType/WIFI",
        "Referer": "http://gzpt.massage-hospital.com/intelligenthospitalBjAmyy/fzyspb.html?recGroupInfosList=%5B%7B%22recGroupCode%22:%2217%22,%22recGroupName%22:%22%E9%A2%88%E8%83%8C%E9%83%A8%E6%8E%A8%E6%8B%BF%22,%22acsBizId%22:%224108001%22,%22groupNo%22:%220%22%7D%5D",
        "Cookie": "acw_tc=0bd17c5e16665303316732209e0122a9a88c3a2c3cb8b35aa84216caa97c1e"
    }


    bookingTime = datetime.datetime.now() + datetime.timedelta(days=DAY_1)

    payload = {
        'webId':webId,
        'direCode':'091',
        'accessPatId':'1032174',
        'recGroupInfos':'[{"recGroupCode":"17","recGroupName":"颈背部推拿","acsBizId":"4108001","groupNo":"0"}]',
        'deptCode':'048',
        'drCode':'9103',
        'shiftCode':'01',
        'dutyDate':bookingTime.strftime("%Y%m%d")
    }

    # 发送请求
    x = requests.post(hostURI,headers=headers,data = payload)
    return json.loads(x.text)

def cureBooking(webId,roomCode,shiftCode,schDate,poolNum):
      # init variable
    hostURI = 'http://gzpt.massage-hospital.com/intelligenthospitalBjAmyy//Cure/cureRemainQuery'

    headers = {
        "Host": "gzpt.massage-hospital.com",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "zh-CN,zh-Hans;q=0.9",
        "Origin": "http://gzpt.massage-hospital.com",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) MicroMessenger/6.8.0(0x16080000) MacWechat/3.5.5(0x13050510) Safari/605.1.15 NetType/WIFI",
        "Referer": "http://gzpt.massage-hospital.com/intelligenthospitalBjAmyy/fzyspb.html?recGroupInfosList=%5B%7B%22recGroupCode%22:%2217%22,%22recGroupName%22:%22%E9%A2%88%E8%83%8C%E9%83%A8%E6%8E%A8%E6%8B%BF%22,%22acsBizId%22:%224108001%22,%22groupNo%22:%220%22%7D%5D",
        "Cookie": "acw_tc=0bd17c5e16665303316732209e0122a9a88c3a2c3cb8b35aa84216caa97c1e"
    }


    bookingTime = datetime.datetime.now() + datetime.timedelta(days=DAY_1)
    #bookingTime.strftime("%Y-%m-%d")
    poolInfos = [{
        "schDate":schDate,
        "poolNum":poolNum
    }]

    payload = {
        'accessPatId': '1032174',
        'webId': webId,
        'direCode': '091',
        'recGroupInfos': '[{"recGroupCode":"17","recGroupName":"颈背部推拿","acsBizId":"4108001","groupNo":"0"}]',
        'acsBizId': '4108001',
        'bookingTime': '2022-10-23 22:00:00',
        'dutyDate': '20221101',
        'deptCode': '048',
        'drCode': '9103',
        'shiftCode': shiftCode,
        'roomCode': roomCode,
        'poolInfos': json.dumps(poolInfos)
    }

    # 发送请求
    x = requests.post(hostURI,headers=headers,data = payload)
    print(payload)
    return json.loads(x.text)

'''
查询余票信息返回结果
{
	"resultCode": "0",
	"errorMsg": "查询成功",
	"accessPatId": "8206",
	"webId": "74814428-28206",
	"direCode": "09 ",
	"DireName": "复诊理疗",
	"recGroupCode": "0",
	"recGroupName": "所有病种",
	"acsBizId": "53275",
	"dutyDate": "2020.08.11",
	"deptCode": "003",
	"deptName": "地下治疗室",
	"drCode": "f-3",
	"drName": "f-3",
	"roomCode": "103 ",
	"roomName": "三诊室",
	"shiftCode": "01 ",
	"shiftName": "0-8",
	"totalNumber": "20",
	"remain": "20",
	"state": "1",
	"poolInfos": [{
		"schDate": "2020.08.11",
		"poolNum": "1",
		"beginTime": "00:00:00",
		"endTime": "00:30:00",
		"truncateTime": ""
	}]

}
'''

def pushMsg2Phone(cureRemainInfo,bookingResult):
    '''
    pushdeer.send_text("hello world", desp="optional description")
    pushdeer.send_markdown("# hello world", desp="**optional** description in markdown")
    pushdeer.send_image("https://github.com/easychen/pushdeer/raw/main/doc/image/clipcode.png")
    pushdeer.send_image(
        "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVQYV2NgYAAAAAMAAWgmWQ0AAAAASUVORK5CYII=")
    '''
    pushdeer = PushDeer(pushkey="PDU17221TOabvW3v9dxaEbpHnV3KNxnyaHvyaQjDW")
    pushdeer.send_markdown("# 按摩医院抢号通知", desp="- cureRemainInfo\n" + json.dumps(cureRemainInfo,ensure_ascii=False) + "\n- bookingResult\n"+json.dumps(bookingResult,ensure_ascii=False))
   

def booking(webId):
    logging.info("-----start booking-----")
    cureRemainInfo = queryCureRemainInfo(webId)
    
    logging.info("queryCureRemainInfo result:"+json.dumps(cureRemainInfo,ensure_ascii=False))
    if cureRemainInfo["code"] == 1:
        pushMsg2Phone(cureRemainInfo,"")
        return 

    roomCode = cureRemainInfo['roomCode']
    shiftCode = cureRemainInfo['shiftCode']
    schDate = cureRemainInfo['schDate']
    poolNum = cureRemainInfo['poolNum']
    bookingResult = cureBooking(webId=webId,roomCode=roomCode,shiftCode=shiftCode,schDate=schDate,poolNum=poolNum)
    logging.info("bookingResult result:"+bookingResult)
    pushMsg2Phone(cureRemainInfo,bookingResult)


if __name__ == '__main__':
    logging.basicConfig(filename='./log.log',level=logging.DEBUG,format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    webId = 'o3Z_GwrCLLpCEnnhjggrDXEh5ChU'
    booking(webId)   

