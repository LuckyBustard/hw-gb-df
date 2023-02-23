import logging

from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, TemplateView, UpdateView, View
from django.views.generic import CreateView, DeleteView, DetailView, TemplateView, UpdateView, ListView
from mainapp import forms as mainapp_forms
from mainapp import models as mainapp_models
from django.http import JsonResponse, FileResponse
from django.template.loader import render_to_string
from django.http import Http404
from django.conf import settings
from django.core.cache import cache
from django.contrib import messages
from mainapp import tasks as mainapp_tasks
from django.http.response import HttpResponseRedirect
from django.utils.translation import gettext_lazy as _


logger = logging.getLogger(__name__)


class MainPageView(TemplateView):
    template_name = "mainapp/index.html"


class NewsPageView(ListView):
    model = mainapp_models.News
    paginate_by = 5

    def get_queryset(self):
        return super().get_queryset().filter(deleted=False)


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
        logger.info(f"Open {self.__class__.__name__}")
        start = (page - 1) * 6
        stop = start + 6
        context["page_num"] = page
        context["courses"] = mainapp_models.Courses.objects.all()[start:stop]
        return context


class CoursesDetailView(TemplateView):
    template_name = "mainapp/courses_detail.html"

    def get_context_data(self, pk=None, **kwargs):
        logger.debug("Yet another log message")
        context = super(CoursesDetailView, self).get_context_data(**kwargs)
        context["course_object"] = get_object_or_404(mainapp_models.Courses, pk=pk)
        context["lessons"] = mainapp_models.Lesson.objects.filter(course=context["course_object"])
        context["teachers"] = mainapp_models.CourseTeachers.objects.filter(course=context["course_object"])
        if not self.request.user.is_anonymous:
            if not mainapp_models.CourseFeedback.objects.filter(
                course=context["course_object"], user=self.request.user
            ).count():
                context["feedback_form"] = mainapp_forms.CourseFeedbackForm(
                    course=context["course_object"], user=self.request.user
                )

        cached_feedback = cache.get(f"feedback_list_{pk}")
        if not cached_feedback:
            context["feedback_list"] = (
                mainapp_models.CourseFeedback.objects.filter(course=context["course_object"])
                .order_by("-created", "-rating")[:5]
                .select_related()
            )
            cache.set(f"feedback_list_{pk}", context["feedback_list"], timeout=300)  # 5 minutes

            # Archive object for tests --->
            import pickle

            with open(f"mainapp/fixtures/005_feedback_list_{pk}.bin", "wb") as outf:
                pickle.dump(context["feedback_list"], outf)
            # <--- Archive object for tests

        else:
            context["feedback_list"] = cached_feedback

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

    def get_context_data(self, **kwargs):
        context = super(ContactsPageView, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context["form"] = mainapp_forms.MailFeedbackForm(user=self.request.user)
        return context

    def post(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            cache_lock_flag = cache.get(f"mail_feedback_lock_{self.request.user.pk}")
            if not cache_lock_flag:
                cache.set(
                    f"mail_feedback_lock_{self.request.user.pk}",
                    "lock",
                    timeout=300,
                )
                messages.add_message(self.request, messages.INFO, _("Message sended"))
                mainapp_tasks.send_feedback_mail.delay(
                    {
                        "user_id": self.request.POST.get("user_id"),
                        "message": self.request.POST.get("message"),
                    }
                )
            else:
                messages.add_message(
                    self.request,
                    messages.WARNING,
                    _("You can send only one message per 5 minutes"),
                )
        return HttpResponseRedirect(reverse_lazy("mainapp:contacts"))


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


class LogView(TemplateView):
    template_name = "mainapp/log_view.html"

    def get_context_data(self, **kwargs):
        context = super(LogView, self).get_context_data(**kwargs)
        log_slice = []
        with open(settings.LOG_FILE, "r") as log_file:
            for i, line in enumerate(log_file):
                if i == 1000:  # first 1000 lines
                    break
                log_slice.insert(0, line)  # append at start
            context["log"] = "".join(log_slice)
        return context


class LogDownloadView(UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_superuser

    def get(self, *args, **kwargs):
        return FileResponse(open(settings.LOG_FILE, "rb"))
