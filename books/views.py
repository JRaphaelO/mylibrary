import requests
from rest_framework import status, views
from rest_framework.response import Response

from books.models import Book, BookData
from books.serializers import BookSerializer, BooksDataSerializer

# Create your views here.
class BookListView(views.APIView):
    def get(self, request, *args, **kwargs):
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)

        booksData = BookData.objects.filter(book__in=books)

        data = []
        for book in serializer.data:
            bookData = booksData.filter(book=book['id']).all()
            data.append({
                **book,
                'bookData': BooksDataSerializer(bookData).data
            })

        return Response(data)
    
    def post(self, request, *args, **kwargs):
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            response = requests.get(f'https://www.googleapis.com/books/v1/volumes?q={serializer.data["title"]}')
            data = response.json()
            
            for item in data['items']:
                bookData = BookData(
                    book=serializer.instance,
                    title=item['volumeInfo']['title'],
                    author=item['volumeInfo']['authors'][0],
                    publisher=item['volumeInfo']['publisher'],
                    description=item['volumeInfo']['description'],
                    info_link=item['volumeInfo']['infoLink'],
                    image_link=item['volumeInfo']['imageLinks']['thumbnail']
                )

                bookData.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)