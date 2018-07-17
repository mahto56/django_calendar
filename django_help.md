Django Reference (1.6+)
---------

For more comprehensive notes: https://github.com/pebreo/django-notes

Migrations
--------
```
# show migrations
./manage.py migrate --list

# For Django>=1.7
# If you didn't change your model
./manage.py migrate

# If you changed your model
./manage.py makemigrations
./manage.py migrate

# For Django<=1.6
# If you changed your model
./manage.py schemamigration myapp --initial
./manage.py migrate myapp

# If you don't have any old data
./manage.py syncdb --all
./manage.py migrate --fake 


# Specify which migration to use: South or Django built-in migrations
MIGRATION_MODULES = [
    'aldryn_people': 'aldryn_people.south_migrations',
    # or
    'aldryn_people': 'aldryn_people.django_migrations',
]

# what if data already exists and it complains of unmigrated migrations?
./manage.py migrate --list
./manage.py migrate --fake

# in south
./manage.py migrate --all --fake

```

dumpdata and loaddata
--------------
```python
# dumpdata for specific app
./manage.py dumpdata myapp > /tmp/myapp.json

# dumpdata for a specific table 
./manage.py dumpdata admin.logentry > /tmp/logentry.json

# loaddata basic
./manage.py loaddata /tmp/user.json

# restore fresh database
./manage.py dumpdata --exclude auth.permission --exclude contenttypes > /tmp/db.json
./manage.py loaddata /tmp/db.json
```

Django+IPython Notebook
-------------
```
pip install "ipython[all]"
pip install django-extensions==1.5.6
add "django_extensions" to INSTALLED_APPS

# create ipython_config.py next to manage.py file and it should have the following contents:
###################################################
c = get_config()

# Allow all IP addresses to use the service and run it on port 80.
c.NotebookApp.ip = '0.0.0.0'
c.NotebookApp.port = 80

# Don't load the browser on startup.
c.NotebookApp.open_browser = False
###################################################


# run this command
./manage.py shell_plus --notebook

# finally, click New-> Django-Shell Plus
```

Views imports
-------------
```python
from django.http import HttpResponse, HttpResponseRedirect
from django.http import Http404t

from django.shortcuts import render_to_response
from django.shortcuts import redirect
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse

from django.template import RequestContext
from django.db.models.loading import get_model
from django.views.generic import ListView
from django.db.models import Count

from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import method_decorator
from django.conf import settings

from another_app.models import YourModel
from another_app.views import is_foo

from django.contrib.auth.models import User

# DRF View imports
from snippets.models import Snippet
from snippets.serializers import SnippetSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

def my_view(request):
    ...
    return redirect('some-view-name', foo='bar')

def login(request):
    # how to grab request context
    context = RequestContext(request, {
         'request': request, 'user': request.user})
    return render_to_response('login.html', context_instance=context)
    
def index(request, template='journal/index.html'):
    # Redirect if not logged in.
    if not request.user.is_authenticated():
        return HttpResponse('you must be logged in')
    context = None
    return render(request, template, context)
```

Static configuration
--------------------
```python
import os
STATIC_ROOT - target directory for collectstatic
STATICFILES_DIRS - additional locations that collectstatic and findstatic will traverse
MEDIA_ROOT - directory that contains user uploaded files

STATIC_URL = '/static/'
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(HTDOCS_ROOT,  'media')
STATIC_ROOT = os.path.join(HTDOCS_ROOT,  'static')

STATICFILES_DIRS = (
    os.path.join(PROJECT_ROOT, 'static'),
)
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django.contrib.staticfiles.finders.DefaultStorageFinder',
    #'compressor.finders.CompressorFinder',
)
===
BASE_DIR = dirname(dirname(__file__))

APPS_PATH = join(BASE_DIR, 'apps')

current working directory
print os.path.dirname(os.path.realpath(__file__))
```

