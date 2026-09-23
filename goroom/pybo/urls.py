from django.urls import path
from . import views
from .views import PyboView

app_name = 'pybo'  # namespace 설정

urlpatterns = [
    path('', views.index, name='index'),
    path('pybo/', views.mainscreen, name='mainscreen'),
    path('pybo/', PyboView.as_view(), name='pybo'),
    path('about.html', views.about, name='about'),
    path('blog.html', views.blog, name='blog'),
    path('csv-data/', views.csv_data, name='csv_data'),
    path('api/favorite/add/', views.add_favorite, name='add_favorite'),
    path('api/favorite/list/', views.list_favorites, name='list_favorites'),
    path('myfavorites/', views.my_favorites_page, name='my_favorites_page'),
    path('api/favorite/remove/<int:favorite_id>/', views.remove_favorite, name='remove_favorite'),
]