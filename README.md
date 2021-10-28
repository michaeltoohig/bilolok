# Bilolok

Bilolok means `Kava` in the local language of a small village on the east, south-east side of Malekula island in Vanuatu.

Bilolok is an open-source application that allows users to browse the hundreds of kava bars in Vanuatu, but focused on Port Vila. It's future may include more social elements similar to the old Foursquare app, but for now will be a catalog of kava bars.

## Roadmap Ideas

Below are some ideas for the future of this project.

 - Have user that visits nakamal most regularly able to have special privileges to modify the profile page of the nakamal.
   - Set primary profile picture
   - Set a pinned message on profile
   - Badge on their profile 

## Development

I welcome contributions and discussions for development. Below is some explanations of the current architecture and plans for future development.

Also, for anyone in Vanuatu, especially students interested in learning software development, I will be happy to work with you and help you contribute your ideas to this project.

### Backend

Backend API requires the environment variables quite a few environment variables to run. Copy the environment template file then fill it with your local values.

```
cp .env.template .env
nano .env
```

TODO describe initial setup further

TODO document backend design ideas and packages used.

FastAPI
FastAPI Users
FastAPI CRUDrouter
FastAPI paginate

SQLAlchemy-Continuum

Will have to use ``databases`` sqlalchemy async framework

One thing I need to figure out is the combined use of both SQLAlchemy declartively defined models used by alembic and the use of the SQLAlchemy core table definitions used by the databases package and CRUDRouter. You can see this in `app.core.db.base.py` and `app.models.__init__.py`. I prefer to move towards exclusively using the SQLAlchemy core and prepare to migrate to SQLAlchemy 1.3 > 1.4 > 2.0 eventually. 

### Frontend

TODO document frontend design ideas and packages used.

Vue
Vuex
Vue-Router
Vuetify
Axios

### Image Handling

#### Tus

Resumable uploads server using uppy on frontend

#### Thumbor

Image CDN and to add watermark to images, etc.