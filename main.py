from xml.etree import ElementTree
from slacker import Slacker
import requests
import time
import websocket
import ast

#config.py에 키 만들기
import config

BUS_API_KEY=config.BUS_API_KEY
SLACK_TOKEN=config.SLACK_TOKEN

# 추가하기 : http://www.gbis.go.kr/gbis2014/publicService.action?cmd=tBusStationList 에서 정류소 이름으로 검색 (테스트 값 입력 후)
#          -> 나온 정류소 id를 이용해서 노선 id 검색

# 반대 경우는 생각하지 않았음
# TODO : 상행/하행 구분하기
station_list={  # 강남으로 가는 정류장
                "게스트하우스":"216000379","게하":"216000379",
                "기숙사":"216000383","긱":"216000383","긱사":"216000383",
                # 정류장이 한개밖에 없음
                "양재역":"121000970","양재": "121000970","양재역9번출구": "121000970"
                # 강남에서 오는 정류장
                }

route_list={"3102":"216000061","20":"224000018"}

# 해당 정류소에 정차하는 버스노선들
# def test1(station_id):
#     req='http://openapi.gbis.go.kr/ws/rest/busarrivalservice/station?' \
#       'serviceKey='+BUS_API_KEY+ \
#       '&stationId='+station_id

# 해당 정류소에 정차하는 특정 버스 노선 정보
def get_info(station,route):

    if(station in station_list):
        station_id=station_list[station]
    else:
        return None

    if(route in route_list):
        route_id=route_list[route]
    else:
        return None

    req='http://openapi.gbis.go.kr/ws/rest/busarrivalservice?' \
      'serviceKey='+BUS_API_KEY+ \
      '&stationId='+station_id+ \
      '&routeId='+route_id

    xml_root=ElementTree.fromstring(requests.get(req).content)

    return parse_info(xml_root,station,route)

def parse_info(xml_root,station,route):

    response=station+" "+route+"\n"
    if(xml_root[1][1].text=='4'):
        return "결과가 존재하지 않습니다. 버스가 없을수도"
    response+=make_response(xml_root[2][0][1].text,xml_root[2][0][7].text,xml_root[2][0][5].text)
    if(xml_root[2][0][2].text is not None):
        response+=make_response(xml_root[2][0][2].text,xml_root[2][0][8].text,xml_root[2][0][6].text)
    return response

def make_response(location,predictTime,plate_no):
    return plate_no+" 현재 "+str(location)+"번째 전 정류장, "+str(predictTime)+"분 후 도착 예정\n"

def make_help():
    response="현재 지원하는 노선 : "
    for key in route_list:
        response+=key+", "
    response+="\n현재 지원하는 정류장 : "
    for key in station_list:
        response+=key+", "
    response+="\n예시 : \"버스봇 양재 3102\""
    return response

def parse_msg(msg):

    if(msg['type']=='message'):
        if(msg['text']=="버스봇 헬프"):
            return make_help()

        elif(msg['text'].count(' ')==2):
            input=msg['text'].split()    # input : [정류장, 노선번호]
            if(input[0]=="버스봇"):
                info=get_info(input[1],input[2])
                if(info is None):
                    return "지원하지 않는 정류장/노선번호. 지원하는 노선은 \"버스봇 헬프\"" \
                           "\n노선이나 정류장을 추가하려면 https://github.com/pjessesco/bus_bot"
                else:
                    return info

slacker=Slacker(SLACK_TOKEN)

if slacker.rtm.connect():
    response=slacker.rtm.start()
    sock_endpoint=response.body['url']
    slack_socket=websocket.create_connection(sock_endpoint)
    while True:
        msg=slack_socket.recv()
        if(len(msg)>0):
            res=parse_msg(ast.literal_eval(msg))
            if(res is not None):
                slacker.chat.post_message(channel="#random",text=res,username="bus bot")

        time.sleep(1)

else:
    print("connect fail")