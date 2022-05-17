# Django for APIs (Book)

---

## Chapter 1: Web APIs

### World Wide Web

Hypertext Transfer Protocol (HTTP)13, was the first standard, universal way to
share documents over the internet. It ushered in the concept of web pages: discrete documents
with a URL, links, and resources such as images, audio, or video.


### URLs

A URL (Uniform Resource Locator) is the address of a resource on the internet. For example, the
Google homepage lives at https://www.google.com.


### Internet Protocol Suite

when a user types https://www.google.com into their web browser and
hits Enter. First the browser uses a domain name service (DNS) to translate the domain name “google.com” into an IP, which is a unique sequence of numbers representing every connected device on the
internet.

After the browser has the IP address for a given domain, it needs a way to set up a consistent
connection with the desired server. This happens via the Transmission Control Protocol (TCP)
which provides reliable, ordered, and error-checked delivery of bytes between two application.


### HTTP Verbs

1. `GET` is used to retrieve information from the given server using a given URI. Requests using GET should only retrieve data and should have no other effect on the data.

2. `HEAD` Same as GET, but transfers the status line and header section only.

3. `POST` is used to send data to the server, for example, customer information, file upload, etc. using HTML forms.

4. `PUT` Replaces all current representations of the target resource with the uploaded content.

5. `DELETE` Removes all current representations of the target resource given by a URI.

6. `CONNECT` Establishes a tunnel to the server identified by a given URI.

7. `OPTIONS` Describes the communication options for the target resource.

8. `TRACE` Performs a message loop-back test along the path to the target resource.

9. `PATCH` method is used to make a partial update to a resource.


### Endpoints

A website consists of web pages with HTML, CSS, images, JavaScript, and more. But a web API
has endpoints instead which are URLs with a list of available actions (HTTP verbs) that expose
data (typically in JSON)


### HTTP

HTTP is a request-response protocol between two computers that have an existing TCP connection.
The computer making the requests is known as the client while the computer responding
is known as the server.

Every HTTP message, whether a request or response, therefore has the following format:

#### Diagram

    -----------------------
    Response/request line
    Headers...

    (optional) Body
    -----------------------



### Status Codes

    - 1xx informational response – the request was received, continuing process
    - 2xx Success - the action requested by the client was received, understood, and accepted
    - 3xx Redirection - the requested URL has moved
    - 4xx Client Error - there was an error, typically a bad URL request by the client
    - 5xx Server Error - the server failed to resolve a request

most common ones such as 200 (OK), 201 (Created), 301 (Moved Permanently),
404 (Not Found), and 500 (Server Error).


### Statelessness

HTTP is a `stateless` protocol. This means each request/response pair is completely
independent of the previous one. There is no stored
memory of past interactions, which is known as state in computer science.


### REST

Every RESTful API must, at a minimum, have these three principles:

- is stateless, like HTTP
- supports common HTTP verbs (GET, POST, PUT, DELETE, etc.)
- returns data in either the JSON or XML format


## Chapter 2: Library Website and API

### DJANGO

A traditional Django website consists of a single project and one (or more) apps representing
discrete functionality.

    $ django-admin startproject project_name .

- `__init__.py` is a Python way to treat a directory as a package; it is empty
- `asgi.py` stands for Asynchronous Server Gateway Interface and is a new option in Django
3.0+
- `settings.py` contains all the configuration for our project
- `urls.py` controls the top-level URL routes
- `wsgi.py` stands for Web Server Gateway Interface and helps Django serve the eventual web
pages
- `manage.py` executes various Django commands such as running the local web server or
creating a new app.

    $ python manage.py runserver


### First App

The typical next step is to start adding apps, which represent discrete areas of functionality. A
single Django project can support multiple apps.

    $ python manage.py startapp app_name

- `admin.py` is a configuration file for the built-in Django Admin app
- `apps.py` is a configuration file for the app itself
- the `migrations/` directory stores migrations files for database changes
- `models.py` is where we define our database models
- `tests.py` is for our app-specific tests
- `views.py` is where we handle the request/response logic for our web app

