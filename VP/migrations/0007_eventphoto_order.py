from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("VP", "0006_eventphoto"),
    ]

    operations = [
        migrations.AddField(
            model_name="eventphoto",
            name="order",
            field=models.IntegerField(default=0),
        ),
        migrations.AlterModelOptions(
            name="eventphoto",
            options={"ordering": ["order", "uploaded_at"]},
        ),
    ]
