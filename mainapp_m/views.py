from rest_framework.viewsets import ModelViewSet
from .models import Book,Comment
from .serializer import BookSerializer,CommentSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated

class BookViewSet(ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]
    
    # ? зачем делать serializer.save() с пустыми строками 
    # * его использовать только если поля нужно заполнить инфой извне обьекта
    def perform_create(self, serializer):
        serializer.save(author=self.request.user) # * 
# ------------------------------------------------------------    
# * Тут сначала идет в сериалайзер, видит что мы вмешались в него, перезодит в perform_craete(), 
# * выполняет строку 12 и под полем author записывает user'а, потом переходит в метод ModelSerailizer.save(),
# * author = serializers.ReadOnlyField(source='author.username')
# ------------------------------------------------------------
class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    
    