from enum import auto
from django.db import models
from django.contrib.auth.models import User

class FlipkartData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    image = models.SlugField(max_length=500, null=True, blank=True)
    title = models.CharField(max_length=500, null=True, blank=True)
    ratting=models.CharField(max_length = 10, null=True, blank=True)
    review_data = models.CharField(max_length=500, null=True, blank=True)
    price = models.CharField(max_length = 20, null=True, blank=True)
    discount = models.CharField(max_length=100, null=True, blank=True)
    original_price = models.CharField(max_length = 20, null=True, blank=True)
    product_description = models.CharField(max_length=600, null=True, blank=True)
    product_link = models.SlugField(max_length=500, null=True, blank=True)
    

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ["created_at"]


class AmezonData(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)
    image = models.SlugField(max_length=500, null=True, blank=True)
    ratting = models.CharField(max_length=50, null = True, blank = True)
    review_num = models.CharField(max_length=20, null=True, blank=True)
    price = models.CharField(max_length = 20, null=True, blank=True)
    product_description = models.CharField(
        max_length=600, null=True, blank=True)
    product_link = models.SlugField(max_length=500, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product_description[:20]

    class Meta:
        ordering = ["created_at"]

class Compare(models.Model):
    flipkart_product = models.ForeignKey(FlipkartData, on_delete=models.CASCADE, null=True, blank=True)
    amazon_product = models.ForeignKey(AmezonData, on_delete=models.CASCADE, null=True, blank=True)

    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.created

class PdfFiles(models.Model):
    pdf_file = models.FileField(upload_to='pdf_files')