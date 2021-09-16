from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
from .feeds import LatestPostsFeed

app_name = 'blog'


urlpatterns = [
	path('', views.post_list, name='post_list'),
	# path('', views.PostListViews.as_view(), name='post_list'),
	path('<int:year>/<int:month>/<int:day>/<slug:post>/',
		 views.post_detail, 
		 name='post_detail'),
	path('<int:post_id>/share/', views.post_share, name='post_share'),
	path('tag/<slug:tag_slug>/', views.post_list, name='post_list_by_tag'),
	path('feed/', LatestPostsFeed(), name='post_feed'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)