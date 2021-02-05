# LuckyRoll
An application for seeing how lucky your dice rolls in a session of D&amp;D are compared to what is expected

Here's a link to the data https://www.kaggle.com/ucffool/dice-d4-d6-d8-d10-d12-d20-images



## Development

For the Django Backend, you will be able to utilize `docker` and `docker-compose` to get the environment up and running.

```bash
# build the docker image
docker-compose build

# For the next steps you'll need  a secret key for the Django API settings.
# Please contact one of the devs about setting up the `SECRET_KEY`

# make the migrations to serialize python classes to models
docker-compose run -e SECRET_KEY=${SECRET_KEY} app sh -c "python manage.py makemigrations"


# Start the Postgresql DB and django backend server
docker-compose up

# now go to interact with api
localhost:8000

```

### Routes 

```bash
  /api/user/

  /api/campaigns/
  /api/campaigns/<id>/
  
  /api/campaigns/<id>/gamesessions/
  /api/campaigns/<id>/gamesessions/<id>/
  
  /api/dice/
  /api/dice/<id>/
  
  /api/dice/<id>/dicerolls/
  /api/dice/<id>/dicerolls/<id>/
```