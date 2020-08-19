from django.urls import path
from . import views

app_name = 'prokart'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    # path('<int:pk>/detail/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/review/', views.voting, name='voting'),
    path('<int:pk>/create_comment/', views.CreateCommentForm.as_view(), name='comment'),
    path('ram_selection/', views.ram_filter, name='ram'),
    path('storage_selection/', views.storage_filter, name='storage'),
    path('display_selection/', views.display_filter, name='display'),
    path('price_selection/', views.price_filter, name='price'),

]
