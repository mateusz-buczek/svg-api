Make sure you've got: 
- Docker Compose installed (https://docs.docker.com/compose/install/)
- repository copied to your local machine 
- `.env` file created in root directory (namely copy of `.env.example` file placed next to it). 
  It also allows to customize some properties of outputted SVG. 
  It is not copied automatically to avoid loosing your settings when rebuilding. 

Before the very first run one must build project locally: 

```
docker-compose build 
```

then: 

```
docker-compose up 
``` 
Next time up command is enough. 

In case of problems you can start fresh with:
```
docker-compose down 
```
and repeat from beginning.  
  

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

Models are also available in regular django-admin. Uploaded data is stored in DB and can be re-rendered to svg if needed
```
localhost:8000/admin/
```