URL bootstrap
---------------
```python
from django.conf.urls import patterns, include, url 
from django.shortcuts import redirect 
from django.core.urlresolvers import reverse

from django.views.generic.base import RedirectView 
from django.views.generic import TemplateView

from django.contrib import admin
admin.autodiscover()

from accounts.views import MyView

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'lulu.views.home', name='home'),
    # url(r'^reputationconsole/', include('lulu.foo.urls')),
    url(
        r'^admin/doc/', 
        include('django.contrib.admindocs.urls')
    ),
    url(
        r'^admin/', 
        include(admin.site.urls)
    ),
    url(
        r'^api-auth/', 
        include('rest_framework.urls', 
        namespace='rest_framework')
    ),
    url(
        r'^api/v1/', 
        include('myapi.urls')
    ),          
    url(
        r'^accounts/', 
        include('userena.urls')
    ),
    url(
        r'^faq/?', 
        include('faq.urls')
    ),

    url(
        r'^reportingcenter/', 
        include('reportingcenter.urls')
    ),
    url(
        r'^unsubscribe/(?P<unsubscribe_key>[a-zA-Z0-9].*)/?$',
        UnsubscribeView.as_view(),
        name="Email Unsubscribe"
    ),
    url(
        r'^', 
        include('app.urls')
    ),    

)

# app/urls.py
from django.conf.urls import *
from myapp.views import IndexView

urlpatterns = patterns('',
    url(r'^$', view=IndexView.as_view(), name="myapp_index"),
    url(r'^signup/', RedirectView.as_view(url='/accounts/signup')),
)

#convert URL to new type
http://stackoverflow.com/questions/14882491/django-release-1-5-url-requires-a-non-empty-first-argument-the-syntax-change/15373978#15373978

command:
find . -type f -print0 | xargs -0 sed -i 's/{% url \([^" >][^ >]*\)/{% url "\1"/g'
```

Template example
-------
```html

{% extends "base.html" %}

{% block stylesheets %}
{{ block.super }}
<link rel="stylesheet" href="{{ STATIC_URL }}css/smoothness/jquery-ui-1.8.20.custom.css" />
<link type="text/css" rel="stylesheet" href="{{ STATIC_URL }}css/slickgrid/slick.grid.css">
<link type="text/css" rel="stylesheet" href="{{ STATIC_URL }}css/grid.css">
{% endblock %}

{% incled 'navbar.html' %}

{% block content %}

{% if request.user.is_superuser %}
    {{ blah }}
{% endif %}

<ul>
    {% for publisher in object_list %}
    <li>{{ publisher.name }}</li>
    {% endfor %}
</ul>

{% endblock %}

```
Django manage.py
------------
```bash
django-admin.py startproject
./manage.py startapp
./manage.py dbshell

./manage.py runserver 0.0.0.0:8000

# dbshell commands - postgres
> \dt # show tables
> drop table mytable; # delete table
> truncate mytable; # clear table
> select * from mytable limit 100;
> \q # quit

# dbshell commands - sqlite
> .tables  # show tables
> .q   # exit
```

Django manage.py
------------
```bash
django-admin.py startproject
./manage.py startapp
./manage.py dbshell

./manage.py inspectdb > models.py # create models based on an existing table

./manage.py runserver 0.0.0.0:8000

# dbshell commands - postgres
> \dt # show tables
> drop table mytable; # delete table
> truncate mytable; # clear table
> select * from mytable limit 100;
> \q # quit

# dbshell commands - sqlite
> .tables  # show tables
> .q   # exit
```

Running tests
-----
```bash
./manage.py test # test all
./manage.py test myapp # test app

# test specific test
./manage.py test myapp.tests.MyTest.test_something

```

Model Admin customization
-------------------------
```python
#admin.py
from django.db import models


class Post(models.Model):
    title = models.CharField('title', max_length=64)
    slug = models.SlugField(max_length=64)
    content = models.TextField('content')
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        permissions = (
            ('view_post', 'Can view post'),
        )
        get_latest_by = 'created_at'

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return {'post_slug': self.slug}
        
    def save(self, *args, **kwargs):
        """Save model and start a celery task"""
        super(Post, self).save(*args, **kwargs)
        # do other stuff here like schedule a celery task or something
```

