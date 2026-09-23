import requests
from datetime import datetime

from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required

from .models import Favorite
from .data import apartment_data


def get_weather():
    try:
        api_key = '90c3617bbf6db56d1be1c2c56e7d26bc'
        city = 'Seoul'
        url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric&lang=kr'
        response = requests.get(url, timeout=10)
        data = response.json()

        return {
            'temperature': data['main']['temp'],
            'fell_temperature': data['main']['feels_like'],
            'humidity': data['main']['humidity'],
            'wind_speed': data['wind']['speed'],
            'icon': f"http://openweathermap.org/img/wn/{data['weather'][0]['icon']}@2x.png"
        }
    except Exception as e:
        print(f"날씨 API 오류: {e}")
        return None


def get_exchange_rate():
    service_key = 'NSx49LkjshbR6WSNwDVMl2f5BNLlDOYz'
    today = datetime.now()
    today_str = today.strftime('%Y%m%d')

    def fetch(date):
        url = (
            f"https://www.koreaexim.go.kr/site/program/financial/exchangeJSON?"
            f"authkey={service_key}&searchdate={date}&data=AP01"
        )
        res = requests.get(url, timeout=10, verify=False)
        res.raise_for_status()
        return res.json()

    try:
        data = fetch(today_str)
        if not data:
            return None, today.strftime('%Y년 %m월 %d일 기준')

        rates = {'usd': '', 'eur': '', 'jpy': ''}
        for item in data:
            if 'USD' in item['cur_unit']:
                rates['usd'] = item['deal_bas_r']
            elif 'EUR' in item['cur_unit']:
                rates['eur'] = item['deal_bas_r']
            elif 'JPY' in item['cur_unit']:
                rates['jpy'] = item['deal_bas_r']

        return rates, today.strftime('%Y년 %m월 %d일 기준')

    except Exception as e:
        print(f"API 오류: {e}")
        return None, today.strftime('%Y년 %m월 %d일 기준')


def index(request):
    exchange, base_date_str = get_exchange_rate()
    weather = get_weather()

    show_exchange = exchange is not None

    return render(request, 'pybo/index.html', {
        'exchange': exchange,
        'base_date': base_date_str,
        'show_exchange': show_exchange,
        'temperature': weather['temperature'] if weather else None,
        'fell_temperature': weather['fell_temperature'] if weather else None,
        'humidity': weather['humidity'] if weather else None,
        'wind_speed': weather['wind_speed'] if weather else None,
        'icon': weather['icon'] if weather else None,
    })


def mainscreen(request):
    return render(request, 'pybo/mainscreen.html')


def about(request):
    return render(request, 'about.html')

def blog(request):
    return render(request, 'blog.html')


def graph_view(request):
    exchange, base_date = get_exchange_rate()
    return render(request, 'pybo/mainscreen.html', {'exchange': exchange, 'base_date': base_date})


def csv_data(request):
    data = apartment_data()
    return JsonResponse(data, safe=False)


@login_required
def add_favorite(request):
    if request.method == 'POST':
        title     = request.POST.get('title')
        location  = request.POST.get('location')
        price     = request.POST.get('price')
        image_url = request.POST.get('image_url')

        if Favorite.objects.filter(
            user=request.user,
            title=title,
            location=location,
            price=price,
            image_url=image_url
        ).exists():
            return JsonResponse({
                'status': 'error',
                'message': '이미 즐겨찾기에 저장되어 있습니다.'
            })

        Favorite.objects.create(
            user=request.user,
            title=title,
            location=location,
            price=price,
            image_url=image_url
        )
        return JsonResponse({'status': 'success'})

    return JsonResponse({
        'status': 'error',
        'message': '잘못된 요청입니다.'
    }, status=400)


@login_required
def list_favorites(request):
    favorites = Favorite.objects.filter(user=request.user)
    data = list(favorites.values())
    return JsonResponse(data, safe=False)


@login_required
def my_favorites_page(request):
    favorites = Favorite.objects.filter(user=request.user)
    return render(request, 'pybo/my_favorites.html', {'favorites': favorites})


@login_required
def remove_favorite(request, favorite_id):
    favorite = get_object_or_404(Favorite, id=favorite_id, user=request.user)
    favorite.delete()
    return redirect('pybo:my_favorites_page')


class PyboView(LoginRequiredMixin, TemplateView):
    template_name = 'pybo.html'
    login_url = '/common/login/'
