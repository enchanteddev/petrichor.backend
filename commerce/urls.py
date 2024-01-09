from django.urls import path
from commerce import views


'''
Hover on the functions to see their purpose.
'''
urlpatterns=[
    path('item/add/',views.upsertItem,name="upsertItem"),
    path('payment/make/',views.makeTransaction,name="makePayment"),
    path('address/add/',views.addAddress,name="addAddress"),
    path('hasaddress/',views.hasAddress,name="hasaddress"),
    path('address/get/',views.getAddress,name="getaddress"),
    path('payment/search/',views.filterTransaction,name="filterPayment")
]