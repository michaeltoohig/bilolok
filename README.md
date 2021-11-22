# Bilolok

Bilolok means `Kava` in the local language of a small village on the east, south-east side of Malekula island in Vanuatu.

Bilolok is an open-source application that allows users to browse the hundreds of kava bars in Vanuatu, but focused on Port Vila. It's future may include more social elements similar to the old Foursquare app, but for now will be a catalog of kava bars.

## Roadmap Ideas

[ ] Check-ins
[ ] Nakamal timeline view of check-ins and images in order

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

Ormar for async database access and easy database object to HTTP response mapping.

#### Ormar - Why not SQLAlchemy Core API via encode/databases?

I found using SQLA Core a bit fragile since I had to define SQL queries manually for each CRUD operation and write different SQL queries depending on which joins I wanted and then also manually handle the mapping the SQL result to HTTP response. Although, it provided great flexibility and kept me cognizant of SQL query performance at every step the overhead is more than I need for this project where I planned to use existing tools whereever possible that increase developer productivity. SQLA Core was quickly becoming a hinderance to that stated goal so I did research on `SQLModel` by the developer of `FastAPI` but found their method of combining SQLAlchemy with Pydantic into a single model felt wrong. I believe they abused the validation hooks of Pydantic for features handled well by SQLAlchemy such as to created computed properties. Plus reading further into their docs and github made me feel it was too young for serious use. So I choose to try Ormar and believe their API of how to handle SQLA table definitions and Pydantic validation schemas felt better to me and overall the project is more mature as it has first-class support in all of the above mentioned packages I want to use in this project. 

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