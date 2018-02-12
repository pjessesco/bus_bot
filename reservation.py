class Reservation:

    def __init__(self, user_id, station, route, min):
        self.user_id = user_id
        self.station = station
        self.route = route
        self.min = min

    def __repr__(self):
        return '%r에 %r가 %r분 이내 거리에 오면 알려주기' % (self.station, self.route,self.min)

    def check(self):

        station_id, route_id = check_valid_input(self.station, self.route)
        assert check_valid_input(self.station, self.route) != False

        req = 'http://openapi.gbis.go.kr/ws/rest/busarrivalservice?' \
              'serviceKey=' + BUS_API_KEY + \
              '&stationId=' + station_id + \
              '&routeId=' + route_id

        xml_root = ElementTree.fromstring(requests.get(req).content)

        predict_time = int(xml_root[2][0][7].text)
        if predict_time <= self.min:
            assert predict_time != 0
            return predict_time

        return False

    def alert_to_user(self,min):

        if self.station is None or self.route is None:
            get_slacker().chat.post_message(channel="#test_bot", text="에러뜸", username="bus bot")

        result_str = self.route + " " + self.station + "에 " + str(min)+"분 이내로 도착"
        get_slacker().chat.post_message(channel="#test_bot", text=result_str, username="bus bot")
