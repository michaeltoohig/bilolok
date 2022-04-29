# Open Graph App

This directory contains an application that returns server-side rendered pages for crawlers/bots; essentially prerender.

The frontend application is currently a Vue2 SPA that has statically defined OG tags in the `public/index.html` file. Since remote services that view our application often do not load JavaScript they only see the default Bilolok OG tags. This is not ideal for sharing on platforms such as Facebook since each resource shared will display the same default values when we would rather have customized OG tags for those sharing specific resources.

Facebook is an especially difficult issue since their crawler does not handle https and will not follow redirects which we use to push actual users from http to https.

## Consideration

There are three sources of truth for Open Graph tags at the moment.

- This app
- The static `public/index.html` 
- The dynamically set `vue-meta` in each frontend router view

This is not ideal and should be consolidated in the future into a single SSR rendered app or SSR Vue app that uses this application or `vue-meta` to configure the OG tags and would mean there is only one source of truth to maintain.

### Future Design Idea

Configure webserver to host this app on primary domain and serve the built `dist/` directory. It may couple the backend and frontend too much but would be away to have the og tags configured correctly in one place then make in-app sharing easier since we would not need to set share title and description in the frontend but could reference the OG tags from the JavaScript.
