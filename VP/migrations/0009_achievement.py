from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("VP", "0008_eventresult"),
    ]

    operations = [
        migrations.CreateModel(
            name="Achievement",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=200)),
                ("contest_name", models.CharField(blank=True, max_length=200)),
                ("category", models.CharField(choices=[("club", "Club Performance"), ("contest", "Outside Contest"), ("research", "Research/Publication"), ("innovation", "Innovation"), ("other", "Other")], max_length=20)),
                ("position", models.CharField(blank=True, max_length=100)),
                ("team_name", models.CharField(blank=True, max_length=200)),
                ("participants", models.TextField(blank=True, help_text="Enter one participant per line")),
                ("description", models.TextField()),
                ("date", models.DateField(blank=True, null=True)),
                ("location", models.CharField(blank=True, max_length=200)),
                ("image", models.ImageField(blank=True, null=True, upload_to="achievements/")),
                ("order", models.IntegerField(default=0)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={
                "ordering": ["order", "-date", "-created_at"],
            },
        ),
    ]
