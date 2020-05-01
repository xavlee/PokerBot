"""poker192 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from core.views import splash, board, check, bet, fold, accounts
from core.views import load_game, new_game, new_hand, call

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', splash, name='splash'),
    path('board', board, name='board'),
    path('check', check, name='check'),
    path('accounts', accounts, name='accounts'),
    path('bet', bet, name='bet'),
    path('fold', fold, name='fold'),
    path('loadgame', load_game, name='load_game'),
    path('newgame', new_game, name='new_game'),
    path('newhand', new_hand, name='new_hand'),
    path('call', call, name='call')
]
