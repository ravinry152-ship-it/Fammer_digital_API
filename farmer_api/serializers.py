# Serializer បំប្លែង JSON String ទៅជា Python Dictionary ព្រោះpython(Django)វាអត់ស្គល់jsonទេ
from rest_framework import serializers
from .models import SaleProduct, Learning ,RicePrice ,RiceVarieties

class SaleProductSerializer(serializers.ModelSerializer) :
    class Meta :
        model = SaleProduct
        fields = '__all__'

class LearningSerializer(serializers.ModelSerializer) :
    class Meta :
        model = Learning
        fields = ["id" , "title" ,"description" , "image"]

class RicePriceSerializer(serializers.ModelSerializer) :
    class Meta :
        model = RicePrice
        fields = '__all__'

class RiceVarietiesSerializer(serializers.ModelSerializer) :
    class Meta :
        model = RiceVarieties
        fields = '__all__'