Views 
-----
```python
# docs: https://docs.djangoproject.com/en/1.8/ref/contrib/auth/

from rango.forms import UserForm, UserProfileForm

def register(request):

    # A boolean value for telling the template whether the registration was successful.
    # Set to False initially. Code changes value to True when registration succeeds.
    registered = False

    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm.
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        # If the two forms are valid...
        if user_form.is_valid() and profile_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()

            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.set_password(user.password)
            user.save()

            # Now sort out the UserProfile instance.
            # Since we need to set the user attribute ourselves, we set commit=False.
            # This delays saving the model until we're ready to avoid integrity problems.
            profile = profile_form.save(commit=False)
            profile.user = user

            # Did the user provide a profile picture?
            # If so, we need to get it from the input form and put it in the UserProfile model.
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            # Now we save the UserProfile model instance.
            profile.save()

            # Update our variable to tell the template registration was successful.
            registered = True

        # Invalid form or forms - mistakes or something else?
        # Print problems to the terminal.
        # They'll also be shown to the user.
        else:
            print user_form.errors, profile_form.errors

    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    # Render the template depending on the context.
    return render(request,
            'rango/register.html',
            {'user_form': user_form, 'profile_form': profile_form, 'registered': registered} )

from django.http import Http404
def my_view(request):
    try:
        my_object = MyModel.objects.get(pk=1)
    except MyModel.DoesNotExist:
        raise Http404("No MyModel matches the given query.")
```

ModelAdmin and Inlines
--------------------
Example model
```python
from django.db import models
from django.contrib import admin

class Topic(models.Model):
    title = models.CharField(max_length=20)
    time = models.DateTimeField(auto_now_add=True)
    
    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ['-time']

class Lesson(models.Model):
    title = models.CharField(max_length=20)
    time = models.DateTimeField(auto_now_add=True)
    slug =  models.SlugField()
    content = models.TextField
    
    # NOTE: A Topic has many lessons so we put that foreign key in Lessons, we don't create a ForeignKey in Topic
    # Topic.objects.filter(lessons__title__iname='foo')
    # or, if there was no 'related_name' Topic.lesson_set.all()
    # or Topic.lessons.all()
    topic = models.ForeignKey(Topic, related_name='lessons')
    
    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ['-time']

class LessonInlineAdmin (admin.TabularInline):
    """Inline configuration for Django's admin on the Lesson model."""
    model = Lesson
    extra = 8
    def get_extra (self, request, obj=None, **kwargs):
        """Dynamically sets the number of extra forms. 0 if the related object
        already exists or the extra configuration otherwise."""
        if obj:
            # Don't add any extra forms if the related object already exists.
            return 0
        return self.extra


class TopicAdmin (admin.ModelAdmin):
    """Configuration for Django's admin on the Topic model."""
    inlines = [ LessonInlineAdmin ]


admin.site.register(Topic, TopicAdmin)
#admin.site.register(Lesson, Lesson)

```

Modeladmin - better formatting
-------------------------------
```python

# screenshot: https://dl.dropboxusercontent.com/s/5yg9wc752gbpqev/__django-meta-and-modeladmin.png?dl=0
# models.py
class SuperHero(models.Model):
    name = models.CharField(max_length=100)
    added_on = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return "{} - {1:%Y-%m-%d %H:%M:%S}".format(self.name, self.added_on)
        
    def get_absolute_url(self):
        return reverse('superhero.views.details', args=[self.id])
    
    class Meta:
        ordering = ["-added_on"]
        verbose_name = "superhero"
        verbose_name_plural = "superheroes"

# admin.py
class SuperHero(admin.ModelAdmin):
    list_display = ('name', 'added_on')
    search_fields = ["name"]
    ordering = ["name"]
```

User Profile w/ Userena
----------------------
"If you would like to include other attributes than what is provided by the User model, then you will needed to create a model that is associated with the the User model."

```python
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from userena.models import UserenaBaseProfile

class UserProfile(UserenaBaseProfile):
    user = models.OneToOneField(User,
                                unique=True,
                                verbose_name=_('user'),
                                related_name='my_profile')
    favourite_snack = models.CharField(_('favourite snack'),
                                       max_length=5)
    customer_ID = models.CharField(max_length=255,blank=True,null=True)
    
    # Override the __unicode__() method to return out something meaningful!
    def __unicode__(self):
        return self.user.username
        

u = User.objects.filter(username='test1')[0]

u = User.objects.get(username='test1')

MyProfile.objects.all()

MyProfile.objects.select_related()

MyProfile.objects.get(user__username='test1')
```

Session data
-----------

