from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.core.paginator import Paginator
from typing import Optional
from . import gencontent

_BASE_CONTEXT = {
    "user": {
        "is_authorized": False,
        "avatar": "",
    },
    "popular_tags": gencontent.get_random_tags(),
    "best_members": [gencontent.BestUser.generate() for _ in range(7)],
}

_QUESTIONS_FEED_CONTEXT = {
    **_BASE_CONTEXT,
    "paginator":    Paginator([gencontent.Question.generate() for _ in range(100)], 5),
}
_QUESTIONS_FEED_CONTEXT["paginator"].ELLIPSIS = "."

_ANSWERS_CONTEXT = {
    **_BASE_CONTEXT,
    "question": gencontent.Question.generate(),
    "paginator": Paginator([gencontent.Answer.generate() for _ in range(100)], 5),
}


def _questions_feed(request: HttpRequest, heading: Optional[str] = None):
    page_number = request.GET.get('page')

    context = _QUESTIONS_FEED_CONTEXT
    context["page_obj"] = context["paginator"].get_page(page_number)
    context["content_heading"] = heading
    return render(request, "feed.html", context)


def questions_feed_new(request: HttpRequest):
    return _questions_feed(request)


def questions_feed_hot(request: HttpRequest):
    return _questions_feed(request, "Hot Questions")


def questions_feed_by_tag(requests: HttpRequest, tag: str):
    return _questions_feed(requests, f"Questions related to {tag}")


def answers(request: HttpRequest, id: int):
    page_number = request.GET.get('page')

    context = _ANSWERS_CONTEXT
    context["page_obj"] = context["paginator"].get_page(page_number)
    return render(request, "question.html", context)


def new_question(request: HttpRequest):
    return render(request, "ask.html", _BASE_CONTEXT)


def authorization(request: HttpRequest):
    return render(request, "login.html", _BASE_CONTEXT)


def registration(request: HttpRequest):
    return render(request, "signup.html", _BASE_CONTEXT)
