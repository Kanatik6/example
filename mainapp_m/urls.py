from rest_framework.routers import SimpleRouter
from .views import BookViewSet, CommentViewSet

router = SimpleRouter()
router.register('books',BookViewSet)
router.register('comments',CommentViewSet)

urlpatterns = []

urlpatterns += router.urls
