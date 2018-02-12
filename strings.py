import global_variable

def make_response_string(location,predictTime,plate_no):
    return plate_no+" 현재 "+str(location)+"번째 전 정류장, "+str(predictTime)+"분 후 도착 예정\n"


def make_help_string():
    response="현재 지원하는 노선 : "
    for key in global_variable.route_list:
        response+=key+", "
    response+="\n현재 지원하는 정류장 : "
    for key in global_variable.station_list:
        response+=key+", "
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

def make_bus_api_string(station_id, route_id):
    return 'http://openapi.gbis.go.kr/ws/rest/busarrivalservice?' \
          'serviceKey=' + global_variable.BUS_API_KEY + \
          '&stationId=' + station_id + \
          '&routeId=' + route_id
