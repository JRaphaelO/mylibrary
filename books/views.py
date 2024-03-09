import requests
from rest_framework import status, views
from rest_framework.response import Response

from books.models import Book
from books.serializers import BookSerializer

# Create your views here.
class BookListView(views.APIView):
    def get(self, request, *args, **kwargs):
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)
    
    def post(self, request, *args, **kwargs):
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            response = requests.get(f'https://www.googleapis.com/books/v1/volumes?q={serializer.data["title"]}')
            data = response.json()
            
            for item in data['items']:
                book = Book(
                    title=item['volumeInfo']['title'],
                    author=item['volumeInfo']['authors'][0],
                    year_published=item['volumeInfo']['publishedDate']
                )
                book.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)