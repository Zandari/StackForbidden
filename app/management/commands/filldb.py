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
        models.AnswerVote.objects.all().delete()
        models.QuestionVote.objects.all().delete()

        fake = faker.Faker()

        users = models.User.objects.bulk_create(
            [models.User(username=fake.unique.user_name()) for _ in range(ratio)]
        )

        profiles = models.Profile.objects.bulk_create(
            [models.Profile(user=u) for u in users]
        )

        tags = models.Tag.objects.bulk_create(
            [models.Tag(name=t) for t in [fake.unique.word() for _ in range(ratio)]]
        )

        questions = models.Question.objects.bulk_create(
            [models.Question(owner=random.choice(profiles),
                             title=fake.sentence(nb_words=15),
                             text=fake.paragraph(nb_sentences=10),
                             created_at=fake.date_time_between(tzinfo=timezone.utc))
             for _ in range(ratio * 10)]
        )
        random.shuffle(tags)
        for question in questions:
            [question.tags.add(tag) for tag in tags[:random.randint(1, 5)]]

        for q in questions:
            models.QuestionVote.objects.bulk_create(
                [models.QuestionVote(question=q,
                                     owner=random.choice(profiles),
                                     is_positive=random.choice((True, False)),
                                     created_at=fake.date_time_between(start_date=q.created_at, tzinfo=timezone.utc))
                 for _ in range(10)]
            )

        for q in questions:
            answers = models.Answer.objects.bulk_create(
                [models.Answer(owner=random.choice(profiles),
                               question=q,
                               is_correct=random.choice((True, False)),
                               text=fake.paragraph(nb_sentences=10),
                               created_at=fake.date_time_between(start_date=q.created_at, tzinfo=timezone.utc))
                 for _ in range(10)]
            )
            for a in answers:
                models.AnswerVote.objects.bulk_create(
                    [models.AnswerVote(answer=a,
                                       owner=random.choice(profiles),
                                       is_positive=random.choice((True, False)),
                                       created_at=fake.date_time_between(start_date=a.created_at, tzinfo=timezone.utc))
                    for _ in range(10)]
                )
                models.AnswerVote.objects.bulk_create(
                    [models.AnswerVote(answer=a,
                                         owner=random.choice(profiles),
                                         is_positive=random.choice((True, False)),
                                         created_at=fake.date_time_between(start_date=a.created_at, tzinfo=timezone.utc))
                     for _ in range(10)]
                )
