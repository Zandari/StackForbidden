from typing import List, Union, Tuple
from dataclasses import dataclass, asdict
import random

_USERNAMES = ["zandari", "aress"]
_TITLE = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt"
_TEXT = "Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo. Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut..."
_TAGS = ["python", "django", "random", "backend", "frontend"]


def get_random_tags() -> List[str]:
    tags = [tag for tag in _TAGS if random.choice((True, False))]
    random.shuffle(tags)
    return tags


@dataclass
class User:
    username: str
    avatar: str

    todict = asdict

    @classmethod
    def generate(cls, usernames: List[str] = _USERNAMES,
                 avatar: Union[List[str] | str] = "placeholder.png"):
        if isinstance(avatar, list):
            avatar = random.choice(avatar)
        return cls(
            username=random.choice(usernames),
            avatar=avatar,
        )


@dataclass
class BestUser(User):
    answers: int

    @classmethod
    def generate(cls, answers_range: Tuple[int, int] = (0, 100), **kwargs):
        return cls(
            **User.generate(**kwargs).todict(),
            answers=random.randint(*answers_range),
        )


@dataclass
class Question:
    id: int
    owner: User
    title: str
    text: str
    votes: int
    answers: int
    posted_at: str
    tags: List[str]

    todict = asdict

    @classmethod
    def generate(cls):
        return cls(
            id=random.randint(100, 1000),
            owner=User.generate(),
            title=_TITLE,
            text=_TEXT,
            votes=random.randint(0, 100),
            answers=random.randint(0, 100),
            tags=get_random_tags(),
            posted_at="6 hr. ago",
        )


@dataclass
class Answer:
    owner: User
    text: str
    votes: int
    posted_at: str

    @classmethod
    def generate(cls):
        return cls(
            owner=User.generate(),
            text=_TEXT,
            votes=random.randint(0, 100),
            posted_at="6 hr. ago",
        )
