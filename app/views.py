from django.shortcuts import render
from django.http import HttpRequest
from django.core.paginator import Paginator, Page, InvalidPage
from typing import Optional, List, Any, Tuple
from dataclasses import dataclass
from enum import Enum
from . import models


class AlertRole(Enum):
    DANGER = "danger"
    WARNING = "warning"
    INFO = "info"


@dataclass
class Alert:
    text: str
    role: AlertRole


def _paginate(objects_list: List[Any], request: HttpRequest, per_page: int = 10) -> Tuple[Page, Paginator]:
    paginator = Paginator(objects_list, per_page)
    paginator.ELLIPSIS = '.'
    page_number = request.GET.get('page')
    try:
        page = paginator.get_page(page_number)
    except InvalidPage:
        page = paginator.get_page(1)
    return page, paginator


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

    page_info = _paginate(data, request)
    context["page_obj"] = page_info[0]
    context["paginator"] = page_info[1]

    return render(request, "feed.html", context)


def questions_feed_new(request: HttpRequest):
    return _question_feed(request, models.Question.objects.get_new())


def questions_feed_hot(request: HttpRequest):
    return _question_feed(request, models.Question.objects.get_hot(), "Hot Questions")


def questions_feed_by_tag(request: HttpRequest, tag: str):
    return _question_feed(request, models.Tag.objects.get(name=tag).questions.all())


def registration(request: HttpRequest):
    context = _get_base_context()
    alert = Alert(role=AlertRole.DANGER, text="Lorem Ipsum =-)")
    context["alert"] = alert
    return render(request, "signup.html", context)


def authorization(request: HttpRequest):
    context = _get_base_context()
    return render(request, "login.html", context)


def new_question(request: HttpRequest):
    context = _get_base_context()
    return render(request, "ask.html", context)


def profile_settings(request: HttpRequest):
    context = _get_base_context()
    return render(request, "settings.html", context)


def answers(request: HttpRequest, id: int):
    context = _get_base_context()
    question = models.Question.objects.get(id=id)
    context["question"] = question

    page_info = _paginate(question.answers.all(), request)
    context["page_obj"] = page_info[0]
    context["paginator"] = page_info[1]

    return render(request, "question.html", context)
