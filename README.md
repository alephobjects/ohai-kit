Open Hardware Assembly Instruction Kit
---

# Introduction
OHAI-KIT is a web application using the Django web framework.
It's a comprehensive, accessible source for putting together your newest piece of machinery. Aiming to create clear and concise instruction for optimal assembly, the OHAI-kit features step-by-step instructions, illustrative pictures, and thorough check-point to be sure all steps have been covered.

# Installation
## Requirements
OHAI-kit requires the following dependencies :

* Django >= 1.7
 * Python
* easy_thumbnails
* django.contrib.markup
* **_Optional : _** Apache
 * mod_wsgi

### Django
OHAI-kit depends on Django version 1.7 or latest. 
You will first need to install Django, please refer to the [Django installation tutorial](https://docs.djangoproject.com/en/dev/topics/install/)

Once installed, run the command :
`python -c "import django; print(django.get_version())"`
And make sure that the django version is at least 1.7.

### easy_thumbnails
Install easy_thumbnails by using the command :
`sudo pip install easy_thumbnails`

### Django-markup
OHAI-kit requires the django.contrib.markup package installed.
However, the markup package was deprecated since django 1.5, you can however still get it from the django 1.5 tree :
`https://github.com/django/django/blob/1.5c2/django/contrib/markup/templatetags/markup.py`
Copy the markup.py file to the _ohai-kit/templatetags_ directory.

# Configuring the Django project
OHAI-kit is a django application. You will first need to create a django project
in which to use the ohai_kit application. 

## Creating a project
Start by creating a django project with the command :
`django-admin startproject myproject`
Where 'myproject' can be any name you want to give the project.

## Adding the ohai_kit application
Copy the ohai_kit application directory to the newly created myproject directory.
You will have a directory structure similar to this :
```
myproject/manage.py                 -- Django manage.py script
myproject/myproject/__init__.py     -- Empty file
myproject/myproject/settings.py     -- Project settings
myproject/myproject/urls.py         -- Project URL settings
myproject/myproject/wsgi.py         -- Project WSGI application
myproject/ohai_kit                  -- ohai_kit application
myproject/ohai_kit/__init__.py
myproject/ohai_kit/models.py
myproject/ohai_kit/admin.py
myproject/ohai_kit/urls.py
myproject/ohai_kit/tests.py
myproject/ohai_kit/views.py
myproject/ohai_kit/management/
myproject/ohai_kit/templatetags/     -- Directory in which you added markup.py
myproject/ohai_kit/migrations/
myproject/ohai_kit/static/
myproject/ohai_kit/templates/
```

## Setting up the project
Edit the **_myproject/settings.py_** file, and add to the *INSTALLED_APPS* variable, the *easy_thumbnails* and *ohai_kit* apps, such that the variable looks like this :
```
  INSTALLED_APPS = (
      'django.contrib.admin',
      'django.contrib.auth',
      'django.contrib.contenttypes',
      'django.contrib.sessions',
      'django.contrib.messages',
      'django.contrib.staticfiles',
      'easy_thumbnails',
      'ohai_kit',
  )
```

## Configuring the database
You can then configure the database to use. By default, the django project will use a sqllite3 database in the local file **db.sqlite3** in the project's base directory.
Refer to the [Django database documentation](https://docs.djangoproject.com/en/dev/ref/settings/#databases) for information on how to set-up your database.
You can either leave it as the default :
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
```
Or set it up to use a MySQL database for example :
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'mydatabase',
        'USER': 'mydatabaseuser',
        'PASSWORD': 'mypassword',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}
``` 

Once the database is configured, you must then create the database by running the command :
`python manage.py migrate`

If you update OHAI-kit or install other application or modify anything relating to the database, you must again call the migrate command.

## Configuring the URLs
You can now add a URL to the project that would resolve to the ohai_kit application by editing the **myproject/urls.py** file and adding a _url_ line to it.
Refer to the [Django URL functions](https://docs.djangoproject.com/en/dev/ref/urls/) for more information.

For example, to have the ohai-kit application run under the url http://mywebsite.com/ohai-kit/ you can add the following line to **myproject/urls.py**
` url(r'^ohai-kit/', include('ohai_kit.urls', namespace='ohai_kit')),`

For turning the entire site into the ohai-kit application, add the following line instead :
` url(r'^', include('ohai_kit.urls', namespace='ohai_kit')),`

You should end up with a **myproject/urls.py** containing somthing similar to this :
```
from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('ohai_kit.urls', namespace='ohai_kit')),
)
```


## Creating administrator user
You must then create the administrator user for the OHAI-kit installation by running the following command :
`python manage.py createsuperuser`
Then follow the instructions on screen to create the administrator user for the application.

## Running OHAI-kit
Now that the django project is created and configured, you can test it by running the command : 
`python manage.py runserver`
This will run a local http server on port 8000 and print the address of the server, which will be by default **http://127.0.0.1:8000/**.
You can then enter that URL in your browser to test the server, and specify the URLs you used in **myproject/urls.py** to access the admin page or OHAI-kit.

You can run the server on any ip:port you want and use it directly on your production server. For more information on the available options, you can run :
`python manage.py help runserver`

# Configuring Apache
You can run OHAI-Kit from Apache using the *mod_wsgi* module. You can read the instructions for deploying Django projects using Apache and mod_wsgi from the relevent [Django documentation page](https://docs.djangoproject.com/en/dev/howto/deployment/wsgi/modwsgi/).

// TODO: add excerpt of ohai.conf and static page settings and database and file permissions

# Configuring OHAI-Kit

