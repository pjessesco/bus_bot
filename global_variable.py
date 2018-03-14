from slacker import Slacker
import os

#SLACK_TOKEN = os.environ.get('SLACK_TOKEN')
#BUS_API_KEY = os.environ.get('BUS_API_KEY')
SLACK_TOKEN = 'xoxp-328261850279-327331276549-327219286052-3defcb338b1ae57509cab8f36b4a5ff4'
BUS_API_KEY = '1234567890'
#config.py에 키 만들기
# import config

# SLACK_TOKEN=config.SLACK_TOKEN
# BUS_API_KEY=config.BUS_API_KEY



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

route_list={"3102":"216000061","20":"224000018","10-1":'216000068'}

_reserve_list = None
_slacker = None

def get_reserve_list():
    global _reserve_list
    if _reserve_list is None:
        _reserve_list = []
    return _reserve_list

def get_slacker():
    global _slacker
    if _slacker is None:
        _slacker = Slacker(SLACK_TOKEN)
    return _slacker

