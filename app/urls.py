from django.urls import path
from . import views
from .  import views2


urlpatterns = [
    path("", views2.questions_feed_new, name='app-feed-new'),
    path("hot/", views.questions_feed_hot, name='app-feed-hot'),
    path("signup/", views.registration, name='app-signup'),
    path("login/", views.authorization, name='app-login'),
    path("ask/", views.new_question, name='app-ask'),
    path("question/<int:id>/", views.answers, name='app-question'),
    path("tag/<str:tag>/", views.questions_feed_by_tag, name='app-feed-by-tag'),
]