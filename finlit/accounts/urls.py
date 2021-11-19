from django.urls import path
from . import views
urlpatterns = [
    path("register",views.register,name="register"),
    path("login",views.login,name="login"),
    path("logout",views.logout,name="logout"),
    path("start",views.start,name="start"),
    path("about",views.about,name="about"),
    path("start/prof_ch",views.prof_ch,name="prof_ch"),
    # path("start/prof_ch/advice",views.advice,name="advice"),
    # path("start/prof_ch/confirm_inv/advice",views.advice,name="advice2"),
    path("start/prof_ch/withdraw",views.withdraw,name="withdraw"),
    path("start/prof_ch/confirm_wd",views.confirm_wd,name="confirm_wd"),
    path("start/prof_ch/invest",views.invest,name="invest"),
    path("start/prof_ch/confirm_inv",views.confirm_inv,name="confirm_inv"),
    path("",views.index,name="index")
]
