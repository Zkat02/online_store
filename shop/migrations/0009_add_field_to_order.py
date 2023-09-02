from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('shop', '0008_create_orderitem'),
    ]

    operations = [

        migrations.AddField(
            model_name="order",
            name="products",
            field=models.ManyToManyField(through="shop.OrderItem", to="shop.product"),
        ),
    ]
