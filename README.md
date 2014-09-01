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
* __*Optional : *__ Apache
 * mod_wsgi

### Django
OHAI-kit depends on Django version 1.7 or latest. 
You will first need to install Django, please refer to the [Django installation tutorial](https://docs.djangoproject.com/en/dev/topics/install/)

At the time of writing, the latest release candidate for 1.7 is 1.7rc3.
Make sure you have installed Python and PyPi (python-pip) from your distribution's package manager, then run :
`sudo pip install https://www.djangoproject.com/download/1.7c3/tarball/`

Once installed, run the command :
`python -c "import django; print(django.get_version())"`
And make sure that the django version is at least 1.7.

### easy_thumbnails
Install easy_thumbnails by using the command :
`sudo pip install easy_thumbnails`

### Django-markup
OHAI-kit requires the django.contrib.markup package installed.
However, the markup package was deprecated since django 1.5, you can however still get it from the django 1.5 tree :
`https://github.com/django/django/1.5c2/django/contrib/markup/`
You can find the path to your django installation by running the following command :
`python -c "import django; print(django.__file__)"`
It should print something like this :
`/usr/lib/python2.7/site-packages/django/__init__.pyc`
Simply create a directory **contrib/markup/** in the django directory and copy the contents of the markup directory to it. 

Alternatively, you can simply download the markup.py file available here :
`https://raw.githubusercontent.com/django/django/1.5c2/django/contrib/markup/templatetags/markup.py`
and copy the markup.py file to the _ohai-kit/templatetags_ directory.

## Example installation
Here is an example log of the installation for Python, PyPi, Django, easy_thumbnails and django-markup : 
```
[root@kakaroto ~]# apt-get install python python-pip; # For Debian
...
[root@kakaroto ~]# yum install python python-pip; # For Fedora
...
[root@kakaroto ~]# pip install https://www.djangoproject.com/download/1.7c3/tarball/`
[root@kakaroto ~]# pip install easy_thumbnails
[root@kakaroto ~]# python -c "import django; print(django.get_version())"
1.7c3
[root@kakaroto ~]# python -c "import django; print(django.__file__)"
/usr/lib/python2.7/site-packages/django/__init__.pyc`
[root@kakaroto ~]# mkdir -p /usr/lib/python2.7/site-packages/django/contrib/markup/templatetags/
[root@kakaroto ~]# touch  /usr/lib/python2.7/site-packages/django/contrib/markup/__init__.py
[root@kakaroto ~]# touch  /usr/lib/python2.7/site-packages/django/contrib/markup/templatetags/__init__.py
[root@kakaroto ~]# wget --quiet -O /usr/lib/python2.7/site-packages/django/contrib/markup/templatetags/markup.py https://raw.githubusercontent.com/django/django/1.5c2/django/contrib/markup/templatetags/markup.py
```

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
Edit the **_myproject/settings.py_** file, and add to the *INSTALLED_APPS* variable, the *django.contrib.markup*, *easy_thumbnails* and *ohai_kit* apps, such that the variable looks like this :
```
  INSTALLED_APPS = (
      'django.contrib.admin',
      'django.contrib.auth',
      'django.contrib.contenttypes',
      'django.contrib.sessions',
      'django.contrib.messages',
      'django.contrib.staticfiles',
      'django.contrib.markup',
      'easy_thumbnails',
      'ohai_kit',
  )
```

If however, you copied the markup.py file to the ohai_kit/templatetags directory instead of installing it, then you can omit the *django.contrib.markup* from the list.

## Configuring the database
You can also configure the database to use in the **_myproject/settings.py_** file. By default, the django project will use a sqllite3 database in the local file **db.sqlite3** in the project's base directory.
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

If you update OHAI-kit or install other applications to your Django project or modify anything relating to the database, you must again call the migrate command.

## Configuring static file deployment
Your django settings will have a **STATIC_URL** option set by default to `/static/`. You can change that value to modify the URL for static file deployments.
You will also need to add the full absolute path where you will want to serve your static files on the server using the **STATIC_ROOT** variable.

For example :
```
STATIC_URL = '/media/'
STATIC_ROOT = '/var/www/myproject/static/'
```

## Configuring media uploads
In order to allow uploads of media to the ohai-kit server, you will need to configure a couple of additional options in **myproject/settings.py**. If you do not properly configure the media uploads, then you may not be able to upload pictures for your assembly instructions.

You will need to add the **MEDIA_URL** and **MEDIA_ROOT** variables to the _settings.py_ file where **MEDIA_URL** will be the URL of your media files and **MEDIA_ROOT** will be the _absolute path_ of your media directory.

For example :
```
MEDIA_URL = '/media/'
MEDIA_ROOT = '/var/www/myproject/media/'
```

## Configuring the URLs
You can now add a URL to the project that would resolve to the `ohai_kit` application by editing the **myproject/urls.py** file and adding a _url_ line to it.
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
Before you can start using Ohai-kit, you must first create the administrator user by running the following command :
`python manage.py createsuperuser`
Then follow the instructions on screen to create the administrator user for the application.

## Running OHAI-kit
Now that the django project is created and configured, you can test it by running the command : 
`python manage.py runserver`
This will run a local http server on port 8000 and print the address of the server, which will be by default **http://127.0.0.1:8000/**.
You can then enter that URL in your browser to test the server, and specify the URLs you used in **myproject/urls.py** to access the admin page or OHAI-kit.

You can run the server on any ip:port you want and use it on your production server. For more information on the available options, you can run :
`python manage.py help runserver`
It might be more secure however to use Apache on a production server.

# Configuring Apache
You can run OHAI-Kit from Apache using the *mod_wsgi* module. You can read the instructions for deploying Django projects using Apache and mod_wsgi from the relevent [Django documentation page](https://docs.djangoproject.com/en/dev/howto/deployment/wsgi/modwsgi/).

## Ohai-kit as a virtual host
In order to integrate Ohai-kit with Apache, you will need the mod_wsgi module loaded and configured and to configure static file deployments.

The following instructions are for Apache 2.4 and later.
We recommend you create a ohai_kit.conf file in your /etc/httpd/conf.d/ directory.

For ohai-kit running as your main server's application, and your django project named 'myproject', your Apache ohai_kit.conf file would look like this :
```
Alias /static/ /var/www/myproject/static/
Alias /media/ /var/www/myproject/media/

<Directory /var/www/myproject/static>
Require all granted
</Directory>

<Directory /var/www/myproject/media>
Require all granted
</Directory>

WSGIScriptAlias / /var/www/myproject/myproject/wsgi.py
WSGIPythonPath /var/www/myproject

<Directory /var/www/myproject/myproject>
<Files wsgi.py>
Require all granted
</Files>
</Directory>
```

You will then need to create a **media** directory in your django project's base directory and copy the static files into the **static** directory using the **collectstatic** command.
```
mkdir /var/www/myproject/media
python manage.py collectstatic
```
The **collectstatic** command of the *manage.py* file will copy all the required static files in the appropriate directories according to your **STATIC_URL** and **STATIC_ROOT** variables defined in the *myproject/settings.py* file.

You must then make sure that the project directory has the proper permissions for access from Apache otherwise the database will be inaccessible.
```chown apache:apache -R /var/www/myproject```

## Ohai-kit configured as a subdirectory of an existing host

// TODO

# Example installation for website ohai.com
Here is an example installation for installing ohai_kit on a website called ohai.com :
```
[root@kakaroto ~]# cd /var
[root@kakaroto var]# django-admin startproject ohai
[root@kakaroto var]# mv ohai/ ohai.com
[root@kakaroto var]# cd ohai.com/
[root@kakaroto ohai.com]# ls
manage.py  ohai
[root@kakaroto ohai.com]# git clone --quiet https://github.com/alephobjects/ohai-kit.git
[root@kakaroto ohai.com]# mv ohai-kit/ohai_kit/ .
[root@kakaroto ohai.com]# rm -rf ohai-kit/
[root@kakaroto ohai.com]# wget --quiet https://raw.githubusercontent.com/django/django/1.5c2/django/contrib/markup/templatetags/markup.py
[root@kakaroto ohai.com]# mv markup.py ohai_kit/templatetags/
[root@kakaroto ohai.com]# vi ohai/settings.py 
[root@kakaroto ohai.com]# grep -A 10 INSTALLED_APPS ohai/settings.py 
INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.markup',
    'easy_thumbnails',
    'ohai_kit',
)
[root@kakaroto ohai.com]# grep -A 5 DATABASES ohai/settings.py 
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
[root@kakaroto ohai.com]# grep -A 3 STATIC_URL ohai/settings.py 
STATIC_URL = '/static/'
STATIC_ROOT = '/var/ohai.com/static/'
MEDIA_URL = '/media/'
MEDIA_ROOT = '/var/ohai.com/media/'
[root@kakaroto ohai.com]# vi ohai/urls.py
[root@kakaroto ohai.com]# cat ohai/urls.py 
from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ohai.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('ohai_kit.urls', namespace='ohai_kit')),
)
[root@kakaroto ohai.com]# python manage.py migrate
Operations to perform:
  Synchronize unmigrated apps: ohai_kit
  Apply all migrations: admin, contenttypes, easy_thumbnails, auth, sessions
Synchronizing apps without migrations:
  Creating tables...
    Creating table ohai_kit_project
    Creating table ohai_kit_projectset_projects
    Creating table ohai_kit_projectset
    Creating table ohai_kit_workstep
    Creating table ohai_kit_steppicture
    Creating table ohai_kit_stepattachment
    Creating table ohai_kit_stepcheck
    Creating table ohai_kit_jobinstance
    Creating table ohai_kit_workreceipt
  Installing custom SQL...
  Installing indexes...
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  Applying admin.0001_initial... OK
  Applying easy_thumbnails.0001_initial... OK
  Applying easy_thumbnails.0002_thumbnaildimensions... OK
  Applying easy_thumbnails.0003_auto_20140829_0112... OK
  Applying sessions.0001_initial... OK
[root@kakaroto ohai.com]# python manage.py createsuperuser
Username (leave blank to use 'root'): admin
Email address: admin@ohai.com
Password: 
Password (again): 
Superuser created successfully.
[root@kakaroto ohai.com]# python manage.py collectstatic
You have requested to collect static files at the destination
location as specified in your settings:

    /var/ohai.com/static

This will overwrite existing files!
Are you sure you want to do this?

Type 'yes' to continue, or 'no' to cancel: yes

[...]

93 static files copied to '/var/ohai.com/static'.
[root@kakaroto ohai.com]# mkdir media
[root@kakaroto ohai.com]# chown apache:apache -R /var/ohai.com/
[root@kakaroto ohai.com]# vi /etc/httpd/conf.d/ohai.conf 
[root@kakaroto ohai.com]# cat /etc/httpd/conf.d/ohai.conf 
Alias /static/ /var/ohai.com/static/
Alias /media/ /var/ohai.com/media/

<Directory /var/ohai.com/static>
Require all granted
</Directory>

<Directory /var/ohai.com/media>
Require all granted
</Directory>

WSGIScriptAlias / /var/ohai.com/ohai/wsgi.py
WSGIPythonPath /var/ohai.com/

<Directory /var/ohai.com/ohai>
<Files wsgi.py>
Require all granted
</Files>
</Directory>

[root@kakaroto ohai.com]# service httpd restart
Redirecting to /bin/systemctl restart  httpd.service
[root@kakaroto ohai.com]# 
```

Congratulations! Your ohai-kit server is now running!

# Configuring OHAI-Kit 

