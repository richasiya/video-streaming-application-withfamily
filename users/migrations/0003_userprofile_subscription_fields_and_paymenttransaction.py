from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_userprofile_dob_userprofile_mobile_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='last_order_id',
            field=models.CharField(blank=True, max_length=120),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='last_payment_id',
            field=models.CharField(blank=True, max_length=120),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='plan_confirmed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='subscription_status',
            field=models.CharField(choices=[('free', 'Free'), ('active', 'Active'), ('canceled', 'Canceled'), ('past_due', 'Past Due')], default='free', max_length=20),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='subscription_updated_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.CreateModel(
            name='PaymentTransaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('plan', models.CharField(choices=[('free', 'Free'), ('basic', 'Basic'), ('premium', 'Premium')], max_length=20)),
                ('amount', models.PositiveIntegerField()),
                ('currency', models.CharField(default='INR', max_length=10)),
                ('razorpay_order_id', models.CharField(blank=True, max_length=120)),
                ('razorpay_payment_id', models.CharField(blank=True, max_length=120)),
                ('razorpay_signature', models.CharField(blank=True, max_length=200)),
                ('status', models.CharField(choices=[('created', 'Created'), ('paid', 'Paid'), ('failed', 'Failed')], default='created', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth.user')),
            ],
        ),
    ]
