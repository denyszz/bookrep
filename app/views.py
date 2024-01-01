from django.shortcuts import render

from django.http import HttpResponse
from django.shortcuts import redirect
from .models import Book, Author
from django.db.models import Q

# Create your views here.

def home(request): 
    # Retrieve the 'q' parameter from the request
    query = request.GET.get('q')
    if query:
        # Filter books based on title or author name and in_stock status
        books = Book.objects.filter(Q(title__icontains=query) | Q(author_id__name__icontains=query), in_stock=True).order_by('-publish_date')
    else:
        # If no query, fetch all books that are in stock and order by publish date
        books = Book.objects.filter(in_stock=True).order_by('-publish_date')
    return render(request, 'book_list.html', {'books': books})

def edit_book(request, book_id=None):
    # When 'update' button is clicked
    if book_id:
        book = Book.objects.get(pk=book_id) 
         # Get fields from HTML form
        if request.method == "POST":
            title = request.POST['title']
            author_name = request.POST['author']
            publish_date = request.POST['publish_date']
            stock = True if request.POST.get('stock') == "yes" else False
            # Check if an author with the given name exists
            existing_author = Author.objects.filter(name=author_name).first()
            if existing_author:
                # Use the existing author's ID
                book.author_id = existing_author
            else:
                # Create a new author if none exists with the given name
                new_author = Author.objects.create(name=author_name)
                book.author_id = new_author
            # Save book
            book.title = title
            book.publish_date = publish_date
            book.in_stock = stock
            book.save()
            # For simplicity, no validation is performed; it is assumed that all fields are inserted correctly
            return redirect('edit')

        return render(request, 'extend_edit.html', {'book': book})
    
    books = Book.objects.order_by('-publish_date')
    return render(request, 'book_edit.html', {'books': books})

def delete_book(request):
    book_id = request.GET.get('bookid')
    author_id = request.GET.get('authorid')
    # Delete a book
    if book_id:
        book = Book.objects.get(id=book_id)
        book.delete()
    # Delete an author (this will also delete all the associated books)
    elif author_id:
        author = Author.objects.get(id=author_id)
        author.delete()
    return redirect('edit')

def add_book(request):
    post_success = None # Control variable passed as an argument to the html file
    # Get fields from HTML form
    if request.method  == "POST":
            title = request.POST['title']
            author_name = request.POST['author']
            publish_date = request.POST['publish_date']
            stock = True if request.POST.get('stock') == "yes" else False
            # Check if all fields were inserted
            if not title or not author_name or not publish_date:
                post_success = False
                return render(request, "book_add.html", {'post_success': post_success})
            # Check if author already exists in database (a single author mantains the same _id across various books)
            author, created = Author.objects.get_or_create(name=author_name)
            # Check if a book with the same author already exists
            if not created:
                existing_book = Book.objects.filter(author_id=author, title=title).exists()
                if existing_book:
                    post_success = False
                    return render(request, "book_add.html", {'post_success': post_success})
            # Save new Book
            book = Book()
            book.title = title
            book.publish_date = publish_date
            book.in_stock = stock
            book.author_id = author
            book.save()
            post_success = True
            return render(request, "book_add.html", {'post_success': post_success})
            
    return render(request, "book_add.html", {'post_success': post_success})



