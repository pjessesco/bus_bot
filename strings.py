import global_variable
import requests
from bs4 import BeautifulSoup
#plate_no - 잔여좌석(42이상), 특정 번호판 차량(3102)
def is_doubledecker(plate_no,seat):
    doubledecker_list = ['1039', '1310', '1320', '1557', '1681']
    if int(seat) > 41 or plate_no[-4:] in doubledecker_list:
        return ", 2층 버스입니다.\n"
    else:
        return "\n"

#routeNum - 노선번호('3102'), stnId - 정류장코드
#목적지 추가 코드
def get_destination(routeNum,stnId):
    string = ''
    temp = 0
    result_link = get_busstop_info2(stnId)
    response2 = requests.get(result_link)
    html = response2.text
    soup2 = BeautifulSoup(html,'html.parser')
    destination = soup2.findAll('span',{'class',"ellipsis"})[1:]
    routeName = soup2.findAll('div',{'class':'bus-num-y float-l md-30p pdt_3'})
    routeName += soup2.findAll('div',{'class':'bus-num-g float-l md-30p pdt_3'})
    routeName += soup2.findAll('div',{'class':'bus-num-b float-l md-30p pdt_3'})
    routeName += soup2.findAll('div',{'class':'bus-num-r float-l md-30p pdt_3'})
    routeName += soup2.findAll('div',{'class':'bus-num-p float-l md-30p pdt_3'})
    routeName += soup2.findAll('div',{'class':'bus-num-gr float-l md-30p pdt_3'})
    for index in range(0,len(destination)):
        if routeName[index].string == routeNum and temp != index:
            temp = index
            string += destination[index].string + '\n'
            break
    return string

#잔여좌석 안내기 추가
def make_response_string(location,predictTime,plate_no,remainSeatCnt='-1'):
    string=plate_no+" 현재 "+str(location)+"번째 전 정류장, "+str(predictTime)+"분 후 도착 예정"
    if remainSeatCnt != '-1':
        string += ', 잔여좌석 '+remainSeatCnt+'석'
    string+=is_doubledecker(plate_no,remainSeatCnt)
    return string

def make_help_string():
    response ='마을버스를 제외한 경기도 차적 노선 및 경기도 진입 전 노선 지원'
    response += "\n경기도 전 정류장 및 서울/인천 일부 정류장 지원"
    response += "\nex)\n"
    response += "\n버스 조회 : *버스봇 양재 3102*"
    response += "\n알람 등록 : *버스봇 양재 3102 10 on* (3102 버스가 양재역에 10분 이내로 올 때 알람)"
    response += "\n예약 조회 : *버스봇 내 예약*"
    #todo : 예약 없애기 만들기
    return response


def make_not_supported_string(param=None):

    if param is not None:
        return "지원하지 않는 정류장/노선번호/시간. 지원하는 노선은 \"버스봇 헬프\"" \
               "\n노선이나 정류장을 추가하려면 https://github.com/pjessesco/bus_bot" \
               "\n시간은 3분 이상으로 하세요"

    return "지원하지 않는 정류장/노선번호. 지원하는 노선은 \"버스봇 헬프\"" \
        "\n노선이나 정류장을 추가하려면 https://github.com/pjessesco/bus_bot"

def make_user_resereve_list_string(user_id):

    reserve_list = ""

    # todo : 가끔 작동을 안한다..? 2인 이상으로 테스트 해보기

    for reserve in global_variable.get_reserve_list():
        if (reserve.user_id == user_id):
            reserve_list += str(reserve)+"\n"

    if reserve_list == "":
        return "없음"
    return reserve_list

def make_no_result_string():
    return "결과가 존재하지 않습니다. 버스가 없을수도"

# 특정 정류장의 특정 노선의 도착 정보
def make_bus_api_string(station_id, route_id=None):

    if route_id == None:
        return 'http://openapi.gbis.go.kr/ws/rest/busarrivalservice/station?' \
               'serviceKey=' + global_variable.BUS_API_KEY + \
               '&stationId=' + station_id

    return 'http://openapi.gbis.go.kr/ws/rest/busarrivalservice?' \
          'serviceKey=' + global_variable.BUS_API_KEY + \
          '&stationId=' + station_id + \
          '&routeId=' + route_id

def make_bus_api_string_by_name(name):
    return 'http://openapi.gbis.go.kr/ws/rest/busstationservice?serviceKey='+global_variable.BUS_API_KEY+'&keyword='+name

def get_busstop_info(stnid):
    return 'http://openapi.gbis.go.kr/ws/rest/busstationservice/route?serviceKey='+global_variable.BUS_API_KEY+'&stationId='+stnid

def get_busstop_info2(stnid):
    return 'http://m.gbis.go.kr/search/StationArrivalViaList.do?stationId='+stnid