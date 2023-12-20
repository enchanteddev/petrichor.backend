from django.urls import path
from . import views

urlpatterns = [
    path('login/',views.user_login,name="login"),
    path('register/', views.signup, name="signup"),
    path('logout/',views.user_logout,name="logout"),
    path('whoami/',views.whoami,name="whoami"),
    path('events/apply',views.apply_event_paid ,name="applyEvent"),
    path('send_grievance',views.send_grievance,name="send_grievance")
]
