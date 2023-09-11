from celery import shared_task
from django.contrib.auth.models import User
from shop.models import Seller, Product, SellerReport


@shared_task(bind=True)
def generate_seller_report(self, seller_id, user_id, title=""):
    try:
        seller = Seller.objects.get(id=seller_id)
        user = User.objects.get(id=user_id)
        products = Product.objects.filter(seller=seller)
        task_id = self.request.id

        report = f"Report to {seller.seller_name}\n"
        report += f"Address: {seller.address}\n"
        report += "Products:\n"
        for product in products:
            report += f" - Product name: {product.name}, Description: {product.description}, Price: {product.price}\n"

        SellerReport.objects.create(
            task_id=task_id,
            user=user,
            seller=seller,
            title=title if title != "" else f"report#{task_id}",
            result=report,
        )
        return report

    except Seller.DoesNotExist:
        return "Seller not found"
