
# WEATHER SPOTIFY ##
## Music based on the weather and the most popular news in your country.

This application allows you to check actuall weather and give a random playlist on spotify based on weather.
You also check the most popular news in your country.\
For more content you can register to the newsletter to get weakly interesting informations.

### Technology that I used:
- Python (Django)
- HTML & BOOTSTRAP & CSS
- PostgreSQL
- Docker
- APIs:
    - Spotify API
    - Openweather API
    - Geolocation API 
    - NEWS API 



## Demo

- [VIDEO DEMO ON YOUTUBE](https://youtu.be/gVOYeAU3Fpo)

<img src="/images/1.png"/>
<img src="/images/2.png"/>
<img src="/images/3.png"/>
<img src="/images/4.png"/>


## Documentation

1. Clone the repository

```bash
git clone <link>
```

2. Install requirements

```bash
pip intall -r requirements.txt
```

3. .env

Inside direction "weathermusic" where settings.py is located you need to create file called ".env" and paste this:

```bash
SECRET_KEY=<DJANGO SECRET KEY>
EMAIL=<YOUR GMAIL EMAIL ADDRESS>
PASSWORD=<YOUR GMAIL PASSWORD>
CLIENT_ID=<TO YOUR SPOTIFY ACCOUNT>
CLIENT_SECRET=<TO YOUR SPOTIFY ACCOUNT>
AUTH_URL=https://accounts.spotify.com/api/token
WEATHER_KEY=<API KEY FROM OPENWEATHERMAP>
GEOLOCATION_KEY=<API KEY FROM IPGEOLOCATION>
NEWS_KEY=<API KEY FROM NEWSAPI>
```

4. Make migrations

```bash
py manage.py makemigrations
```

```bash
py manage.py migrate
```

5. Create superuser

```bash
py manage.py createsuperuser
```


### Newsletter:

To send newsletter you need to be registered on admin account.\
Then go to url /newsletter/send and you can write an email.

## License

[MIT](https://choosealicense.com/licenses/mit/)

