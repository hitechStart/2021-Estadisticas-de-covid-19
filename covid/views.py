from django.shortcuts import render
import requests

import json
from datetime import date, timedelta


def index(request):
  url_history = "https://covid-193.p.rapidapi.com/history"
  url_statistics= 'https://covid-193.p.rapidapi.com/statistics'

  headers= {
      'x-rapidapi-host': 'covid-193.p.rapidapi.com',
      'x-rapidapi-key': '759433ef01mshbc4aa8ca8c5d9dfp10c8b8jsn03b7ec7aa3a6'
    }

  today =date.today()
      
  response = requests.request("GET", url_statistics, headers=headers).json()
  allStatistics = response["response"]

  countries = [ dato['country'] for dato in allStatistics ] # lista por compresion
  countries.sort()

  if request.method=='POST':

    sel_country = request.POST['selectedcountry']
    pointStartDate = date.today() - timedelta( days= 6)
    yearUTC= int('{}'.format(pointStartDate.year))
    monthUTC = int('{}'.format(pointStartDate.month)) -1
    dayUTC = int('{}'.format(pointStartDate.day))
    week_cases =[]
    week_deaths =[]
        
    for i in range(7):
              day = pointStartDate + timedelta( days= i)
              querystring = { "country": sel_country ,"day": day }
              response = requests.request("GET", url_history, headers=headers, params=querystring).json()
              response = response['response']
              if response:
                  response = response[len(response)-1]
                  week_cases.append(int(response['cases']['new']))  
                  if response['deaths']['new']:
                      week_deaths.append(int(response['deaths']['new']))   
                  else :
                      week_deaths.append(0)        
          
          
    for i in allStatistics:
              if sel_country == i['country']:
                  new = i['cases']['new'] if i['cases']['new'] else '-'
                  active = i['cases']['active'] if i['cases']['active'] else '-'
                  critical = i['cases']['critical'] if i['cases']['critical'] else '-'
                  recovered = i['cases']['recovered'] if i['cases']['recovered'] else '-'
                  total = i['cases']['total'] if i['cases']['total'] else '-'
                  deaths = int(total) - int(active) - int(recovered)

    context = {
              'yearUTC': yearUTC,
              'monthUTC': monthUTC,
              'dayUTC': dayUTC,
              'new': new,
              'total': total,
              'active': active,
              'deaths': deaths,
              'critical': critical,
              'countries': countries,
              'recovered': recovered,
              'week_cases': week_cases,
              'week_deaths': week_deaths,
              'sel_country': sel_country
          }
    return render(request, 'covid/index.html', context=context)

  return render(request, 'covid/index.html', {'countries': countries })