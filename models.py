import requests
from bs4 import BeautifulSoup
import pandas as pd

# vo : 정류소명 조회
class StationByName:

    def __init__(self, stId=None, stNm=None, tmX=None, tmY=None, arsId=None, posX=None, posY=None):
        self.stId = stId
        self.stNm = stNm
        self.tmX = tmX
        self.tmY = tmY
        self.arsId = arsId
        self.posX = posX
        self.posY = posY


# vo : 좌표기반 근접 정류소 목록 조회
class Station_gps:

    def __init__(self, stationId=None, stationNm=None, gpsX=None, gpsY=None, arsId2=None, dist=None, posX=None, posY=None, stationTp=None):
        self.stationId=stationId
        self.stationNm=stationNm
        self.gpsX=gpsX
        self.gpsY=gpsY
        self.arsId2=arsId2
        self.dist=dist
        self.posX=posX
        self.posY=posY
        self.stationTp=stationTp

# vo : 고유번호별교통약자전용정류소목록조회 요청 정보 : arsId-정류소 고유번호
class LowStaionByUid:

    def __init__(self, stId=None, stnNm=None, arsId=None,
                 busRouteId=None, rtNm=None, firstTm=None,
                 lastTm=None, term=None, repTm1=None,
                 plainNo1=None, vehId1=None,arrmsg1=None,
                 vehId2=None, plainNo2=None, repTm2=None,
                 arrmsg2=None):
        self.stId=stId # 정류소 ID
        self.stnNm=stnNm # 정류소명
        self.arsId=arsId # 정류소 고유번호
        self.busRouteId=busRouteId # 노선ID
        self.rtNm=rtNm # 버스 번호
        self.firstTm=firstTm #첫차시간
        self.lastTm=lastTm #막차시간
        self.term=term #배차간격

        self.vehId1=vehId1 #첫번째도착예정버스ID
        self.plainNo1=plainNo1 #첫번째도착예정차량번호
        self.repTm1=repTm1 #첫번째도착예정버스의 최종 보고 시간
        self.arrmsg1=arrmsg1 #첫번째도착예정버스의 도착정보메시지

        self.vehId2=vehId2 #두번째도착예정버스ID
        self.plainNo2=plainNo2 #두번째도착예정차량번호
        self.repTm2=repTm2 #두번째도착예정버스의 현재구간 순번
        self.arrmsg2=arrmsg2 #두번째도착예정버스의 최종 정류소명

class StationService:
    def __init__(self):
        self.base_url = 'http://ws.bus.go.kr/api/rest/stationinfo/'
        self.api_key = 'fR6oQVhtpaWn2RyCaSSreFVYmVYFcfv2W%2F03wiTFyLbtmNtjln0rmHyK4XDei92IJnjBkLpqQAc0BENj8nrhEw%3D%3D'

    # 정류장 좌표로 정류장정보 얻기
    def getStationByPosInfo(self, tmX: str, tmY: str, radius: str):
        cmd = '/getStationByPos'
        url = self.base_url + cmd + '?ServiceKey=' + self.api_key + '&tmX=' + tmX + '&tmY=' + tmY + '&radius=' + radius
        html = requests.get(url).text
        root = BeautifulSoup(html, 'lxml-xml')
        code = root.find('headerCd').get_text()
        stations = []
        if code == '0':
            items = root.select('itemList')
            for item in items:
                stationId = item.find('stationId').get_text()
                stationNm = item.find('stationNm').get_text()
                gpsX = item.find('gpsX').get_text() # 위도 x
                gpsY = item.find('gpsY').get_text() # 위도 y
                arsId2 = item.find('arsId').get_text()  # 정류소 고유번호
                dist = item.find('dist').get_text()  # 거리
                posX = item.find('posX').get_text()
                posY = item.find('posY').get_text()
                stationTp = item.find('stationTp').get_text()
                stations.append(
                    Station_gps(stationId=stationId, stationNm=stationNm, gpsX=gpsX, gpsY=gpsY, arsId2=arsId2,
                                dist=dist, posX=posX, posY=posY, stationTp=stationTp))

        else:
            print('오류발생 code:', code)

        return stations
        
    # 정류장 이름으로 정류장 정보 얻기
    def getStationByName(self, stSrch:str):
        cmd = '/getStationByName'
        url = self.base_url+cmd+'?ServiceKey='+self.api_key+'&stSrch='+stSrch
        print(url)
        html = requests.get(url).text
        root = BeautifulSoup(html, 'lxml-xml')
        code = root.find('headerCd').get_text()
        if code == '0':
            item = root.select_one('itemList')
            stId = item.find('stId').get_text()
            stNm = item.find('stNm').get_text()
            tmX = item.find('tmX').get_text()
            tmY = item.find('tmY').get_text()
            arsId = item.find('arsId').get_text()
            posX = item.find('posX').get_text()
            posY = item.find('posY').get_text()
        else:
            print('오류발생 code:', code)

        return StationByName(stId=stId, stNm=stNm,tmX=tmX, tmY=tmY, arsId=arsId, posX=posX, posY=posY)



    # 정류장 버스 도착 예정 정보
    def getLowStaionByUidList(self, arsId:str):
        cmd = '/getLowStationByUid'
        url = self.base_url + cmd + '?ServiceKey=' + self.api_key + '&arsId=' + arsId
        html = requests.get(url).text
        root = BeautifulSoup(html, 'lxml-xml')
        code = root.find('headerCd').get_text()
        stations = []
        if code == '0':
            items = root.select('itemList')
            for item in items:
                # 정류소 정보
                stId = item.find('stId').get_text() #정류소 id
                stnNm = item.find('stnNm').get_text() #정류소명
                arsId = item.find('arsId').get_text()

                busRouteId = item.find('busRouteId').get_text() # 노선ID
                rtNm = item.find('rtNm').get_text() # 버스 번호
                firstTm = item.find('firstTm').get_text() #첫차시간
                hour1 = firstTm[:2]
                min1 = firstTm[2:4]
                firstTm = hour1 + ':' + min1

                lastTm = item.find('lastTm').get_text() #막차시간
                hour2 = lastTm[:2]
                min2 = lastTm[2:4]
                lastTm = hour2 + ':' + min2
                term = item.find('term').get_text() #배차간격

                # 첫번째 도착 예정 버스
                vehId1 = item.find('vehId1').get_text() #첫번째도착예정버스ID
                # plainNo1 = item.find('plainNo1').get_text() #첫번째도착예정차량번호
                repTm1 = item.find('repTm1').get_text() #첫번째도착예정버스의 최종 보고 시간
                arrmsg1 = item.find('arrmsg1').get_text() #첫번째도착예정버스의 도착정보메시지

                # 두번째 도착 예정 버스
                vehId2 = item.find('vehId2').get_text() #두번째도착예정버스ID
                # plainNo2 = item.find('plainNo2').get_text() #두번째도착예정차량번호
                # repTm2 = item.find('repTm2').get_text() #두번째도착예정버스의 현재구간 순번
                arrmsg2 = item.find('arrmsg2').get_text() #두번째도착예정버스의 최종 정류소명

                stations.append(
                    LowStaionByUid(stId=stId, stnNm=stnNm, arsId=arsId, busRouteId=busRouteId, rtNm=rtNm,
                 firstTm=firstTm, lastTm=lastTm, term=term,
                 vehId1=vehId1, plainNo1=None, repTm1=repTm1,
                 arrmsg1=arrmsg1,vehId2=vehId2, plainNo2=None,
                 repTm2=None, arrmsg2=arrmsg2))

        else:
            print('오류발생 code:', code)

        return stations