```python

request.method == 'GET' 
# or 'POST'

request.session['mycookievar']

request.POST['stripeToken'] # e.g. <input type="hidden" name="stripeToken" />

request.GET['q'] # e.g. /?q=foo

request.user.id # the user id

form.cleaned_data['input_name']

def login(request):
    m = Member.objects.get(username=request.POST['username'])
    if m.password == request.POST['password']:
        request.session['member_id'] = m.id
        return HttpResponse("You're logged in.")
    else:
        return HttpResponse("Your username and password didn't match.")

# cookies        
def login(request):
    if request.method == 'POST':
        if request.session.test_cookie_worked():
            request.session.delete_test_cookie()
            return HttpResponse("You're logged in.")
        else:
            return HttpResponse("Please enable cookies and try again.")
        request.session.set_test_cookie()
    return render_to_response('foo/login_form.html')
```


Django ORM Queries
-----------------
```python
'''
ManyToMany vs ForeignKey

If each car has one manufacturer, then you should use a foreign key from Car to Manufacturer. 
This will allow multiple cars to have the same manufacturer, 
and manufacturers will not be deleted when cars are deleted. 
A many to many field suggests that one car can have multiple manufacturers.

source: http://stackoverflow.com/questions/8872030/confused-about-django-foreignkey-manytomanyfield-inlineformset-factories
'''
# give these models
from django.db import models

class Blog(models.Model):
    name = models.CharField(max_length=100)
    tagline = models.TextField()

    def __unicode__(self):              # __str__ on Python 3
        return self.name

class Author(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()

    def __unicode__(self):              # __str__ on Python 3
        return self.name

class Entry(models.Model):
    blog = models.ForeignKey(Blog)
    authors = models.ManyToManyField(Author)
    body_text = models.TextField()
    pub_date = models.DateField()

    def __unicode__(self):              # __str__ on Python 3
        return self.headline
        
        
# CREATE
from blog.models import Blog

b = Blog(name='Beatles Blog', tagline='All the latest Beatles news.')
b.save()

# saving for 'ForeignKey' relationships
from blog.models import Entry
entry = Entry.objects.get(pk=1)
cheese_blog = Blog.objects.get(name="Cheddar Talk")
entry.blog = cheese_blog
entry.save()

# saving for 'ManyToManyField' relationships
from blog.models import Author
joe = Author.objects.create(name="Joe")
entry.authors.add(joe)

john =  Author.objects.create(name="John")
paul =  Author.objects.create(name="Paul")
entry.authors.add(john, paul)

# UPDATE
b.name = 'New name'
b.save()

# GET
Entry.objects.get(id=1) 
Entry.objects.get(id__exact=1) # same as above
Entry.objects.get(pk=1)  # same as above
Entry.objects.filter(id=1)[0] # same as above

# FILTER

Entry.objects.filter(pub_date__year=2006) 
# same as
Entry.objects.all().filter(pub_date__year=2006)
Entry.objects.filter(pub_date__lte='2006-01-01') # sql: SELECT * FROM blog_entry WHERE pub_date <= '2006-01-01';

# iexact
Blog.objects.get(name__iexact="beatles blog")
# contains
Entry.objects.get(headline__contains='Lennon')

# chaining
Entry.objects.filter(headline__startswith='What')
             .exclude(pub_date__gte=datetime.date.today())
             .filter(pub_date__gte=datetime(2005, 1, 30))

# first entry
Entry.objects.order_by('headline')[0]
# same as
Entry.objects.order_by('headline')[0:1].get()

# filtering relationships
Entry.objects.filter(blog__name='Beatles Blog')
Blog.objects.filter(entry__headline__contains='Lennon')
Blog.objects.filter(entry__authors__name='Lennon')

Blog.objects.filter(entry__headline__contains='Lennon',
        entry__pub_date__year=2008)
        
Blog.objects.filter(entry__headline__contains='Lennon')
            .filter(entry__pub_date__year=2008)
        
# DELETE
b.delete()
```

Django ORM query examples
---------------------
```python

# show duplicate values 

import collections
L = Entry.objects.values_list('slug')
slugs_duplicates = [x for x, y in collections.Counter(L).items() if y > 1]
pks_of_duplicates = Entry.objects.filter(slug__in=slugs_with_duplicates).values_list('pk')

```

