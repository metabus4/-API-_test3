from flask import Flask, request, render_template, redirect, Blueprint
import models as mo
import matplotlib.pyplot as plt

# 블루 프린트 등록, 요청 url을 등록하는
# 라우트를 저장해두는 보관해두는 객체, 라우트를 임시로 저장하는 저장소
bp = Blueprint('station', __name__, url_prefix='/station')

# 정류장과 관련된 기능을 제공해주는 서비스 객체
service_sj = mo.StationService()

@bp.route('/station-gps', methods=['POST'])
def station_gps():
    tmX = request.form['tmX']
    tmY = request.form['tmY']
    radius = request.form['radius']
    station_gps: mo.Station_gps = service_sj.getStationByPosInfo(tmX, tmY, radius)

    # bus=bus, 뷰페이지에 전달할 값
    return render_template('station/stationGps.html', station_gps=station_gps)

@bp.route('/station-name-gps', methods=['POST'])
def station_name_gps():
    stSrch = request.form['stSrch']
    stationByName: mo.StationByName = service_sj.getStationByName(stSrch)
    tmX = str(stationByName.tmX)
    tmY = str(stationByName.tmY)
    radius = str(50) # 반경
    arsId = str(stationByName.arsId)
    station_gps: mo.Station_gps = service_sj.getStationByPosInfo(tmX, tmY, radius)
    lowStaionByUid: mo.LowStaionByUid = service_sj.getLowStaionByUidList(arsId)
    # bus=bus, 뷰페이지에 전달할 값
    return render_template('station/stationGpsByName.html', stationByName=stationByName, station_gps=station_gps, lowStaionByUid=lowStaionByUid)

@bp.route('/lowStaionByUid', methods=['POST'])
def lowStaionByUid():
    arsId = request.form['arsId']
    lowStaionByUid: mo.LowStaionByUid = service_sj.getLowStaionByUidList(arsId)
    stSrch = lowStaionByUid[0].stnNm
    stationByName: mo.StationByName = service_sj.getStationByName(stSrch)
    tmX = str(stationByName.tmX)
    tmY = str(stationByName.tmY)
    radius = str(50)  # 반경
    station_gps: mo.Station_gps = service_sj.getStationByPosInfo(tmX, tmY, radius)

    # 뷰페이지에 전달할 값
    return render_template('station/LowStaionByUidList.html', lowStaionByUid=lowStaionByUid, station_gps=station_gps)