from django.urls import path, include

from rest_framework.routers import DefaultRouter

from subjects import views

router = DefaultRouter()
router.register('tarot-club', views.HelloTarotViewSet, basename='hello-tarot-viewset')
router.register('tarot-subject-profiles', views.TarotCardViewSet)
router.register('tarot-club-news', views.ProfileFeedItemViewSet)

urlpatterns = [
    path('hello-world-view/', views.HelloApiView.as_view()),
    path('login/', views.LoginView.as_view()),
    path('', include(router.urls)),
]