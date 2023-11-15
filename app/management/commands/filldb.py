from django.core.management.base import BaseCommand, CommandError
from app import models
import faker
import random


class Command(BaseCommand):
    help = "Closes the specified poll for voting"

    def add_arguments(self, parser):
        pass
        # parser.add_argument("poll_ids", nargs="+", type=int)

    def handle(self, *args, **options):
        print("All records would be deleted. Continue? [Y/N]: ")
        if input().lower() not in ("y", "yes"):
            return

        models.Profile.objects.all().delete()
        models.Tag.objects.all().delete()
        models.Question.objects.all().delete()
        models.Answer.objects.all().delete()
        models.Vote.objects.all().delete()

        fake = faker.Faker()
        profiles = list()

        for i in range(10):
            u = models.User(username=fake.unique.user_name())
            u.save()
            p = models.Profile(user=u)
            p.save()
            profiles.append(p)

        TAGS = ["python", "django", "orm", "backend", "frontend",
                "random", "vk", "helpme", "ruby", "c++"]

        tags = list()
        for tag in TAGS:
            t = models.Tag(name=tag)
            t.save()
            tags.append(t)

        questions = list()
        answers = list()

        for _ in range(20):
            q = models.Question(owner=random.choice(profiles),
                                title=fake.sentence(nb_words=15),
                                text=fake.paragraph(nb_sentences=10))
            random.shuffle(tags)
            q.save()
            for tag in tags[:random.randint(1, len(tags))]:
                q.tags.add(tag)
            questions.append(q)
            for i in range(random.randint(1, 20)):
                a = models.Answer(owner=random.choice(profiles),
                                  question=q,
                                  text=fake.paragraph(nb_sentences=3))
                a.save()
                answers.append(a)
                for _ in range(random.randint(1, 100)):
                    v = models.Vote(answer=a,
                                    owner=random.choice(profiles),
                                    is_positive=random.choice((True, False)))
                    v.save()
            for _ in range(random.randint(1, 100)):
                v = models.Vote(question=q,
                                owner=random.choice(profiles),
                                is_positive=random.choice((True, False)))
                v.save()