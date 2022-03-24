import requests
from pprint import pprint
import json


def getmaxminavgtemp(res_ans, index):

    max_temp = res_ans['weather'][index]['maxtempC']
    min_temp = res_ans['weather'][index]['mintempC']
    avg_temp = res_ans['weather'][index]['avgtempC']
    return max_temp, min_temp, avg_temp


def gettimeandtemp(res_ans, index):

    time, temp, weather_stat, chance_of_rain = [], [], [], []
    for i in range(len(res_ans['weather'][index]['hourly'])):
        time.append(res_ans['weather'][index]['hourly'][i]['time'])
        temp.append(res_ans['weather'][index]['hourly'][i]['tempC'])
        weather_stat.append(res_ans['weather'][index]
                            ['hourly'][i]['weatherDesc'][0]['value'])
        chance_of_rain.append(
            float(res_ans['weather'][index]['hourly'][i]['chanceofrain']))

    return time, temp, weather_stat, chance_of_rain


def getcurrentstatus(res_ans):

    temp = res_ans['current_condition'][0]['temp_C']
    humidity = res_ans['current_condition'][0]['humidity']
    pressure = res_ans['current_condition'][0]['pressure']
    desc = res_ans['current_condition'][0]['weatherDesc'][0]['value']
    obsdate = res_ans['current_condition'][0]['localObsDateTime'].split(' ')[0]

    return temp, humidity, pressure, desc, obsdate


def getdata(city):

    url = 'https://wttr.in/{}?format=j1'.format(city)
    res = requests.get(url).json()

    # the response object will not be iterable/subscriptable so we need to convert it into json

    res_save = json.dumps(res)

    # loading the json using dumps

    res_ans = json.loads(res_save)

    return res_ans


def getfinalresult(res_ans):

    dates = [res_ans['weather'][i]['date']
             for i in range(len(res_ans['weather']))]

    date_map = {dates[i]: {} for i in range(len(dates))}

    temp_current, humidity_current, pressure_current, desc_current, obsdate_current = getcurrentstatus(
        res_ans)

    start = 0
    stop = len(res_ans['weather'])

    while start < stop:

        max_temp, min_temp, avg_temp = getmaxminavgtemp(res_ans, start)

        date_map[dates[start]]['max_temp'] = max_temp
        date_map[dates[start]]['min_temp'] = min_temp
        date_map[dates[start]]['avg_temp'] = avg_temp

        time_sec, temp_sec, weather_stat, chance_of_rain = gettimeandtemp(
            res_ans, start)
        date_map[dates[start]]['time_sec'] = time_sec
        date_map[dates[start]]['temp_sec'] = temp_sec
        date_map[dates[start]]['weather_status'] = weather_stat
        date_map[dates[start]]['chance_of_rain'] = chance_of_rain

        start += 1

    return temp_current, humidity_current, pressure_current, desc_current, obsdate_current, date_map
