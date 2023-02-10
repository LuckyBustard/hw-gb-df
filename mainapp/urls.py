from django.urls import path

from mainapp import views
from mainapp.apps import MainappConfig

app_name = MainappConfig.name

urlpatterns = [
    path("", views.MainPageView.as_view(), name="main_page"),
    path("news/", views.NewsPageView.as_view(), name="news"),
    path("news/<int:page>", views.NewsPageView.as_view(), name="news_pagen"),
    path("news/detail/<int:news_id>", views.NewsDetailPageView.as_view(), name="news_detail"),
    path("courses/", views.CoursesPageView.as_view(), name="courses"),
    path("courses/<int:page>", views.CoursesPageView.as_view(), name="courses_pagen"),
    path("courses/detail/<int:course_id>", views.CoursesDetailPageView.as_view(), name="courses_detail"),
    path("contacts/", views.ContactsPageView.as_view(), name="contacts"),
    path("doc_site/", views.DocSitePageView.as_view(), name="doc_site"),
]


