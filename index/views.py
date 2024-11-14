from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.views import View

from index.forms import ReviewForm
from index.models import TeamMember, Review


class HomePageView(View):
    """Обрабатывает запросы для главной страницы, которая отображает участников команды и отзывы."""

    template_home: str = 'index/index.html'

    def get(self, request: HttpRequest) -> HttpResponse:
        """Обрабатывает GET-запросы и отображает команду и отзывы."""
        team = TeamMember.objects.all()
        reviews = Review.objects.filter(is_published=True)

        context = {
            'team': team,
            'reviews': reviews,
        }
        return render(request, self.template_home, context=context)


class ReviewCreateView(View):
    """Обрабатывает создание отзыва."""

    template_name = 'index/review.html'
    form_class = ReviewForm
    success_url = 'home'

    def get(self, request: HttpRequest) -> HttpResponse:
        """Отображает форму для создания отзыва."""
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request: HttpRequest) -> HttpResponse:
        """Обрабатывает сохранение отзыва при отправке формы."""
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            return redirect(self.success_url)

        return render(request, self.template_name, {'form': form})

