from django.urls import path
from . import views

# this like app.use() in express
urlpatterns = [
path('', views.Home.as_view(), name="home"),
path('about/', views.About.as_view(), name="about"),
path('artists/', views.ArtistList.as_view(), name="artist_list"),
path('artists/new/', views.ArtistCreate.as_view(), name="artist_create"),
path('artists/<int:pk>/', views.ArtistDetail.as_view(), name="artist_detail"),
path('artists/<int:pk>/update',views.ArtistUpdate.as_view(), name="artist_update"),
path('artists/<int:pk>/delete', views.ArtistDelete.as_view(), name="artist_delete"),
path('artists/<int:pk>/artworks/new/', views.ArtworksCreate.as_view(), name="artworks_create"),
path('artgallerys/<int:pk>/artworks/<int:artworks_pk>/', views.ArtgalleryArtworksAssoc.as_view(), name="artgallery_artworks_assoc"),
]