JMeter
--------------
```
Search : jmeter download and download the tgz

Note: thread=users
1.
Right click "Test Plan" -> add Thread Group

Number of threads: 10 # number of clients
Ramp-up period: 0   # all clients start at same time
Loop count: 100    # number of requests per client

2.
Right click on Thread Group -> Config Element -> Http Request Defaults

Server Name or IP: localhost (or 192.168.23.11)
Port: 8000 # or whatever it should be

3. Right click on Thread Group -> Sampler -> Http Request
specify path: /

4. Right click on Thread Group -> Listener -> View Results Tree
  Right click on Thread group -> Listener -> Aggregate report
  
5. While Aggregate report is selected: Click Play icon on the top

Analysis
Throughput:
Throughput => number of requests per second your server can handle
Reponse time:
90% percentile => number of milliseconds it can respond

Note: if you want to test new results you should remove and re-add the Listeners
```

django forms notes
----------------
```html

// ideally, you should haven to pass arguments to the view, but instead use hidden field values and grab with POST.get()
<form method="POST" action="{% url 'create_comment' %}">
// if your view needs arguments
<form method="POST" action="{% url 'create_comment' arg1=1 arg2=comment.foo %}">

<input type="hidden" id="parent_id" value="{{comment.parent_id}}">
<input type="hidden" id="comment_id" value="{{comment.id}}">

# in the view
request.POST.get('parent_id') 
request.POST.get('comment_id')
```

Search approach 1
-------
```python

BELOW IS CODE FOR A HYPOTHETICAL SEARCH APP FOR A HYPOTHETICAL BLOG

# forms.py

from django import forms
TOPIC_CHOICES = ((1,'topic1'),(2,'topic2'),(3,'topic3'))
class SearchForm(forms.Form):
    '''
    Form to search based on blog text and topic
    '''
    blog_text = forms.CharField(required=False,label='BLOG TEXT')
    # a dropdown 
    topic = forms.ChoiceField(required=False,widget=forms.Select,choices=TOPIC_CHOICES)
    
# views.py
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.views.generic import TemplateView
from django.db.models import Q

from .forms import SearchForm
from .models import Blog

class SearchFormView(TemplateView):
    '''
    Render the form
    '''
    template_name = 'myapp/searchform.html'
    def get_context_data(self, **kwargs):
        context = super(SearchView, self).get_context_data(**kwargs)
        form = SearchForm()
        context.update({'form':form})
        return context

def mysearch(request, template_name='search_results.html'):
    '''
    Run a sequence of filters using Q objects
    '''
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            entries = Blog.objects.all()
            if form.cleaned_data['blog_text'] != '':
                q = Q(entry__icontains=form.cleaned_data['blog_text'])
                entries = entries.filter(q)
            if form.cleaned_data['category'] != '':
                q = Q(category__exact=form.cleaned_data['category'])
                entries = entries.filter(q)
            return render(request, template_name, {'object_list':entries})
    
    return redirect(reverse('searchform_view'))
    
# searchform.html 
<html>
<form id="search" action="post" action="{% url 'searchresult_view' %}"> 
{{form.as_ul}}
  <input type="submit" value="Pay $25">
 </form>
</html>

# searchresults.html 
<html>
{% for r in object_list %}
{{r.title}}
{{r.date_published}}
{% endfor %}
</html>

# app/urls.py
from django.conf.urls import *
from .views import SearchFormView, mysearch

urlpatterns = patterns('',
    url(r'search/',SearchView.as_view(), name="searchform_view"),
    url(r'searchresult/', mysearch, name="searchresult_view"),
)
````

Search approach 2
-----------------
```python

EVERYTHING IS THE SAME AS ABOVE EXCEPT THE SEARCH VIEW
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.views.generic import TemplateView
from django.db.models import Q

from .forms import SearchForm
from .models import Blog
import operator

def searchresult_view(request,template_name='myapp/searchresults.html'):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            predicates = [('entry__icontains', 'entry'), ('category__exact', 'category')]
            q_list = [Q(p) for p in predicates]
            final_Q = reduce(operator.and_, q_list)
            
            entries = Blog.objects.filter(final_Q)
            return render(request, template_name, {'object_list':entries})
            
    return redirect(reverse('searchform_view'))


```

Django class based view (CBV) overrides
--------------------------------------
```python

