from django.urls import path
from . import views
from .views import CreateCommentAPIView

urlpatterns = [
    path('', views.TVShowViewSet.as_view(), name='tvshow_list'),
    path('tvshow/<int:pk>/', views.TVShowDetailView.as_view(), name='tvshow_detail'),
    path('tvshows/<int:tvshow_id>/comments/', views.CreateCommentAPIView.as_view(), name='create_comment'),
    path('tvshow/<int:tvshow_id>/watch/<int:episode_number>/user/', views.watch_episode_user, name='watch_episode_user')

]

