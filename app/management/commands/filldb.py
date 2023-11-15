from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from app import models
import faker
import random


class Command(BaseCommand):
    help = "Closes the specified poll for voting"

    def add_arguments(self, parser):
        parser.add_argument("ratio", type=int)

    def handle(self, *args, **options):
        ratio = options["ratio"]
        print("All records would be deleted if there is any. Continue? [Y/N]: ")
        if input().lower() not in ("y", "yes"):
            return

        models.Profile.objects.all().delete()
        models.Tag.objects.all().delete()
        models.Question.objects.all().delete()
        models.Answer.objects.all().delete()
        models.Vote.objects.all().delete()

        fake = faker.Faker()
        profiles = list()

        for _ in range(ratio):
            u = models.User(username=fake.unique.user_name())
            u.save()
            p = models.Profile(user=u)
            p.save()
            profiles.append(p)

        # TAGS = ["python", "django", "orm", "backend", "frontend",
        #         "random", "vk", "helpme", "ruby", "c++"]
        TAGS = [fake.word() for _ in range(ratio)]

        tags = list()
        for tag in TAGS:
            t = models.Tag(name=tag)
            t.save()
            tags.append(t)

        for _ in range(ratio * 10):
            q = models.Question(owner=random.choice(profiles),
                                title=fake.sentence(nb_words=15),
                                text=fake.paragraph(nb_sentences=10),
                                created_at=fake.date_time_between(tzinfo=timezone.utc))
            random.shuffle(tags)
            q.save()
            for tag in tags[:random.randint(1, 5)]:
                q.tags.add(tag)
            for _ in range(10):
                a = models.Answer(owner=random.choice(profiles),
                                  question=q,
                                  text=fake.paragraph(nb_sentences=3),
                                  created_at=fake.date_time_between(start_date=q.created_at, tzinfo=timezone.utc))
                a.save()
                for _ in range(10):
                    v = models.Vote(answer=a,
                                    owner=random.choice(profiles),
                                    is_positive=random.choice((True, False)),
                                    created_at=fake.date_time_between(start_date=a.created_at, tzinfo=timezone.utc))
                    v.save()
            for _ in range(10):
                v = models.Vote(question=q,
                                owner=random.choice(profiles),
                                is_positive=random.choice((True, False)),
                                created_at=fake.date_time_between(start_date=q.created_at, tzinfo=timezone.utc))
                v.save()
