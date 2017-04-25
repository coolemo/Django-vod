# Django-vod
Use Django to create a vod(video on demand) manage system
Based on Bootstrap3

# FAQ
1. Centos7 no models named '__sqlite3'
> yum install sqlite-devel
rebuil python and install

# Useful 3rd-party app
1. Django Crispy Forms \
`pip install django-crispy-forms`
>settings.py
```
INSTALLED_APPS = {
...
'crispy_forms',
...
}

2. Django with Nginx-gunicorn
```
pip install gunicorn
gunicorn hello.wsgi:application --bind example.com:8001 #test gunicorn

#edite file gunicorn_start, django.conf(for nginx)
./gunicorn_start
nginx -s reload
```

#Crispy Form Tags Settings
CRISPY_TEMPLATE_PACK = 'bootstrap3'
```
>*.html
```
{% load crispy_forms_tags %}

<form method='POST' action='' >{%csrf_token%}
{{form|crispy}}
<input class='btn btn-primary' type='submit' value='Sign Up'/>
</form>
```
2. Django Registration Redux
https://django-registration-redux.readthedocs.io/en/latest/quickstart.html

`pip install django-registration-redux`
>settings.py
```
INSTALLED_APPS = {
...
'django.contrib.auth',
'django.contrib.sites',
'crispy_forms', 
...
}
#Django Registration Redux Settings
ACCOUNT_ACTIVATION_DAYS = 7 #days email is availd
REGISTRATION_AUTO_LOGIN = True
LOGIN_REDIRECT_URL='/'
```
>url.py
```
url(r'^accounts/',include('registration.backends.default.urls')),
```
>templets
>need to copy templates from official site
