from django.urls import path
from battle.apis.views import get


urlpatterns = [
    path('get/<str:battleuuid>/',get.GetBattleView),
    
]