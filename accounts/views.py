from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated

from rest_framework.parsers import FormParser
from .serializer import RegistrationSerializer

User = get_user_model()

class RegistrationAPIView(APIView):
    
    def post(self,request):
        # * вытаскиваем данные из базы данных(request.data) и сериализуем в норм вид через RegistrationSerialzer 
        serializer = RegistrationSerializer(data=request.data)
        # * тут мы делаем is_valid() потому что без этого нельзя вытаскивать данные из validated_data 
        # * а raise_exception
        serializer.is_valid(raise_exception=True)

        # ? почему нельзя просто прописать validated_data['username']? потому что это может потенциально вызвать ошибку
        # * просто исопльзуйте во всех словарях .get() и избегите всех возможных ошибок
        username=serializer.validated_data.get('username')
        password=serializer.validated_data.get('password')
        
        if User.objects.filter(username=username).exists():
            return Response({'message':'username already exist! try again'},
                            status=status.HTTP_400_BAD_REQUEST)
            
        # * create_user хэширует данные пароля 
        user = User.objects.create_user(username=username,password=password)
        token = Token.objects.create(user=user)
        
        return Response({'token':token.key},status=status.HTTP_201_CREATED)

class LoginAPIView(APIView):
    
    def post(self,request):
        serializer = RegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data.get('username')
        password = serializer.validated_data.get('password')
        
        user = authenticate(username=username,password=password)
        # * если в базе данных он есть и пароль совпал, то
        if user is not None:
            # * мы получаем/создаем токен потому, что когда юзер logout то его токен удаляется
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token':token.key})  # * тут по дефолту стоит статуc 200_OK
        return Response({'message':'invalid credentials'},status = status.HTTP_400_BAD_REQUEST)
    
    
class LogoutAPIView(APIView):
    # * если ты хочешь использовать логаут, то должен быть в системе 
    permission_classes = [IsAuthenticated]
    def post(self,request):
        # * тут я вытаскиваю юзера через реквест, все верно
        user = request.user
        # * у пользователя когда он авторизировался был токен, который можно найти по user'у
        token = Token.objects.filter(user=user).first()
        # * тут я удаляю токен, поэтому несмотря на то, что токен в хэдере у пользователя еще хранится, он недействителен
        # * поэтому он должен снова авторизироваться
        token.delete()
        return Response({"seccess":True})





# ---------
# {
# "username":"admin1",
# "password":"admin"
# }