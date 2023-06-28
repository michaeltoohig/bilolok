# Roadmap

Current project codebase is far behind on updates.
This mostly falls back to development being dependent on SQLAlchemy 1.3 and it was undergoing major changes towards version 2.0 while FastAPI was also going through growing pains as it was young when this project started too.

In the beginning of the project I ran into issues with Docker for Windows with WSL 1 so I didn't use Docker much but in past years I have other projects that work well with Docker with WSL 2 so I also want to migrate the codebase to Docker for easier development startup and deployment.

- [ ] Update dev docker config with explicit envvars rather than implicit envfile
- [x] Makefile for easy dev, setup, deploy, etc.
- [ ] Update deployment scripts to use new production docker-compose.yml

- [x] Frontend docker for development
- [ ] Update Python version; 3.8 is getting a tad old
- [ ] Update SQLAlchemy, requires big update to many packages; see below

## Notes to upgrade Python and Fastapi and SQLAlchemy

Below are current package versions and my notes based on considerations I should take to upgrade to the latest version of each of the following packages.

fastapi > 0.73
 - 0.95.1 fixes bug related to `Annotated` in path
 - 0.95.0 recommends and now supports use of `Annotated`
 - 0.93.0 `startup` and `shutdown` event hooks are replaced with single `lifespan` hook
 - 0.91.0 technically fixes past middleware behaviour; may introduce bug due to my existing middleware kludges 
 - 0.89.0 `response_model` is replaced by function return type annotation (reduces boilerplate)
 - 0.86.0 supports py3.11
 - 0.81.0 allow middleware to raise `HTTPException`; may be useful for my existing middlewares
 - 0.78.0 allows omitting `default=...` in parameter declarations; can simplify parameter declarations
 - 0.74.0 dependencies with `yield` can now try/catch `HTTPException`; however I found this release to cause errors with `asyncpg` in the past; see my demo project for work around
fastapi-mail > 0.4.1
 - 1.2.0 changes html field to body
   - breaks old TLS related config vars
 - 1.0.5/6 upgrades fastapi to 0.75.0 and httpx
fastapi-crudrouter > currently some git-hash
 - 3.9.x supports async SQLAlchemy**
 - 3.8.6 supports py3.11
 - 3.8.5 supports py3.10
fastapi-users > 9.2.5
 - will require checking docs as many breaking changes
 - 10.4.0 supports SQLAlchemy 2.0; pin `fastapi-users-db-sqlalchemy<5.0.0` for SQLA 1.4
 - 10.3.0 changes JWT claim `user_id` changed to standard `sub`
 - 10.2.x adds new `on_after_login` hook
 - 10.1.2 returns 204 on successful login
 - 10.1.0 adds new hooks `on_before_delete` and `on_after_delete`
 - 10.0.7 replaces `aioredis` package with `redis` as main redis package now supports async
 - 10.0.0 breaks how user is handled; now returns ORM object instead of Pydantic object; migration path exists in docs
   - see: https://fastapi-users.github.io/fastapi-users/10.0/migration/9x_to_10x/
   - breaks SQLA 1.4; supports SQLA 2.0 ***
 - 9.3.x allows newer/better encryption algos; may require alembic migration to support longer `password_hash` string in users table
sqlalchemy-continuum > idk
 - has branch to support SQLA 2.0 but not quite ready see: https://github.com/kvesteri/sqlalchemy-continuum/issues/326
 - does support SQLA 1.4 so perhaps I can stop at this SQLA version until 2.0 is supported... may not be possile with our dependency requirements

The happy path to migrate dependencies looks slim to nil. Each package has different FastAPI versions dependencies at different times with support for SQLAlchemy 1.4 or 2.0.
Not sure from just reading changelogs what exact upgrade steps I could take to migrate with the least difficulty but this is a personal project and I don't think I would mind just throwing everything to latest versions and working it out.

## Notes to upgrade frontend

Vue should be upgraded to Vue3 and Vite as soon as possible for quicker development and in my experience much better build sizes.
Vue3 with Leaflet will be a difficulty as last I checked a year or 2 ago there was no working replacement for Vue-Leaflet and Vue3-Leaflet was lacking.
We can double check this again.
The largest hurdle to upgrading to Vue3 in the past was Veutify was taking *forever* to migrate to Vue3 but they may be done by now.

> https://vuetifyjs.com/en/getting-started/installation/
> It appears they are still in development???

Either way I'll support the old API and update the backend first then look at the frontend.