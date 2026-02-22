# Generated manually for two-level schedules

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("schedules", "0002_schedule_unique_schedule_name"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="ScheduleTemplate",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="schedule_templates",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.RemoveConstraint(
            model_name="schedule",
            name="unique_schedule_name",
        ),
        migrations.AddField(
            model_name="schedule",
            name="schedule_template",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="slots",
                to="schedules.scheduletemplate",
            ),
        ),
        migrations.AddConstraint(
            model_name="scheduletemplate",
            constraint=models.UniqueConstraint(
                fields=("user", "name"), name="unique_user_schedule_name"
            ),
        ),
    ]
