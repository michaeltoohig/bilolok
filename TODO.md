This file contains a combination of TODO items, wild ideas, project roadmap plans and past completions as I like to see what I have done and keep it in context of what I want to to do yet.

> Forgive the the messy state of this file.

## Current Roadmap

- [ ] Nakamal events schedule
- [ ] Upgrade FastAPI to latest version; handle issues regarding SQLAlchemy that result (ie. connections to db not closing after requests)
- [ ] Create bottom nav UI for important actions (ie. search)

## Ideas

- [ ] Update UI to focus more on map by making nakamals pages, home page, etc open as bottom sheets or something that feels as if the map view is the only view
  - [ ] Maybe bottom sheet for nakamals as a "peak" before opening it further
- [ ] UI update to show delayed POST requests until network returns
- [ ] Show your checkin count for the month on nakamal profile
  - [ ] Show other history of checkins

## TODOs

- [ ] Add cache to `loadRecent` actions
  - [ ] Better yet create timeline API endpoint

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
- [ ] Chief stored in DB
  - [ ] notification when chief position is lost
  - [ ] user view can show number of chief titles held by user

- [x] Fix arq to use async db session
- [ ] Stop loading all nakamals each time map view is mounted
- [ ] Add endpoint param or other cue to flyToSelected on map view mounted; otherwise map should still be on last point and not necessary to flyToSelected interfere with UX
- [ ] featured nakamal
  - [x] API endpoints
  - [x] Home page section
    - [ ] when chief is added to nakamal table then add chief to featured nakamal card
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
  - [x] Facebook issue with images having "incorrect content type"
    - [x] Issue was related to https not being supported by facebook crawler
    - [x] Resolve http solution for video subdomain
      - [x] Issue above is images are not minimum 600px for FB

- [x] Allow users to set featured nakamal

- [ ] Check SW video/image caches
  - [ ] Looks like we have to resolve cross-origin assets

- [x] Translations
  - [x] Store preference same as dark/light mode

- [ ] Refactor frontend components
  - [x] Move map components to map directory
  - [ ] break out components related to map edit/create to a subdirector
  - [x] Create components for App.vue

- [x] Handle request timeout gracefully
- [ ] Remove repetitive "Not Allowed" notifications in favor of single "Request Error" notification using the response.data.detail

- [ ] Vue-tour ?

- [ ] Chief of Nakamal
  - [ ] List
  - [ ] isChief special card styling
  - [ ] event when chief title is changed
    - [ ] user notification
    - [ ] news feed card
  - [ ] requirements
    - [x] daily task to calculate new chiefs (expire chiefs too)
    - [x] post check-in task to calculate if new chief title is awarded
      - [ ] ? how to alert user they have become chief after task completes ?
        - [ ] poll endpoint for task completion. notify result.
    - [x] chief history table (using already versioned nakamal table)
    - [x] chief user_id column on nakamal

Chief todos
  - [x] Add normalizeRelation and update resolveRelation helpers for store
    - [x] Add user's chief of nakamal list to profile
      - [x] Add call to chiefs api to fetch complete list of chief titles in case nakamals are not all loaded already
    - [ ] Add chiefs to home page or user list
    - [ ] Add chief to nakamal popup
    - [x] Remove chief calculation from nakamal profile use given chief value from API

- [ ] Favourite nakamals on home page
- [x] Easy to access search (autocomplete) on home page

- [ ] Your checkin count on nakamal profile (compare against chief)

- [ ] New nakamal view tab for basic map with option to find your distance from etc.
  - [ ] Big obvious "View on full map" link
  - [ ] Pop up with name, area, perhaps name of nearby nakamals to help users find its general area. Maybe map is always centered on nakamal.

- [ ] Admin features
  - [ ] Review status of push notifications
  - [ ] User activity (login failures etc.)
  - [ ] Nakamal modifications / activity


### Version 3.1  (version means nothing lol)

TODO
1. update get all route, trip routes, etc to return nakamal schema with profile
2. work on nakamal profile points below
3. work on frontend
4. cache nakamal and update trip endpoints, etc to return UUID not full object

- [ ] Can we google translate for more languages? Why not auto translate to major languages?

- [x] Add easy access search for kava bar from home page
- [ ] Map view of nakamal on nakamal profile page
- [ ] Use vue-router sub-routes for nakamal profile tabs
- [x] Nakamal light color badges for avatars
  - [ ] make into component - make DRY

!! - [ ] Stop returning full objects and instead return IDs then let client load object

- [x] Add explicit profile picture selection for nakamals
  - [x] Add api endpoints to update the profile picture ID
    - [x] Add logic to restrict who may update profile id
    - [x] Add logic to handle when profile picture is removed
    - [x] Add logic to restrict profile ID to image of nakamal
    - [x] Make sure all occurances of `nakamal` API responses have up-to-date profile
    - [x] Set all most recent images for each nakamal as the profile picture for first release
    - [x] Alembic migration must set initial profile pictures
    - [x] Add logic to set first image of a nakamal as profile when added
    - [x] Add UI to remove and set profile picture on frontend
  - [x] Update logic to display profile picture instead of first image across frontend
  - [x] add logic to delete profile when image is deleted (not a cascade)

  To make profile pictures possible; avoid recursion in loading related objects nakamal -> profile -> nakamal -> ... we need to change the way we handle vuex store and fetching objects.
  My plan at the moment is to use the local cache I've introduced for more objects and wrap vuex actions with cache checks to transparently return the requested object when a component's `mounted` call would otherwise fetch the object.
  Below are the steps I see thus far to acheive this goal and lay the foundation for the remaining steps for nakamal profile pictures
  - [ ] Find components (mainly view components) that use a `${resource}/find` getter from vuex as a local computed property where a local variable would be better since these properties are tied to the view and not changing.
  - [ ] Update vuex modules to include a "fetch" action that checks a local cache before making a remote request
    - [ ] when fetching many perhaps it is always a shallow fetch then at the component level the component fetches related objects which again would possibly hit the vuex cache behind the scenes.
  Steps:
    1. make "fetch" actions that include a cache check
    2. update view components to use fetch on mounted lifecycle hook then store the result for the route in local variable
    3. components would use the ID from the local object to fetch (or get from cache) related objects instead of transparently merging related objects in the vuex store
      3a. Cache must use a volatile storage so hard refreshes can override (i think that is a good idea right now; I like the idea of overridinge cache or clearing cache being available to users)

- [ ] Related nakamals or nearby nakamals selection from nakamal profile

- [ ] Notification and email for change of chief status
- [ ] Handle chief in separate table just like profile picture so history of chiefs can be retained