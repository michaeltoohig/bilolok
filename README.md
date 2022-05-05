# Bilolok

Bilolok means `Kava` in the local language of a small village on the east, south-east side of Malekula island in Vanuatu.

Bilolok is an open-source application that allows users to browse the hundreds of kava bars in Vanuatu, but focused on Port Vila. It's future may include more social elements similar to the old Foursquare app, but for now will be a catalog of kava bars.


## Version 1 Roadmap

 - [x] Profile page
   - [x] User Avatar
   - [x] Custom Avatar
   - [x] User Timeline
 - [x] Search filters
   - [x] Search filters on map
   - [x] Remove redundant search page
 - [x] Nakamal page
   - [x] Nakamal Timeline
   - [x] Check-in details
   - [x] Check-in message
   - [x] Chief
   - [x] Resources (wasemaot, tusker, billiard table, etc)
   - [x] Area (Freswota, Namburu, Nambatu, etc)
   - [x] Kava Source (Malekula, Santo, etc)
 - [ ] Home page
   - [x] Big eye-catching link to map view
   - [ ] Change 'about', 'recent activity' as dialogs or bottom sheets to map
 - [x] User Auth Features
   - [x] Resend email verification link
   - [x] Forgot password process
   - [x] Add auth check to open auth modal for existing features

 - [x] Set map bounds after each filter is applied
 - [x] Archive / Log tables for important user-editable tables
   - [x] Nakamal table

The following were recommended additions

 - [x] Add kava source to nakamal / include in search filters
 - [x] Support multiple names of nakamal
 - [x] Add nakamal area / include in search filters
  
The following packages are not officially supporting SQLA 1.4 yet but have user
made forks that are awaiting review to be officially integrated to support the
new SQLA async version. I'm using those user forks at the moment and will need
to return the offical project code bases.

 - [ ] SQLAlchemy 1.4 migration
   - [ ] FastAPI-Users
   - [ ] FastAPI-CRUDRouter
   - [ ] SQLAlchemy-Continuum


### Version 1.1 Roadmap

I will focus on features related to a better offline user experience the goal of 
version 1.1. Unlike version 2 which brings features to the users' that they interact
with and will see, these features should blend in smoothly with the current app and
mostly "Just Work" behind the scenes.

- [x] App loads while offline
  - [x] prefetch nakamal areas, resources, kava sources on app load
  - [ ] prefetch add nakamal map marker
- [ ] Allow for POST requests while offline
  - [x] nakamal
  - [x] checkin
  - [ ] resources, areas, kava sources are not available to POST offline
         due to them being dependents of creating a nakamal and therefore
         I won't have an ID available to create the nakamal while offline
         so why bother creating these resources while offline also?
         So add a note that these resources may not be created while offline.
  - [ ] Add UI element to display queued POST requests while offline - connect to IndexedDB with dexie maybe?
  - [ ] Add notification that POST request is queued instead of submitted.
- [x] Try using NetworkFirst for endpoints such as GET checkins and other dynamic resources
        Currently, after returning to network a queued POST /checkins is not visible to user until
        the second full page reload to get the new resource into cache on first refresh and into
        the UI on the second reload.
  - [x] NetworkFirst /nakamals
  - [x] NetworkFirst /checkins
- [x] Better Geolocation API
  - [x] Improve accuracy
  - [x] Distinct marker for user's location
  - [x] UI element to show fetching location in progress
- [x] Show nearby nakamals to user if user location icon is selected
  - [x] show distance
- [x] Show distance if location available for NakamalMapPopup

 
## Future Roadmap Ideas

Below are some ideas for the future of this project.

For version 2 and beyond we can build upon this foundation such as the following ideas:

  - Have user that checks-in to nakamal most regularly (aka the chief of the kava bar) be able to have special privileges to modify the profile page of the nakamal.
    - Set primary profile picture
    - Set a pinned message on profile of nakamal
    - Badge on user profile 
  - Add badges for users and include it in their profile timeline
    - Badges for first image uploaded, first checkin, checking in X times, etc.
  - Interactive charts for popularity of areas, user history, other visuals.
  - Add chart to nakamals with multiple windows that shows most popular windows
    - Use check-in and regex `@w[ie](n?)do(w?)(\s?)#(\s?)(\d)+` to find which windows are mentioned
    - Use another regex with special character to mark the window as bad
    - chart shows windows with positve and negative and no reviews then

- [ ] More Logging
  - [x] Use Loguru / replace default logger
  - [x] Add middleware to log requests (timeit?)
    - [x] Log to file
  - [x] Log request-id
- [ ] Sentry
  - [x] backend
    - [x] include context such as user id and request id
  - [x] frontend
    - [x] generate request on frontend
    - [ ] include context such as user id and request id
  - [x] look into sentry feature to join frontend and backend errors into one continuous timeline
- [ ] Refresh Access Token
  - [ ] Blacklist tokens
  - [ ] Add iat to JWT
- [ ] Update emails to more professional standard (maybe use mjml)
- [x] On map zoomed out show areas instead of markers
- [ ] User actions table
  - [ ] Add `last_seen` or similar to users table
- [ ] Push Notifications - Experimental setup
  - [x] Allow users to subscribe / unsubscribe
  - [x] Remove subscriptions for device when user logs out
  - [ ] Handle `pushsubscriptionchange` event - seems impossible cannot trigger manually
- [x] Heatmap layer
  - [x] Show heatmap for all users
  - [x] Filter heatmap to only user's checkins
  - [x] Filter heatmap by date ranges
