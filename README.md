# Bilolok

Bilolok means `Kava` in the local language of a small village on the east, south-east side of Malekula island in Vanuatu.

Bilolok is an open-source application that allows users to browse the hundreds of kava bars in Vanuatu, but focused on Port Vila.
It takes inspiration from Foursquare and is built with FastAPI and Vue.js along with some supporting services such as Tus and Uppy for resumable uploads and Thumbor for image serving.

## Features

- User profiles and user favorites and `chief` titles (like Foursquare mayor).
- Support for check-ins, videos, images and GPS guided navigation to kava bars.
- Kava bar filters, heatmap for popularity, basic search functionality.
- Offline support from PWA's service worker and custom map tile caching.

## Development

The project requires a top-level environment variable file first so copy the template to begin.

```sh
cp .env.template .env
nano .env
```

Modify the values within for your usecase/preferences.
Most values are sensible defaults but a few you will need to provide such as your own vapid key values for push notifications and the MailJet API keys for sending messages. 

Running the code for development currently requires three steps, but it could be a single `docker-compose up` if my local environment within WSL would play nicely with docker and code reloading was working.
So given my personal environment issue I opted for the following.

```sh
# in first tmux window
docker-compose up
# in second tmux window
./export-env.sh
export POSTGRES_SERVER=localhost REDIS_SERVER=localhost
cd backend/app/
poetry shell
./start-reload.sh
# in third tmux window
cd frontend
yarn run dev
```

Some of the complexity above comes from the fact my initial design comes from inspiration from Tiangolo's FastAPI and Postgres starter but after awhile I got fed up with its use of docker as the dev environment and slow rebuilds between code changes so I took the frontend and backend services out of docker.
As a benefit the code base is still docker ready for when I may go back to a full docker environment, one line dev environment start-up and all.

### DB Migrations

Make changes to or add a new model file to the `backend/app/app/models` directory.
If you are adding a new file then import the new models to the `backend/app/app/db/base.py` file so that it can be found by Alembic, and also make our models compatible with `sqlalchemy-continuum` package for easy history tables.
Lastly, run the migration commands.

```sh
alembic migration --autogenerate -m "Your migrtation message"
alembic upgrade head
```

#### OpenGraph Tags

Currently OG tags are a sticking point of my frontend implementation.
Since the frontend Vue.js application is a SPA it means crawlers do not see customized OG tags prior to the app's JavaScript files loading, which crawlers generally ignore anyways.
So each page that users may share would have the same default OG tags which I see as a negative.
Facebook is a main source of potential users so I am catering to their crawler which has some quirks.

Again, cralwers do not load JavaScript so they do not see the dynamic OG tags provided by `vue-meta` so I may remove it altogether but for now it exists and contributes to one of three locations that OG tags are defined.

- frontend/public/index.html
- frontend/public/facebook/index.html
- frontend/src/views/*.vue

To make things worse, Facebook, will not work on https and requires a special nginx check if the incoming request is a facebook bot so we redirect it to a static file available to them via http.

Lastly, the current solution is Nginx detects known bots and forwards them to our OG tag service found in `backend/app/app/og_app` which provides dynamic OG tags based on the URL so when users share our links the social media platforms have the individualized OG tags.

## Contributing

I welcome contributions and discussions for development.

Also, for anyone in Vanuatu, especially students interested in learning software development, I will be happy to work with you and help you contribute your ideas to this project.
