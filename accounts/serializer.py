from rest_framework import serializers
from django.core.validators import MinLengthValidator, MaxLengthValidator


# TODO добавить нормальные формочки, не только для зщстмана, но и для людей
class RegistrationSerializer(serializers.Serializer):
    #  тут не нужны валидаторы только по одной причине: инфа передается в json ащрмате, тут нет никаких форм 
    # чтобы предварительно проверять    validators=[MinLengthValidator(5),MaxLengthValidator(14)]
    username= serializers.CharField(max_length=20)
    password= serializers.CharField(max_length=20)
    
