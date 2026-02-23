from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("VP", "0005_member_fathers_name"),
    ]

    operations = [
        migrations.CreateModel(
            name="EventPhoto",
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
                    "image",
                    models.ImageField(
                        blank=True, null=True, upload_to="events/photos/"
                    ),
                ),
                ("caption", models.CharField(blank=True, max_length=200)),
                ("uploaded_at", models.DateTimeField(auto_now_add=True)),
                (
                    "event",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="photos",
                        to="VP.event",
                    ),
                ),
            ],
            options={
                "ordering": ["-uploaded_at"],
            },
        ),
    ]
