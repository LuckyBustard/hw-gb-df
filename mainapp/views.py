from django.views.generic import TemplateView
from datetime import datetime
import json

class MainPageView(TemplateView):
    template_name = "mainapp/templates/index.html"


class NewsPageView(TemplateView):
    template_name = "mainapp/templates/news.html"

    def get_context_data(self, page=1, **kwargs):
        start = (page - 1) * 5
        stop = start + 5
        context = super().get_context_data(**kwargs)
        context["page_num"] = page
        context["news_items"] = []
        with open('mainapp/data/news.json') as news_file:
            news_items = json.load(news_file)
            for news_item in news_items[start:stop]:
                news_item["date"] = datetime.strptime(news_item['date'], "%Y-%m-%d %H-%M-%S")
                context["news_items"].append(news_item)
        return context


class CoursesPageView(TemplateView):
    template_name = "mainapp/templates/courses_list.html"


class ContactsPageView(TemplateView):
    template_name = "mainapp/templates/contacts.html"


class DocSitePageView(TemplateView):
    template_name = "mainapp/templates/doc_site.html"


class LoginPageView(TemplateView):
    template_name = "mainapp/templates/login.html"