Typically, developers will also create an `urls.py` file within each app, too, for routing.

The first step is to add the new app to our INSTALLED_APPS configuration.

```python
# config/settings.py
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Local
    'books', # new
]
```

Each web page in traditional Django requires several files: a view, url, and template. But first we
need a database model so let’s start there.


### Models

```python
# books/models.py
from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=250)
    subtitle = models.CharField(max_length=250)
    author = models.CharField(max_length=100)
    isbn = models.CharField(max_length=13)

def __str__(self):
    return self.title
```

This is a basic Django model where we import models from Django on the top line and then create
a Book class that extends it. There are four fields: title, subtitle, author, and isbn. We also include
a __str__ method so that the title of a book will display in the admin later on.

Since we created a new database model we need to create a migration file to go along with
it.

    $ python manage.py makemigrations books
        Migrations for 'books':
        books/migrations/0001_initial.py
            - Create model Book
    $ python manage.py migrate
        Operations to perform:
            Apply all migrations: admin, auth, books, contenttypes, sessions
        Running migrations:
            Applying books.0001_initial... OK


### Admin

We can start entering data into our new model via the built-in Django app. But we must do two
things first: 

- create a superuser account

    $ python manage.py createsuperuser

- update `admin.py` so the ***books*** app is displayed.

```python
# books/admin.py
from django.contrib import admin
from .models import Book

admin.site.register(Book)
```

    $ python manage.py runserver

Navigate to http://127.0.0.1:8000/admin, click on the “+ Add” link next to Book and add the data scpecified 

Our traditional Django project has data now but we need a way to expose it as a web page. That
means creating views, URLs, and template files. Let’s do that now.


### Views

