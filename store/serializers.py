from rest_framework import serializers  # type: ignore
from .models import Customer, Product, Category, Comment, Cart, CartItem
from decimal import Decimal
from django.utils.text import slugify


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
    
     
    def create(self, validated_data):
        product = Product(**validated_data)
        product.slug = slugify(product.name)
        product.save()
        return product
    

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['name', 'body', 'status', ]

    def create(self, validated_data):
        product_id = self.context['product_pk']
        return Comment.objects.create(product_id=product_id, **validated_data)


class CartProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'unit_price' ]


class UpdateCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['quantity']


class AddCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity']

    def create(self, validated_data):
        cart_id = self.context['cart_pk']

        product = validated_data.get('product')
        quantity = validated_data.get('quantity')

        try:
            cart_item = CartItem.objects.get(cart_id=cart_id, product_id=product.id)
            cart_item.quantity += quantity
            cart_item.save()
        except CartItem.DoesNotExist:
            cart_item = CartItem.objects.create(cart_id=cart_id, **validated_data)

        self.instance = cart_item
        return cart_item


class CartItemSerializer(serializers.ModelSerializer):
    product = CartProductSerializer()
    item_total = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity', 'item_total']

    def get_item_total(self, cart_item):
        return cart_item.quantity * cart_item.product.unit_price


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['id', 'items', 'total_price']
        read_only_fields = ['id', ]

    def get_total_price(self, cart):
        return sum([item.quantity * item.product.unit_price for item in cart.items.all()])
    
class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'user', 'birth_date']
        read_only_fields = ['user', ]

       