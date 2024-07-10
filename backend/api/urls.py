from django.urls import path,include

urlpatterns = [
    # Accounts
    path('accounts/',include('accounts.urls')),
    path('notification/',include('notification.urls')),
]
