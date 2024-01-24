# Generated by Django 4.2.7 on 2023-11-15 17:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_answer_created_at_question_created_at_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='AnswerVote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_positive', models.BooleanField(help_text='Describes is record upvote or downvote')),
                ('created_at', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='QuestionVote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_positive', models.BooleanField(help_text='Describes is record upvote or downvote')),
                ('created_at', models.DateTimeField()),
            ],
        ),
        migrations.AddField(
            model_name='answer',
            name='is_correct',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='answer',
            name='owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='answers', to='app.profile'),
        ),
        migrations.AlterField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='app.question'),
        ),
        migrations.AlterField(
            model_name='question',
            name='owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='questions', to='app.profile'),
        ),
        migrations.DeleteModel(
            name='Vote',
        ),
        migrations.AddField(
            model_name='questionvote',
            name='answer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='question_votes', to='app.answer'),
        ),
        migrations.AddField(
            model_name='questionvote',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='question_votes', to='app.profile'),
        ),
        migrations.AddField(
            model_name='answervote',
            name='answer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='answer_votes', to='app.answer'),
        ),
        migrations.AddField(
            model_name='answervote',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answer_votes', to='app.profile'),
        ),
    ]
