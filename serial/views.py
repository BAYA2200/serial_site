from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views import View
from django.views.generic import DetailView
from rest_framework import generics, status, request
from django.shortcuts import render, get_object_or_404
from .models import TVShow, Episode

from rest_framework import status
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated, BasePermission
from django.shortcuts import get_object_or_404

from .forms import EpisodeSelectionForm
from .models import TVShow, Episode
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import TVShow, Genre, Comment
from .serializer import TVShowSerializer, CommentSerializer


class TVShowViewSet(generics.ListAPIView):
    serializer_class = TVShowSerializer

    def get_queryset(self):
        query = self.request.GET.get('q')
        genres = self.request.GET.getlist('genre')

        queryset = TVShow.objects.all()

        if query:
            queryset = queryset.filter(title__icontains=query)

        if genres:
            genre_filters = Q()
            for genre in genres:
                genre_filters |= Q(genres__name=genre)
            queryset = queryset.filter(genre_filters)

        return queryset.distinct()  # Use distinct() to remove duplicate results

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAdminUser()]

    def list(self, request, *args, **kwargs):
        tvshows = self.get_queryset()
        is_search = bool(request.GET.get('q'))
        all_genres = Genre.objects.values_list('name', flat=True)

        return render(request, 'tvshow_list.html',
                      {'tvshows': tvshows, 'is_search': is_search, 'all_genres': all_genres})


class TVShowDetailView(View):
    def get(self, request, pk):
        tvshow = get_object_or_404(TVShow, pk=pk)
        episodes = Episode.objects.filter(tvshow=tvshow).order_by('episode_number')

        paginator = Paginator(episodes, 1)  # По одной серии на страницу
        page_number = request.GET.get('page')
        page = paginator.get_page(page_number)

        return render(request, 'tvshow_detail.html', {'tvshow': tvshow, 'page': page})


def watch_episode_user(request, tvshow_id, episode_number):
    print("Entering watch_episode_user view")
    tvshow = get_object_or_404(TVShow, id=tvshow_id)
    episode = get_object_or_404(Episode, tvshow=tvshow, episode_number=episode_number)

    print(f"TV Show: {tvshow.title}, Episode: {episode.title}")

    return render(request, 'watch_episode_user.html', {'tvshow': tvshow, 'episode': episode})


# def watch_episode_user(request, tvshow_id, episode_number):
#     tvshow = get_object_or_404(TVShow, id=tvshow_id)
#     episode = get_object_or_404(Episode, tvshow=tvshow, episode_number=episode_number)
#
#     return render(request, 'watch_episode_user.html', {'tvshow': tvshow, 'episode': episode})


# class TVShowDetailView(View):
#     def get(self, request, pk):
#         tvshow = get_object_or_404(TVShow, pk=pk)
#         comments = Comment.objects.filter(tvshow=tvshow)  # Get comments for this TV show
#         return render(request, 'tvshow_detail.html', {'tvshow': tvshow})
# class TVShowDetailView(View):
#     def get(self, request, pk):
#         tvshow = get_object_or_404(TVShow, pk=pk)
#         return render(request, 'tvshow_detail.html', {'tvshow': tvshow})
#


# class TVShowDetail(DetailView):
#     model = TVShow
#     template_name = 'tvshow_detail.html'
#
#
# def watch_episode(request, pk):
#     tvshow = get_object_or_404(TVShow, pk=pk)
#     selected_episode_id = request.POST.get('episode')  # Получаем ID выбранного эпизода
#     selected_episode = get_object_or_404(Episode, id=selected_episode_id)
#
#     return render(request, 'watch_episode.html', {'tvshow': tvshow, 'selected_episode': selected_episode})


class CreateCommentAPIView(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, tvshow_id):
        try:
            tvshow = get_object_or_404(TVShow, id=tvshow_id)
            serializer = CommentSerializer(data=request.data)

            if serializer.is_valid():
                # Установите пользователя и сериал перед сохранением
                serializer.validated_data['user'] = request.user
                serializer.validated_data['tvshow'] = tvshow

                serializer.save()

                # Получите URL-адрес страницы деталей сериала
                tvshow_detail_url = reverse('tvshow_detail', kwargs={'pk': tvshow_id})

                # Перенаправьте на страницу деталей сериала после успешного создания комментария
                return redirect(tvshow_detail_url)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except TVShow.DoesNotExist:
            return Response({'error': 'TVShow not found'}, status=status.HTTP_404_NOT_FOUND)

    # def post(self, request, tvshow_id):
    #     try:
    #         tvshow = get_object_or_404(TVShow, id=tvshow_id)
    #         serializer = CommentSerializer(data=request.data)
    #
    #         if serializer.is_valid():
    #             # Установите пользователя и сериал перед сохранением
    #             serializer.validated_data['user'] = request.user
    #             serializer.validated_data['tvshow'] = tvshow
    #
    #             serializer.save()
    #             return Response(serializer.data, status=status.HTTP_201_CREATED)
    #
    #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #
    #     except TVShow.DoesNotExist:
    #         return Response({'error': 'TVShow not found'}, status=status.HTTP_404_NOT_FOUND)
