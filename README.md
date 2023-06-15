# django-E-commerce

Simulation of a computer component online shop 

Features used in this project :
  * Add items in your basket
  * Add order 
  * Manage your addresses and personal information
  * Rate and add comment to purchased products 
  * Used Redis as cache backend
  * Used Session Framework
  * update user basket after login or register via signals
  * Send a Welcome Email using Celey


How to run the project?

1:
  install requirements.txt with command : pip install -r requirements.txt
  
2:
  install Redis and make sure it's active and running
  
3:
  Create a file with name local_setting.py beside of setting.py and add the following code:
  
  SECRET_KEY = 'YOUR SECRET KEY'
  DEBUG = True          # if you want to use this project in production change the value to False.
  EMAIL = "YOUR EMAIL ADDRESS"
  APP_PASSWORD = "YOUR APP PASSWORD"
  ALLOWED_HOSTS = ['*']         # if you want to use this project in production replace your domain in that list.
  
4: 
  Run python manage.py migrate
  Run python manage.py createsuperuser

5:
  run python manage.py runserver

6:
  celery -A E_commerce worker -Q Eemail -l INFO --logfile=/var/log/celery/celery_eco.log    # if you don't run this, emails will not send to the users.

  
ENJOY THE PROJECT :)
    