class DojoSearchResultView(ListView):
    model = MyModel
    template_name="myapp/myapp_search.html"
    queryset = MyModel.objects.all()
    
    def dispatch(self, request, q, *args, **kwargs):
        # do stuff here...
        self.extra_context = [1,2,3]
        return super(MyView, self).dispatch(request, q, *args, **kwargs)

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(MyView, self).get_context_data(**kwargs)
        context.update(self.extra_context)
        return context
        
    def get_queryset(self):
        queryset = super(MyView, self).get_queryset()
        queryset = MyModel.objects.filter(foo=True)
        return queryset
        
# login decorator

from django.views.generic import View
from django.views.generic.base import TemplateView, TemplateResponseMixin, ContextMixin
django.utils.decorators import method_decorator 
from django.contrib.auth.decorators import login_required

class MyView(ContextMixin, TemplateResponseMixin, View):
    @method_decorator(login_view)
    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context["title"] = "some other title"
        return self.render_to_response(context)
```

Django user model actions
-----------------------
```python
from django.contrib.auth import get_user_model

User = get_user_model()
u = User(username='foo', email='myemail', is_active=True)
u.save()

```

Django unit tests
--------------
```python

def setUp(self):
    rf = RequestFactory()
    api_client = 

def test_that_page_serves_correct_content(self):

def test_that_url_exists(self):

def test_response(self):
    # GET NOT ALLOWED
    
    # POST response is correct format

```

Django populate script 
---------------------
```python
# source: https://github.com/danielveazey/rango/blob/master/populate_rango.py

__author__ = 'daniel'

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tango_with_django_project.settings')

import django
django.setup()

from rango.models import Category, Page


def populate():
    python_cat = add_cat('Python', 128, 64)

    add_page(cat=python_cat,
             title="Official Python Tutorial",
             url="http://docs.python.org/2/tutorial/",
             views=15)
             
    # print additions for user
    for c in Category.objects.all():
        for p in Page.objects.filter(category=c):
            print "- {0} - {1}".format(str(c), str(p))


def add_page(cat, title, url, views):
    p = Page.objects.get_or_create(category=cat, title=title)[0]
    p.url=url
    p.views=views
    p.save()
    return p


def add_cat(name, views, likes):
    c = Category.objects.get_or_create(name=name)[0]
    c.views = views
    c.likes = likes
    c.save()
    return c


# start execution here
if __name__ == '__main__':
    print "Starting Rango population script ..."
    populate()
```

Twitter clone
------------
```python
# models.py

from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin
from django.core.exceptions import ObjectDoesNotExist

class ProfileManager(models.Manager):
    def get_followers(self, username):
        try:
            return Profile.objects.get(user__username=username).followers.all()
        except ObjectDoesNotExist:
            pass
        return None

class Profile(models.Model):
    user = models.OneToOneField(User)
    objects = ProfileManager()

    def __unicode__(self):
        return self.user.username

class Follower(models.Model):
    user = models.OneToOneField(User)
    # a profile has many followers
    profile = models.ManyToManyField(Profile, related_name='followers')

    def __unicode__(self):
        return "follower: %s" % self.user.username

class ProfileAdmin(admin.ModelAdmin):
    pass

class FollowerAdmin(admin.ModelAdmin):
    pass

admin.site.register(Profile, ProfileAdmin)
admin.site.register(Follower, FollowerAdmin)

'''
from myapp.models import *
from django.contrib.auth.models import User

# create user and profile
u1 = User(username='userAlpha')
u1.save()
prof1 = Profile(user=u1)
prof1.save()

# create follower
u9 = User(username='follower1')
u9.save()

f1 = Follower(user=u9)
f1.save()
f1.profile.add(prof1)

# get all followers
 Profile.objects.get(id=1).follower_set.all()
 or, Profile.objects.get(id=1).followers.all()
 or, Profile.object.get_followers(username='myusername')

# get all people you are following
f1.profile.all()


'''
```

ForeignKey vs ManyToMany Examples
------------------------------
```python
from django.db import models

 # manufacturer
 class Manufacturer(models.Model):
    name = models.CharField(blank=True, max_length=255)
# car - use foreignkey because a car only has one manufacturer
class Car(models.Model):
    name = models.CharField(blank=True, max_length=255)
    manufacturer = models.ForeignKey(Manufacturer, related_name='cars')
