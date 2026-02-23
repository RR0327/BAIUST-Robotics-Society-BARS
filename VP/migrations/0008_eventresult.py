from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("VP", "0007_eventphoto_order"),
    ]

    operations = [
        migrations.CreateModel(
            name="EventResult",
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
                (
                    "rank",
                    models.CharField(
                        choices=[
                            ("Champion", "Champion"),
                            ("1st Runner-up", "1st Runner-up"),
                            ("2nd Runner-up", "2nd Runner-up"),
                            ("3rd Place", "3rd Place"),
                            ("4th Place", "4th Place"),
                            ("5th Place", "5th Place"),
                            ("6th Place", "6th Place"),
                            ("7th Place", "7th Place"),
                            ("8th Place", "8th Place"),
                            ("9th Place", "9th Place"),
                            ("10th Place", "10th Place"),
                        ],
                        max_length=50,
                    ),
                ),
                ("participant_name", models.CharField(max_length=200)),
                ("team_name", models.CharField(blank=True, max_length=200)),
                ("order", models.IntegerField(default=0)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "event",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="results",
                        to="VP.event",
                    ),
                ),
            ],
            options={
                "ordering": ["order"],
                "unique_together": {("event", "rank")},
            },
        ),
    ]
