from xml.etree import ElementTree
import requests
import global_variable
import strings
import subway
from bs4 import BeautifulSoup

class Reservation:

    def __init__(self, user_id, channel_id, station, route, min):
        self.user_id = user_id
        self.channel_id = channel_id
        self.station = station
        self.route = route
        self.min = min

    def __repr__(self):
        return '%r에 %r가 %r분 이내 거리에 오면 알려주기' % (self.station, self.route,self.min)

    def check(self):
        station_id, route_id = check_valid_input(self.station, self.route)
        assert check_valid_input(self.station, self.route) != False

        req = strings.make_bus_api_string(station_id=station_id, route_id=route_id)
        xml_root = ElementTree.fromstring(requests.get(req).content)

        predict_time = int(xml_root[2][0][7].text)
        if predict_time <= self.min:
            assert predict_time != 0
            return predict_time

        return False

    def alert_to_user(self,min):

        if self.station is None or self.route is None:
            global_variable.get_slacker().chat.post_message(channel="#test_bot", text="에러뜸", username="bus bot")

        result_str = self.route + " " + self.station + "에 " + str(min)+"분 이내로 도착"
        global_variable.get_slacker().chat.post_message(channel=self.channel_id, text=result_str, username="bus bot")


#                                      string
def check_valid_input(station, route, min=None):

    if (station not in global_variable.station_list or route not in global_variable.route_list):
        return False

    if(min!=None and not (min.isnumeric() and int(float(min)) > 2)):
        return False

    station_id = global_variable.station_list[station]
    route_id = global_variable.route_list[route]
    return station_id, route_id

def request_info(station_id,route_id=None):

    req = strings.make_bus_api_string(station_id=station_id, route_id=route_id)
    xml_root=ElementTree.fromstring(requests.get(req).content)

    return parse_info(xml_root,station_id,route_id)

#버스정류장 코드 5자리 또는 이름으로 검색 후 제대로 된 정류장인지 검증
def stations_get_by_name(name,route):
    stationList = []
    result = []
    link = 'http://openapi.gbis.go.kr/ws/rest/busstationservice?serviceKey='+global_variable.BUS_API_KEY+'&keyword='+name
    response = requests.get(link)
    soup = BeautifulSoup(response.content,'lxml-xml')
    for stop in soup.findAll('busStationList'):
    	stationList += [{stop.find('stationId').string:stop.find('stationName').string}]
    if stationList == []:
        return "검색된 정류소가 없습니다."
    else:
        for stnlist in stationList:
            x = list(stnlist.keys())[0]
            link = 'http://openapi.gbis.go.kr/ws/rest/busstationservice/route?serviceKey='+global_variable.BUS_API_KEY+'&stationId='+x
            response = requests.get(link)
            soup = BeautifulSoup(response.content,'lxml-xml')
            for busline in soup.findAll('busRouteList'):
                if busline.find('routeName').string == route:
                    routeId = busline.find('routeId').string
                    result += [[x,{routeId:route},stnlist[x]]]
        return request_info_2(result,route,x)

def parse_info(xml_root,station_id,route_id=None):

    if route_id != None:
        station_name = list(global_variable.station_list.keys())[list(global_variable.station_list.values()).index(station_id)]
        route_name = list(global_variable.route_list.keys())[list(global_variable.route_list.values()).index(route_id)]
        response=station_name+" "+route_name+"\n"

        if(xml_root[1][1].text=='4'):
            return strings.make_no_result_string()

        response += strings.make_response_string(xml_root[2][0][1].text, xml_root[2][0][7].text, xml_root[2][0][5].text)

        if(xml_root[2][0][2].text is not None):
            response+= strings.make_response_string(xml_root[2][0][2].text, xml_root[2][0][8].text, xml_root[2][0][6].text)

        return response
#문자열 만들기
#beautifulsoup을 이용한 파싱
def request_info_2(result,route,stnid):
    string=''
    for x in result:
        string+='\n\n*'+x[2]+'* 정류소의 '+route+'번 도착 정보\n'
        station_id = x[0]
        route_id = list(x[1].keys())[0]
        req = strings.make_bus_api_string(station_id,route_id)
        response=requests.get(req)
        soup = BeautifulSoup(response.content,'lxml-xml')
        string += strings.get_destination(route,station_id)
        plateno1=soup.find('plateNo1')
        if plateno1!=None:
            plateno1=soup.find('plateNo1').string
            location1=soup.find('locationNo1').string
            predict_time1=soup.find('predictTime1').string
            remain_seat1=soup.find('remainSeatCnt1').string
            string+=strings.make_response_string(location1,predict_time1,plateno1,remain_seat1)
            second_bus=soup.find('locationNo2').string
            if second_bus != None:
                plateno2=soup.find('plateNo2').string
                location2=soup.find('locationNo2').string
                predict_time2=soup.find('predictTime2').string
                remain_seat2=soup.find('remainSeatCnt2').string
                string+=strings.make_response_string(location2,predict_time2,plateno2,remain_seat2)
        else:
            string+=strings.make_no_result_string()
    return string




def parse_msg(msg):

    if(msg['type']=='message'):

        msg_text = msg['text']

        if(msg_text=="버스봇 헬프"):
            return strings.make_help_string()

        if(msg_text=="버스봇 내 예약"):
            return strings.make_user_resereve_list_string(msg['user'])

        input = msg_text.split()  # input : [정류장, 노선번호]

        if(input[0]=="버스봇"):

            if(msg_text.count(' ')==2):
                id = check_valid_input(input[1], input[2])

                if(id):
                    return request_info(station_id=id[0], route_id=id[1])

                else:
                    return stations_get_by_name(input[1],input[2])


            elif (msg_text.count(' ')==4):
                id = check_valid_input(input[1], input[2], input[3])

                if(id):
                    # todo : 만약 이미 추가돼있다면 추가하지 않기
                    # todo : 꼭 제거 기능을 만들어야 하나?
                    if(input[4] == 'on'):
                        global_variable.get_reserve_list().append(Reservation(msg['user'],msg['channel'], input[1], input[2], int(float(input[3]))))
                        return "예약됨"

                else:
                    if(input[4]=='on'):
                        global_variable.get_reserve_list().append(Reservation(msg['user'],msg['channel'], input[1], input[2], int(float(input[3]))))
                        return "예약됨"
                    return strings.make_not_supported_string(1)

            else:
                return strings.make_help_string()
        elif(input[0]=="전철봇"):
            if (msg_text.count(' ')==1):
                return subway.subway(input[1])
            else:
                return string.make_help_string()