- [ ] Compass mode
  - [x] Show heading to selected nakamal
  - [x] Follow user location marker while watching user location
  - [x] Draw Polyline of user trip
  - [x] Show live distance and trip traveled distances
  - [x] Save the trip for showing later
  - [x] Auto submit when proximity threshold reached
  - [ ] Fix edge cases and odd behavior
    - [ ] Compass failing to save after repeated uses without reloading page
- [x] User profile upgrade
  - [x] show favourite nakamals (maybe ranked top 3) by check-in count
  - [x] personalized user profile picture
  - [x] add trips to profile timeline
- [ ] Share API
  - [x] Set default Open Graph tags 
    - [ ] Fix facebook bot handling of OG tags / only works for root domain sharing
  - [x] Share nakamal
  - [x] Share user
- [x] Automate backup with ansible
  - [x] database
  - [x] photos
- [x] Fix browser quota limit error - handle by clearing cache and starting again?
- [x] Add nakamal created_at and updated_at columns
  - [x] User edit history of nakamals
- [ ] Handle possibly dead nakamals by looking for nakamals without recent updates or recent check-ins. A `confirmed_at` value or table with user and result of confirmation visit?
- [x] User view for public - rank users or show their badges and order by different criteria (last check-in, most this week/month, etc)
- [ ] User login history and track IP and other details to help prepare against bad actors
- [ ] Current user chat (websockets or something) KISS so no history or logging
  - [ ] Alerts users to new messages or @user messages
  - [ ] Must be able to listen to incoming messages in background while user has joined chat for the day or something like this? Or it becomes a always running chat app at the same time???
  - [ ] Current active users list on frontend? - may be best if implemented when new auth token is generated since if we have refresh tokens we can set the auth tokens to a short lifespan - or when if chat is an available feature then use the websocket to set a more precise value based on last message sent or other event
- [x] Fix right side bars not collapsing on desktop
- [ ] Cheif stored in DB
  - [ ] notification when cheif position is lost
  - [ ] user view can show number of cheif titles held by user

- [x] Fix arq to use async db session
- [ ] Stop loading all nakamals each time map view is mounted
- [ ] Add endpoint param or other cue to flyToSelected on map view mounted; otherwise map should still be on last point and not necessary to flyToSelected interfere with UX
- [ ] featured nakamal
  - [x] API endpoints
  - [x] Home page section
    - [ ] when cheif is added to nakamal table then add cheif to featured nakamal card
  - [ ] Map special marker
- [ ] nakamal reviews
  - [ ] 0 - 100 rating scale / calculated to 5 star rating system

- [x] Handle DOM Exception Quota Exceeded
- [x] Fine-tune SW api endpoint caches
- [x] Make login easier. Trim for any erroneous spaces on input fields


### Verison 3

I would have to say adding video and some other features I'm working on is pushing towards a more social platform and less data driven platform. It would then be appropriate to label the following features as the roadmap to version 3.

- [x] User videos
  - [x] Refactor local media data storage 
  - [x] Show appropriate buttons based on state of video
  - [x] tear down everything when modal is closed
  - [x] support vertical and horizontal video formats / or only 1:1
  - [x] backend saving / storing / processing of videos TBD
    - [x] Save file with PENDING
    - [x] Run task from tus-hook
    - [x] test task
    - [x] watermark
  - [x] debug static video endpoint / nginx endpoint for production
  - [x] endpoints for videos
  - [x] frontend timeline card for videos
  - [x] home page recent videos
  - [x] sw cache for videos
  - [x] delete videos UI
    - [ ] delete video/cover and original on backend
  - [x] restrict upload to verified users only
  - [ ] allow upload video
    - [x] handle video without sound
    - [ ] limit to specific duration
    - [x] limit to specific max size
    - [ ] limit to square video only or process in task to sqaure video

- [x] Shareable pages
  - [x] Check-ins
  - [x] Images
  - [x] Trips
  - [x] Videos
- [x] SSR OG tags
  - [ ] Facebook issue with images having "incorrect content type"

- [ ] Check SW video/image caches
  - [ ] Looks like we have to resolve cross-origin assets

- [ ] Translations
  - [x] Store preference same as dark/light mode

- [ ] Refactor frontend components
  - [ ] Move map components to map directory
  - [ ] break out components related to map edit/create to a subdirectory

- [ ] Vue-tour ?

- [ ] Chief of Nakamal
  - [ ] List
  - [ ] isCheif special card styling
  - [ ] event when cheif title is changed
    - [ ] user notification
    - [ ] news feed card

- [ ] Admin features
  - [ ] Review status of push notifications
  - [ ] User activity (login failures etc.)
  - [ ] Nakamal modifications / activity


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

#### OpenGraph tags

Currently OG tags are a mess. The OG tags are defined in multiple areas

- public/index.html
- public/facebook/index.html
- views/*.vue

Since the app is a SPA most crawlers or other websites checking for OG tags will only see the static tags set in index.html. The app views use `vue-meta` to update the OG tags and page title dynamically but again the remote websites do not load the js to get the updated values.

To make things worse, Facebook, will not work on https and requires a special nginx check if the incoming request is a facebook bot then we redirect to a static file available to them via http.

I believe going forward the proper solution will be an nginx check for any bots and redirects them to a flask app that can quickly spit out an empty html page with OG tags properly set. Otherwise, normal users will be correctly passed to the SPA and loaded the expected content. In this static page we should include a link to the https page incase our bot check catches a real user.

### Image Handling

#### Tus

Resumable uploads server using uppy on frontend

#### Thumbor

Image CDN and to add watermark to images, etc.