'''
from myapp.models import *
toyota = Manufacturer(name='toyota')
toyota.save()

corolla = Car(name='corolla', manufacturer=toyota)
corolla.save()

Manufacturer.objects.get(name='toyota').cars.all()
'''
# ==========================================================================
# recipe
class Recipe(models.Model):
    name = models.CharField(blank=True, max_length=255)
# ingredient
# use manytomany because if you delete an ingredient it won't delete the recipe
class Ingredient(models.Model):
    name = models.CharField(blank=True, max_length=255)
    # a recipe has many ingredient
    recipe = models.ManyToManyField(Recipe, related_name='ingredients')
'''
pancakes = Recipe(name='pancakes')
pancakes.save()
eggs = Ingredient(name='eggs')
eggs.save()
eggs.recipe.add(pancakes)
eggs.save()
flour = Ingredient(name='flour')
flour.save()
flour.recipe.add(pancakes)
'''
```

Useful utilities
---------------

Django-compressor
--------------
Compresses linked and inline JavaScript or CSS into a single cached file.
```html
//Example

{% load compress %}
{% compress css %}
<link rel="stylesheet" href="/static/css/one.css" type="text/css" charset="utf-8">
<style type="text/css">p { border:5px solid green;}</style>
<link rel="stylesheet" href="/static/css/two.css" type="text/css" charset="utf-8">
{% endcompress %}
```

Misc
```python
   def get_queryset(self):
        entries = []

        for date in Entry.objects.values_list('created__date', flat=True):
            entries.extend(
                Entry.objects.filter(created__date=date).order_by('created')[:N]
            )

        return entries
```

Angular - Common directives
----------------------------
```html

# ng-if 
// Show if the condition is true
<div class="alert" ng-if="myvar"></div>

# ng-hide ; ng-show
<div ng-hide="foo == bar"></div>

# ng-class
ng-class="{'myclass': foo.bar > x}"

# ng-repeat

<ul>
  <li ng-repeat="rule in rules">
  {{ rule.rulename }}
  </li>
</ul>

# ng-click

<input type="button" ng-click="myAlert()"/>

$scope.$watch('mymodel', function() {
    // do something when mymodel changes
});
```

Angular promises and $q
------------------------
```javascript

# in the service
var defer = $q.defer()
    defer.resolve(myData);
    
    defer.reject('my reason');
return defer.promised;

# in the controller
myService
.then(handleSuccess)
.catch(handleFailure)


# For $http
# in the myAPIService

// A SIMPLE EXAMPLE ON USING q OBJECT TO MAKE PROMISES
/// AND STORING DATA IN THESO PROMISES
app.factory("myService", [ "$http", "$q" ,function($http, $q){

    var deferred = $q.defer();

    $http.get('/my/api/point', {

        success: function(data) {
            // optional
            deferred.resolve(data);
        },
        fail: function(message) {
            // optional
            deferred.fail(message); //?
        },

    });

    return deferred.promise;

}]);

// USAGE
app.controller("MyCtrl"["myService", function(myService){

    myService.myFunc
        .then(handleSuccess)
        .catch(handleFail)

    function handleSuccess(data) {

        $scope.data = data;
    };

    function handleFail(message) {
        console.log(message);
    };

}]);

```

Windows installation
------------
```
- Google : "python for windows" and download python 3.6.x
- run: cmd
- $ python
- $ pip install virtualenv
- $ virtualenv dj18
- $ .\dj18\Scripts\activate.bat
or in git bash:
- $ source .\dj18\Scripts\activate
- $ pip install django==1.8
- $ django-admin startproject mysite
- $ cd mysite
- $ python manage.py runserver  - goto localhost:8080 or http://192.168.1.1:8080

To make a new django app
- $ python manage.py startapp polls
- edit your model
- $ python manage.py makemigrations polls
- $ python manage.py migrate
- $ python manage.py createsuperuser # for the first time only
```

Docker for Windows 7
------------------
```
- google: "docker windows 7" and download Docker Toolbar
- make sure that git is installed during installation
- when the installation dialog is finished, make sure to run the 
    shortcut that finishes off the installation
- $ docker run hello-world
- $ docker images
```

Node for Windows 7
--------
```
- google: "node for windows"
- download "windows installer"
- $ npm install -g gulp
```
