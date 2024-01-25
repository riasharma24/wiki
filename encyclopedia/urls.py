from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('wiki/<str:entry>', views.display, name='display'),
    path('search', views.search, name='search'),
    path('new',views.new, name='new'),
    path('edit', views.edit, name='edit'),
    path('save_changes',views.save_changes, name='save_changes'),
    path('random',views.random_page,name='random_page')
]
