# Data migration: set schedule_template from (user, name)

from django.db import migrations


def populate_schedule_template(apps, schema_editor):
    Schedule = apps.get_model("schedules", "Schedule")
    ScheduleTemplate = apps.get_model("schedules", "ScheduleTemplate")
    for schedule in Schedule.objects.all():
        template, _ = ScheduleTemplate.objects.get_or_create(
            user_id=schedule.user_id,
            name=schedule.name,
        )
        schedule.schedule_template_id = template.id
        schedule.save(update_fields=["schedule_template_id"])


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [
        ("schedules", "0003_scheduletemplate_and_schedule_schedule_template"),
    ]

    operations = [
        migrations.RunPython(populate_schedule_template, noop),
    ]
