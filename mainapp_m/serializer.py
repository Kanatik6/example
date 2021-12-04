from rest_framework import serializers
from .models import Book,Comment
from django.contrib.auth import get_user_model 

User = get_user_model()

class BookSerializer(serializers.ModelSerializer):
    # * perform_craete не может работать если его тут не выделить   
    author = serializers.ReadOnlyField(source='author.username')
    class Meta:
        model = Book
        # * exclude нельзя использовать, т.к. у нас есть property в модельке, которую тут нужно указать
        fields = ['id','title','description','author','avg_raiting']
    
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        exclude = []
        
    # def update(self,instance,validated_data):
    #     if instance.type == Order.OrderType.PERDING and validated_data['type'] == 'canceled':
    #         ordered_products = instance.products.all()
    #         for product in ordered_products:
    #             pass
            
    #     return super.update(instance,validated_data)

# ? то он не может найти это поле и выдаст ошибку     "author": ["This field is required."]
