from rest_framework import serializers  # type: ignore
from .models import Product, Category
from decimal import Decimal

class CategorySerializer(serializers.ModelSerializer):
    num_top_product = serializers.IntegerField(source = 'products.count', read_only = True)

    class Meta:
        model = Category
        fields = ['id', 'title', 'description', 'num_top_product' ,]

DOLLORS_TO_RIALS = 600000
class ProductSerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=255, source='name')
    price = serializers.DecimalField(max_digits=6, decimal_places=2, source='unit_price')
    category = serializers.StringRelatedField()
    unit_price_after_tax = serializers.SerializerMethodField()
    price_rials = serializers.SerializerMethodField()
    class Meta:
        model = Product
        fields = ['id', 'title', 'price', 'category', 'unit_price_after_tax', 'inventory', 'description', 'price_rials' ,]

    def get_unit_price_after_tax(self, product):
        return round(product.unit_price * Decimal(1.09), 2)    
    
    def get_price_rials(self,product):
        return int(product.unit_price * DOLLORS_TO_RIALS)
    
    