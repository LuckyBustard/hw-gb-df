from django.views.generic import TemplateView
from mainapp import models as mainapp_models
from django.http import Http404


class MainPageView(TemplateView):
    template_name = "mainapp/templates/index.html"


class NewsPageView(TemplateView):
    template_name = "mainapp/templates/news.html"

    def get_context_data(self, page=1, **kwargs):
        context = super().get_context_data(**kwargs)
        start = (page - 1) * 5
        stop = start + 5
        context["page_num"] = page
        context["news_items"] = mainapp_models.News.objects.order_by('-updated').all()[start:stop]
        return context


class NewsDetailPageView(TemplateView):
    template_name = "mainapp/templates/news_detail.html"

    def get_context_data(self, news_id, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['news_detail'] = mainapp_models.News.objects.get(pk=news_id)
            return context
        except:
            raise Http404("Новость не найдена")


class CoursesPageView(TemplateView):
    template_name = "mainapp/templates/courses_list.html"

    def get_context_data(self, page=1, **kwargs):
        context = super().get_context_data(**kwargs)
        start = (page - 1) * 6
        stop = start + 6
        context["page_num"] = page
        context["courses"] = mainapp_models.Courses.objects.all()[start:stop]
        return context


class CoursesDetailPageView(TemplateView):
    template_name = "mainapp/templates/courses_detail.html"

    def get_context_data(self, course_id, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['course_detail'] = mainapp_models.Courses.objects.get(pk=course_id)
            print(context['course_detail'].__dict__)
            return context
        except:
            raise Http404("Курс не найден")


class ContactsPageView(TemplateView):
    template_name = "mainapp/templates/contacts.html"


class DocSitePageView(TemplateView):
    template_name = "mainapp/templates/doc_site.html"


class LoginPageView(TemplateView):
    template_name = "mainapp/templates/login.html"
