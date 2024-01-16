from django.urls import path
from commerce import views


'''
Hover on the functions to see their purpose.
'''
urlpatterns=[
    path('item/add/',views.upsertItem,name="upsertItem"),
    path('address/add/',views.upsertAddress,name="upsertAddress"),
    path('hasaddress/',views.hasAddress,name="hasaddress"),
    path('address/get/',views.getAddress,name="getaddress"),
    path('payment/make/',views.makeTransaction,name="makePayment"),
    path('payment/search/',views.filterTransaction,name="filterPayment")
]