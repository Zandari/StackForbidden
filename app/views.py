from django.shortcuts import render
from django.http import HttpRequest
from django.core.paginator import Paginator, Page
from typing import Optional, List, Any
from . import models


def _paginate(objects_list: List[Any], request: HttpRequest, per_page: int = 10) -> Page:
    paginator = Paginator(objects_list, per_page)
    page_number = request.GET.get('page')
    return paginator.get_page(page_number)


def _get_base_context() -> dict:
    popular_tags = models.Tag.objects.get_popular()[:10]
    best_members = models.Profile.objects.get_best()[:5]
    context = {
        "popular_tags": popular_tags,
        "best_members": best_members,
    }
    return context


def _question_feed(request: HttpRequest, data, heading: Optional[str] = None):
    context = _get_base_context()
    context["content_heading"] = heading

    paginator = Paginator(data, 10)
    paginator.ELLIPSIS = '.'
    page_number = request.GET.get('page')
    context["page_obj"] = paginator.get_page(page_number)
    context["paginator"] = paginator    # used for navigation

    return render(request, "feed.html", context)


def questions_feed_new(request: HttpRequest):
    return _question_feed(request, models.Question.objects.get_new())


def questions_feed_hot(request: HttpRequest):
    return _question_feed(request, models.Question.objects.get_hot(), "Hot Questions")


def questions_feed_by_tag(request: HttpRequest, tag: str):
    return _question_feed(request, models.Tag.objects.get(name=tag).questions.all())


def registration(request: HttpRequest):
    context = _get_base_context()
    return render(request, "signup.html", context)


def authorization(request: HttpRequest):
    context = _get_base_context()
    return render(request, "login.html", context)


def new_question(request: HttpRequest):
    context = _get_base_context()
    return render(request, "ask.html", context)


def answers(request: HttpRequest, id: int):
    context = _get_base_context()
    question = models.Question.objects.get(id=id)
    context["question"] = question

    paginator = Paginator(question.answers.all(), 5)
    paginator.ELLIPSIS = '.'
    page_number = request.GET.get('page')
    context["page_obj"] = paginator.get_page(page_number)
    context["paginator"] = paginator    # used for navigation

    return render(request, "question.html", context)
