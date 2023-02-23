from django.urls import path

from mainapp import views
from mainapp.apps import MainappConfig
from django.views.decorators.cache import cache_page

app_name = MainappConfig.name

urlpatterns = [
    path("", views.MainPageView.as_view(), name="main_page"),
    path("news/", views.NewsPageView.as_view(), name="news"),
    path("news/create/", views.NewsCreateView.as_view(), name="news_create"),
    path("news/<int:page>", views.NewsPageView.as_view(), name="news_pagen"),
    path("news/<int:pk>/detail", views.NewsDetailView.as_view(), name="news_detail"),
    path("news/<int:pk>/update", views.NewsUpdateView.as_view(), name="news_update"),
    path("news/<int:pk>/delete", views.NewsDeleteView.as_view(), name="news_delete"),
    path("courses/", cache_page(60 * 5)(views.CoursesPageView.as_view()), name="courses"),
    path("courses/<int:page>", views.CoursesPageView.as_view(), name="courses_pagen"),
    path("courses/<int:course_id>/detail", views.CoursesDetailPageView.as_view(), name="courses_detail"),
    path("course_feedback/", views.CourseFeedbackFormProcessView.as_view(), name="course_feedback"),
    path("contacts/", views.ContactsPageView.as_view(), name="contacts"),
    path("doc_site/", views.DocSitePageView.as_view(), name="doc_site"),
    path("log_view/", views.LogView.as_view(), name="log_view"),
    path("log_download/", views.LogDownloadView.as_view(), name="log_download"),
]
