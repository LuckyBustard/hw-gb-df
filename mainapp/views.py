from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, TemplateView, UpdateView
from mainapp import forms as mainapp_forms
from mainapp import models as mainapp_models
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.http import Http404


class MainPageView(TemplateView):
    template_name = "mainapp/index.html"


class NewsPageView(TemplateView):
    template_name = "mainapp/news_list.html"

    def get_context_data(self, page=1, **kwargs):
        context = super().get_context_data(**kwargs)
        start = (page - 1) * 5
        stop = start + 5
        context["page_num"] = page
        context["news_items"] = mainapp_models.News.objects.order_by('-updated').all()[start:stop]
        return context


class NewsDetailPageView(TemplateView):
    template_name = "mainapp/news_detail.html"

    def get_context_data(self, pk, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['news_detail'] = mainapp_models.News.objects.get(pk=pk)
            return context
        except:
            raise Http404("Новость не найдена")


class CoursesPageView(TemplateView):
    template_name = "mainapp/courses_list.html"

    def get_context_data(self, page=1, **kwargs):
        context = super().get_context_data(**kwargs)
        start = (page - 1) * 6
        stop = start + 6
        context["page_num"] = page
        context["courses"] = mainapp_models.Courses.objects.all()[start:stop]
        return context


class CoursesDetailPageView(TemplateView):
    template_name = "mainapp/courses_detail.html"

    def get_context_data(self, course_id, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['course_detail'] = mainapp_models.Courses.objects.get(pk=course_id)
        except:
            raise Http404("Курс не найден")

        context["lessons"] = mainapp_models.Lesson.objects.filter(course=context["course_detail"])
        context["teachers"] = mainapp_models.CourseTeachers.objects.filter(course=context["course_detail"])
        if not self.request.user.is_anonymous:
            if not mainapp_models.CourseFeedback.objects.filter(
                    course=context["course_detail"], user=self.request.user
            ).count():
                context["feedback_form"] = mainapp_forms.CourseFeedbackForm(
                    course=context["course_detail"], user=self.request.user
                )
        context["feedback_list"] = mainapp_models.CourseFeedback.objects.filter(
            course=context["course_detail"]
        ).order_by("-created", "-rating")[:5]
        return context


class CourseFeedbackFormProcessView(LoginRequiredMixin, CreateView):
    model = mainapp_models.CourseFeedback
    form_class = mainapp_forms.CourseFeedbackForm

    def form_valid(self, form):
        self.object = form.save()
        rendered_card = render_to_string("mainapp/includes/feedback_card.html", context={"item": self.object})
        return JsonResponse({"card": rendered_card})


class ContactsPageView(TemplateView):
    template_name = "mainapp/contacts.html"


class DocSitePageView(TemplateView):
    template_name = "mainapp/doc_site.html"


class NewsCreateView(PermissionRequiredMixin, CreateView):
    model = mainapp_models.News
    fields = "__all__"
    success_url = reverse_lazy("mainapp:news")
    permission_required = ("mainapp.add_news",)


class NewsDetailView(DetailView):
    model = mainapp_models.News


class NewsUpdateView(PermissionRequiredMixin, UpdateView):
    model = mainapp_models.News
    fields = "__all__"
    success_url = reverse_lazy("mainapp:news")
    permission_required = ("mainapp.change_news",)


class NewsDeleteView(PermissionRequiredMixin, DeleteView):
    model = mainapp_models.News
    success_url = reverse_lazy("mainapp:news")
    permission_required = ("mainapp.delete_news",)