The views.py file controls how the database model content is displayed. Since we want to list all
books we can use the built-in generic class [ListView](https://docs.djangoproject.com/en/3.1/ref/class-based-views/generic-display/#django.views.generic.list.ListView).

```python
# books/views.py
from django.views.generic import ListView
from .models import Book

class BookListView(ListView):
    model = Book
    template_name = 'book_list.html'
```

### Urls

We need to set up both the project-level `urls.py` file and then one within the books app. When
a user visits our site they will first interact with the config/urls.py file

```python
# config/urls.py
from django.contrib import admin
from django.urls import path, include # new

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('books.urls')), # new
]
```

Now we can create and configure our books/urls.py file.

```python
# books/urls.py
from django.urls import path
from .views import BookListView

urlpatterns = [
    path('', BookListView.as_view(), name='home'),
]
```

The way Django works, now when a user goes to the homepage of our website they will first
hit the `config/urls.py` file, then be redirected to `books/urls.py` which specifies using the
BookListView. In this view file, the ***Book*** model is used along with ListView to list out all books.


### Webpages

The final step is to create our template file that controls the layout on the actual web page.

```html
<!-- books/templates/books/book_list.html -->
<h1>All books</h1>
{% for book in object_list %}
<ul>
<li>Title: {{ book.title }}</li>
<li>Subtitle: {{ book.subtitle }}</li>
<li>Author: {{ book.author }}</li>
<li>ISBN: {{ book.isbn }}</li>
</ul>
{% endfor %}
```

and we can now run the server and navigate to our homepage to see all our books listed

    $ python manage.py runserver


### Django Rest Framework

Django REST Framework is added just like any other third-party app.

    $ pipenv install djangorestframework

Add rest_framework to the INSTALLED_APPS config in our config/settings.py file

```python
# config/settings.py
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 3rd party
    'rest_framework', # new
    # Local
    'books',
]
```

Ultimately, our API will expose a single endpoint that lists out all books in JSON. So we will need
a new URL route, a new view, and a new serializer file

There are multiple ways we can organize these files however my preferred approach is to create
a dedicated ***api*** app. That way even if we add more apps in the future, each app can contain the
models, views, templates, and urls needed for dedicated webpages, but all API-specific files for
the entire project will live in a dedicated api app.

    $ python manage.py startapp api

```python
# config/settings.py
INSTALLED_APPS = [
    # Local
    'books.apps.BooksConfig',
    'api.apps.ApiConfig', # new

    # 3rd party
    'rest_framework',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]
```


### Urls

First at the project-level we need to include the api app and configure its
URL route, which will be api/.

```python
# config/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')), # new
    path('', include('books.urls')),
]
```

Then create a urls.py file within the api app.

```python
# api/urls.py
from django.urls import path
from .views import BookAPIView

urlpatterns = [
    path('', BookAPIView.as_view()),
]
```


### Views

Next up is our views.py file which relies on Django REST Framework’s built-in generic class
[views](https://www.django-rest-framework.org/api-guide/generic-views/#generic-views). These deliberately mimic traditional Django’s generic class-based views in format, but
they are not the same thing.

```python
# api/views.py
from rest_framework import generics
from books.models import Book
from .serializers import BookSerializer

class BookAPIView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
```

we create a ***BookAPIView*** that uses ListAPIView to create a read-only endpoint for all
book instances. There are many generic views available and we will explore them further in later
chapters.

The only two steps required in our view are to specify the queryset which is all available books,
and then the serializer_class which will be BookSerializer.


### Serializers

A serializer translates data into a format that is easy to consume over the internet, typically
JSON, and is displayed at an API endpoint.

Make a serializers.py file within our api app.

```python
# api/serializers.py
from rest_framework import serializers
from books.models import Book

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ('title', 'subtitle', 'author', 'isbn')
```

We extend Django REST Framework’s [ModelSerializer](https://www.django-rest-framework.org/api-guide/serializers/#modelserializer) into a BookSerializer
class that specifies our database model Book and the database fields we wish to expose: title,
subtitle, author, and isbn.
That’s it! We’re done.


### cURL

run your server 

    $ python manage.py runserver

and in a new temrinal run:

    $ curl http://127.0.0.1:8000/api/
    [
        {
            "title":"Django for Beginners",
            "subtitle":"Build websites with Python and Django",
            "author":"William S. Vincent",
            "isbn":"9781735467207"
        }
    ]


### Browsable API

With the local server still running in the first command line console, navigate to our API endpoint
in the web browser at http://127.0.0.1:8000/api/.

Django REST Framework provides this visualization by default


## Chapter 3: Todo API


### DRF

We also want to start configuring Django REST Framework specific settings which all exist
under REST_FRAMEWORK. For starters, let’s explicitly set permissions to [AllowAny](https://www.django-rest-framework.org/api-guide/permissions/#allowany)

Django REST Framework has a lengthy list of implicitly set default settings. You can see the
complete list [here](https://www.django-rest-framework.org/api-guide/settings/). `AllowAny` 
is one of them which means that when we set it explicitly, as we did above, the effect is 
exactly the same as if we had no DEFAULT_PERMISSION_CLASSES config set.


### Views

In traditional Django views are used to customize what data to send to the templates. In Django
REST Framework views do the same thing but for our serialized data.

Recall from our todos/urls.py file that we have two routes and therefore two distinct views.
We will use [ListAPIView](https://www.django-rest-framework.org/api-guide/generic-views/#listapiview) to display all todos and [RetrieveAPIView](https://www.django-rest-framework.org/api-guide/generic-views/#retrieveapiview) to display a single model instance.
instance.

### [CORS](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS)

Whenever a client interacts with an API hosted on a different domain (mysite.com vs yoursite.com) or port (localhost:3000 vs localhost:8000) there are potential security issues.
Specifically, CORS requires the server to include specific HTTP headers that allow for the client
to determine if and when cross-domain requests should be allowed.

The easiest way to handle this and the [one](https://www.django-rest-framework.org/topics/ajax-csrf-cors/)
recommended by DRF is to use middleware that will automatically include the appropriate HTTP headers
based on our settings.

---
Build web APIs with Python and Django by William S Vincent