## Basic Deployment

+ heroku login

+ heroku git:clone -a <app_name>

+ git add .

+ git commit -am "<commit_name>"

+ git push heroku master

In future if there were any changes or edits made on the app,we can follow the same procedure,but starting from

+ heroku git:clone -a <app_name>

+ git add .

+ git commit -am "<commit_name>"

+ git push heroku master

Once this is done,type the following commands to activate your database and inorder to run the app,follow this commands step by step,so first you need to create your superuser,so that you can use your database present at the heroku server,so run the following commands step by step,once all the commands are successfully executed run the last command which is `heroku run`

  
```
heroku run python manage.py makemigrations

heroku run python manage.py makemigrate

heroku run python manage.py createsuperuser

heroku run
```