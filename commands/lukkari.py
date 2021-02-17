import requests, json
from datetime import datetime
from datetime import timedelta
from utils import createEmbed

async def execute(msg, args):
    today = datetime.strftime(datetime.now(), '%Y-%m-%d')
    nextWeek = datetime.strftime(datetime.now() + timedelta(days=7), '%Y-%m-%d')
    payload = {"dateFrom":today,"dateTo":nextWeek,"eventType":"visible"}
    url = 'https://lukkari.turkuamk.fi'
    data = {}

    with requests.Session() as s:
        try:
            r1 = s.post('https://lukkari.turkuamk.fi/rest/groups', data=json.dumps({"target":"group","type":"name","text":"ptivis20e","dateFrom":"","dateTo":"","filters":[],"show":True}))
        except Exception as e:
            return await msg.channel.send("Error: Could not get the data requested. Seems like a problem on their side.")

        cookie = {'PHPSESSID': requests.utils.dict_from_cookiejar(s.cookies)['PHPSESSID']}
        r2 = s.post('https://lukkari.turkuamk.fi/rest/basket/0/group/PTIVIS20E', data=json.dumps({}), cookies=cookie)
        r3 = s.post('https://lukkari.turkuamk.fi/rest/basket/0/events', data=json.dumps(payload), cookies=cookie)
        data = r3.json()
        data2 = sortDataByDay(data)

    t = 'Lukujärjestys'
    fields = []

    for day in data2:
        daysLessons = ''
        for lesson in data2[day]:
            daysLessons += f"{lesson['startTime']} - {lesson['endTime']}: {lesson['subject']}\n"

        formatedDay = datetime.strftime(datetime.strptime(day, '%Y-%m-%d'), '%a %d.%m.%Y')
        fields.append({'name': formatedDay, 'value': daysLessons})

    embed = createEmbed(title=t, fields=fields, thumbnail='https://pics.freeicons.io/uploads/icons/png/8938216821547546487-512.png')
    await msg.channel.send(embed=embed)

def sortDataByDay(data):
    list = {}
    for lesson in data:
        startDate,startTime = lesson['start_date'].split(' ')
        endDate,endTime = lesson['end_date'].split(' ')
        subject = lesson['subject']

        # print(list)
        if not startDate in list.keys():
            list[startDate] = []

        lessonData = { "startTime": startTime, "endTime": endTime, "subject": subject }
        list[startDate].append(lessonData)

    return list


commandData = {
    "name": "lukkari",
    "description": "Palauttaa viikon lukujärjestyksen",
    "author": "kripi",
    "execute": lambda msg,arguments,*args : execute(msg, arguments) # katso ping.py:stä selitys *args-argumentille
}
