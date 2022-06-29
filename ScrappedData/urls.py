from django.urls import path, include
from . views import RegisterPage, CustomLoginView, query_page, saved_for_later, pagelogout




urlpatterns = [
    path('register/', RegisterPage.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('query_page/', query_page, name='query_page'),
    path('saved/', saved_for_later, name='saved' ),
    path('logout/', pagelogout, name='logout')
]
