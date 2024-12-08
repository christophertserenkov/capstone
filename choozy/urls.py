from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views


router = DefaultRouter()
router.register(r'room', views.RoomViewSet)


urlpatterns = [
    path('', views.index, name='index'),
    path('rooms', views.rooms, name='rooms'),
    path('api/', include(router.urls)),
    path('api/room/<int:room_id>/players', views.players_in_room, name='playerapi'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('register', views.register, name='register'),
    path('create', views.create_room, name='create'),
    path('room_admin/<int:room_id>', views.room_admin, name='room_admin'),
    path('room_admin/close/<int:room_id>', views.close_room, name='close'),
    path('join/<int:room_id>', views.join, name='join'),
    path('room/<int:room_id>', views.room, name='room'),
    path('room/results/<int:room_id>', views.results, name='results')
]