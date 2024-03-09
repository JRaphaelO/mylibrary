from django import views
from rest_framework.response import Response

from books.models import Book
from books.serializers import BookSerializer

# Create your views here.
class BookListView(views.APIView):
    def get(self, request, *args, **kwargs):
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)