# Change Task.schedule FK from Schedule to ScheduleTemplate

import django.db.models.deletion
from django.db import migrations, models


def set_schedule_template_id(apps, schema_editor):
    Task = apps.get_model("tasks", "Task")
    Schedule = apps.get_model("schedules", "Schedule")
    for task in Task.objects.filter(schedule_id__isnull=False):
        try:
            slot = Schedule.objects.get(pk=task.schedule_id)
            if slot.schedule_template_id:
                task.schedule_new_id = slot.schedule_template_id
                task.save(update_fields=["schedule_new_id"])
        except Schedule.DoesNotExist:
            pass


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [
        ("schedules", "0004_populate_schedule_template"),
        ("tasks", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="task",
            name="schedule_new",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="+",
                to="schedules.scheduletemplate",
            ),
        ),
        migrations.RunPython(set_schedule_template_id, noop),
        migrations.RemoveField(
            model_name="task",
            name="schedule",
        ),
        migrations.RenameField(
            model_name="task",
            old_name="schedule_new",
            new_name="schedule",
        ),
        migrations.AlterField(
            model_name="task",
            name="schedule",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="tasks",
                to="schedules.scheduletemplate",
            ),
        ),
    ]
