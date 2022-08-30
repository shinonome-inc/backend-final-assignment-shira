from django.views.generic import CreateView, DetailView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404
from django.forms import Textarea

from .models import Tweet


class TweetCreateView(LoginRequiredMixin, CreateView):
    model = Tweet
    fields = ("content",)
    template_name = "tweets/create.html"
    success_url = reverse_lazy("accounts:home")

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["content"].widget = Textarea()

        return form

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class TweetDetailView(LoginRequiredMixin, DetailView):
    model = Tweet
    context_object_name = "tweet"
    template_name = "tweets/detail.html"


class TweetDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Tweet
    template_name = "tweets/delete.html"
    success_url = reverse_lazy("accounts:home")

    def test_func(self):
        tweet = get_object_or_404(Tweet, pk=self.kwargs["pk"])
        return self.request.user.pk == tweet.user.pk
