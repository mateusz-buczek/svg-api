Make sure you've got: 
- Docker installed 
- repository copied to your local machine 
- `.env` file created in root directory (namely copy of `.env.example` file placed next to it). It also allows to customize some properties of outputted SVG. 

first run to build project locally: 

```
docker-compose up --build 
```

next time: 

```
docker-compose up 
``` 
is enough. 

To create superuser: 

- enter working container
- ```
    docker-compose exec web sh
    ``` 
- execute command
- ```
    python manage.py createsuperuser
    ``` 
- and follow instructions


Browsable API is available at 
```
localhost:8000/api-info/
```
or other port if you specify it for `web` container in `docker-compose.yml`

You can check how it works with swagger GUI, or f.e. curl requests that it generates

Models are also available in regular django-admin
```
localhost:8000/admin/
```
