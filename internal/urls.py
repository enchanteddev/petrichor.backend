from django.urls import path
from . import views

urlpatterns = [
    path('events/',views.getEventUsers ,name="event"),
    path('verifyTR',views.verifyTR,name="verifyTR"),
    path('events/unconfirmed',views.getUnconfirmed ,name="unconfirmed"),
    path('event/add/',views.addEvent,name="addEvent")
]
