from django.urls import path
from .views import *  
from django.contrib.auth.views import LogoutView
from base import views
from . import views
from .views import CustomLoginView

# handler400 = custom_error_400
# handler403 = custom_error_403
# handler404 = custom_error_404
# handler500 = custom_error_500
# Create your views here.
urlpatterns=[
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', RegisterPage.as_view(), name='register'),
    path('', TaskList.as_view(), name='tasks'),
    path('task/<int:pk>', TaskDetail.as_view(), name='task'),
    path('task-create', TaskCreate.as_view(), name='task-create'),
    path('task-update/<int:pk>', TaskUpdate.as_view(), name='task-update'),
    path('task-delete/<int:pk>', DeleteView.as_view(), name='task-delete'),
]