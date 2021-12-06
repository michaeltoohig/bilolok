# Bilolok

Bilolok means `Kava` in the local language of a small village on the east, south-east side of Malekula island in Vanuatu.

Bilolok is an open-source application that allows users to browse the hundreds of kava bars in Vanuatu, but focused on Port Vila. It's future may include more social elements similar to the old Foursquare app, but for now will be a catalog of kava bars.

## Version 1 Roadmap

 - [x] Profile page
   - [x] User Avatar
   - [x] User Timeline
 - [ ] Search page
   - [ ] Search filters
 - [ ] Nakamal page
   - [ ] Nakamal Timeline
   - [x] Check-in details
   - [x] Check-in message
   - [x] Chief
 - [ ] Home page
   - [x] Big eye-catching link to map view
   - [ ] Change 'about', 'recent activity' as dialogs or bottom sheets to map

 - [ ] SQLAlchemy-Continuum integration
   - [ ] Admin view to un-do unwanted edits
  
The following packages are not officially supporting SQLA 1.4 yet but have user
made forks that are awaiting review to be officially integrated to support the
new SQLA async version. I'm using those user forks at the moment and will need
to return the offical project code bases.

 - [ ] SQLAlchemy 1.4 migration
   - [ ] FastAPI-Users
   - [ ] FastAPI-CRUDRouter
   - [ ] SQLAlchemy-Continuum


## Future Roadmap Ideas

Below are some ideas for the future of this project.

For version 2 and beyond we can build upon this foundation such as the following ideas:

  - Have user that checks-in to nakamal most regularly be able to have special privileges to modify the profile page of the nakamal.
    - Set primary profile picture
    - Set a pinned message on profile
    - Badge on their profile 
  - Add badges for users and include it in their profile timeline
    - Badges for first image uploaded, first checkin, checking in X times, etc.
  - Interactive charts for popularity of areas, user history, other visuals.

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
SQLAlchemy
FastAPI Users
FastAPI CRUDrouter
FastAPI paginate
SQLAlchemy-Continuum

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