from django.shortcuts import render
from darksky import forecast
from datetime import date,timedelta,datetime
from ipstack import GeoLookup

def home(request):
    geolookup=GeoLookup('ba3495a30c658700b23916512f93eef0')
    location=geolookup.get_own_location()
    lat=location['latitude']
    lng=location['longitude']
    region=location['region_name']

    city=lat,lng
    weekday=date.today()

    weatherdaily={}

    with forecast('af01e6071f266c8191d8446298b7f097',*city) as country:
        for d in country.daily:

            d=dict(date=weekday,day=date.strftime(weekday,'%d/%m/%Y  %A'),sum=d.summary,tempmin=(((d.temperatureMin-32)*5)/9),
                   tempmax=(((d.temperatureMax-32)*5)/9))

            print('{date}----{day}-----{sum}---{tempmin}----{tempmax}'.format(**d))
            tmin=str(round(float('{tempmin}'.format(**d))))
            tmax=str(round(float('{tempmax}'.format(**d))))
            summary='{sum}'.format(**d).lower()
            weekday += timedelta(days=1)

            pic=''

            if 'partly cloudy' in summary:
                pic='partly-cloudy-day.png'
            if 'drizzle' in summary:
                pic='rain.png'
            if 'rain' in summary:
                pic='rain.png'
            if 'Rain' in summary:
                pic='rain.png'
            if 'cloudy' in summary:
                pic='clouds.png'
            if 'clear' in summary:
                pic='sun.png'
            if 'humid and overcast throughout the day' in summary:
                pic='clouds.png'

            weatherdaily.update({'{day}'.format(**d):
                                     {'MinTemp': '{}'.format(tmin),
                                      'MaxTemp':
                                          '{}'.format(tmax), 'pic': pic}})



    hour=datetime.now().hour
    location=forecast('af01e6071f266c8191d8446298b7f097',*city)
    i=0
    hourly_weather={}
    while hour<=24:
        t=round(location.hourly[i].temperature)
        sammary=location.hourly[i].summary.lower()

        pic = ''

        if 'drizzle' in sammary:
            pic = 'rain.png'
        if 'rain' in sammary:
            pic='rain.png'
        if 'Rain' in sammary:
            pic='rain.png'
        if 'cloudy' in sammary:
            pic='clouds.png'
        if 'overcast' in sammary:
            pic='clouds.png'
        if 'humid' in sammary:
            pic='clouds.png'
        if 'clear' in sammary:
            pic='sun.png'
        if 'partly cloudy' in sammary:
            pic='partly-cloudy-day.png'


        temp=round(((t-32)/9)*5)
        if hour<12:
            hour_=f'{hour}am'
            print(f'{hour}am---{temp}--{sammary}')
        elif hour==12:
            hour_ = f'{hour}pm'
            print(f'{hour}pm---{temp}--{sammary}')

        else:
            hour_ = f'{hour-12}pm'
            print(f'{hour-12}pm---{temp}--{sammary}')
        hourly_weather.update({hour_:{'pic':pic,'temp':temp}})
        i+=1
        hour+=1
    tn=round(location.hourly[0].temperature)
    tnf=round(((tn-32)/9)*5)
    tempnow={'nowtemp':tnf}


    return render(request,'home.html',
                  {'weekly_weather':weatherdaily,
                  'hourlyweather':hourly_weather,
                   'current_temp':tempnow,
                   'region_own':region})






# Create your views here.
