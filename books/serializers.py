from rest_framework import serializers
from .models import Book, BookData

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

class BooksDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookData
        fields = '__all__'