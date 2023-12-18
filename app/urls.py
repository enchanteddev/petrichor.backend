from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name = "home"),
    path('login/',views.user_login,name="login"),
    path('register/', views.signup, name="signup"),
    path('logout/',views.user_logout,name="logout"),
    path('whoami/',views.whoami,name="whoami"),
    # path('mt/',views.mailtest ,name="mailtest"),
    path('events/apply',views.apply_event ,name="applyEvent"),
    path('events/',views.getEventUsers ,name="event"),
    path('verifyTR',views.verifyTR,name="verifyTR"),
    path('send_grievance',views.send_grievance,name="send_grievance"),
    path('events/unconfirmed',views.getUnconfirmed ,name="unconfirmed"),
]
