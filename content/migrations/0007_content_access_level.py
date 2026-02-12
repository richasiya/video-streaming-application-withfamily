from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0006_alter_content_content_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='content',
            name='access_level',
            field=models.CharField(choices=[('free', 'Free'), ('basic', 'Basic'), ('premium', 'Premium')], default='free', max_length=20),
        ),
    ]
