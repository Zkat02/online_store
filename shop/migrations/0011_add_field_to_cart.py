from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0010_create_cartitem'),
    ]

    operations = [
        migrations.AddField(
            model_name="cart",
            name="customer",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="shop.customer"
            ),
        ),
    ]