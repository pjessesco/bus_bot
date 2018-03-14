from bs4 import BeautifulSoup
import requests
def subway(stn):
    string = ''
    if '역' == stn[-1]:
        stn = stn[:-1]
    status_list = {'0':'진입','1':'도착','2':'전역 출발','3':'전역 도착','4':'전역 진입','5':'전역 접근','99':'운행'}
    response = requests.get('http://swopenapi.seoul.go.kr/api/subway/sample/xml/realtimeStationArrival/0/5/'+stn)
    if response.status_code != 200:
        return '서버가 원활하지 않습니다.'
    soup = BeautifulSoup(response.content,'lxml-xml')
    dest_list = []
    for x in soup.findAll('row'):
        time = -1
        endstn = x.find('bstatnNm').string
        location = x.find('arvlMsg3').string
        status = status_list[x.find('arvlCd').string]
        if endstn not in dest_list:
            if (x.find('barvlDt')) and (x.find('barvlDt').string) != '0':
                time = x.find('barvlDt').string
            if '전역' in status:
                string += endstn+' 행\n'+status+'\n'
                if time != -1 and time != 0:
                    string += str(int(time)//60)+'분 '+str(int(time)%60)+'초 남음\n'
            else:
                if '-1' not in endstn:
                    string += endstn+' 행\n'+location+' '+status+'\n'
                    if time != -1 and time != 0:
                        string += str(int(time)//60)+'분 '+str(int(time)%60)+'초 남음\n'
            dest_list += [endstn]
        else:
            continue
        string += '\n'
    if soup.findAll('row') == []:
        string = '도착예정인 전철이 없습니다.'
    return string