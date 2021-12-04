from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.fields.related import ForeignKey, OneToOneField

User = get_user_model()


class Book(models.Model):
    
    # * тут важно указать класс, а сорс укажется во вьюшке и сериалайзере | названия с сериалаййзером должны совпадать
    author = models.ForeignKey(User,on_delete=models.CASCADE,related_name='books')
    title = models.CharField(max_length=24)
    description = models.TextField()
    
    # * тут он работает правильно, главное указать его в сериалайзере, иначе его просто пропустит
    @property
    def avg_raiting(self,*args,**kwargs):
    # * prefetch_related делает 1 запрос в базу и хранит все значения в оперативке, потому некст циклы не будут так тормозить
        comments_ = self.comments.prefetch_related()
        # * эта проверка на наличие для того, чтобы не выпало ошибки деления на ноль
        if len(comments_)>0:
            returned_raiting = 0
            # * тут я делаю цикл чтобы вытащить параметры рейтинга у всех комментариев, без него никак
            for comment in comments_:
                returned_raiting += comment.raiting 
            return returned_raiting/len(self.comments.all())
        else:
            return 0
    
    def __str__(self):
        return f"{self.author} - {self.title}"
    
    
class Comment(models.Model):
    
    # * когда foreignkey видимо по умолчанию ищет по pk(id) 
    book = models.ForeignKey(Book,on_delete=models.CASCADE,related_name='comments')
    descriptions = models.TextField()    
    
    # ? почему бы просто не сделать кортеж, для чего делать класс и константы?
    # * это для того, чтобы не пришлось создавать новую модельку отдельно под рейтинг
    class RaitingStatus(models.IntegerChoices):
        ONE_STAR = 1
        TWO_STARS = 2
        THREE_STARS = 3
        FOUR_STARS = 4
        FIVE_STARS = 5
    raiting = models.IntegerField(choices=RaitingStatus.choices,default=RaitingStatus.ONE_STAR)


# TODO и на основе новых знаний делать свои дела

