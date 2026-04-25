from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("VP", "0022_generalmemberapplication"),
    ]

    operations = [
        migrations.AlterField(
            model_name="achievement",
            name="category",
            field=models.CharField(
                choices=[
                    ("club", "Club Performance"),
                    ("contest", "Outside Contest"),
                    ("research", "Research/Publication"),
                    ("innovation", "Innovation"),
                    ("autonomous_robot_challenge", "Autonomous Robot Challenge"),
                    ("line_following_robot_competition", "Line Following Robot Competition"),
                    ("maze_solving_robot", "Maze Solving Robot"),
                    ("robo_soccer", "Robo Soccer"),
                    ("robo_race", "Robo Race"),
                    ("combat_robotics_battle_bots", "Combat Robotics (Battle Bots)"),
                    ("drone_racing_uav_competition", "Drone Racing / UAV Competition"),
                    ("other", "Other"),
                ],
                max_length=50,
            ),
        ),
    ]
