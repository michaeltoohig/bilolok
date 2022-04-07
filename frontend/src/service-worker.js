/* eslint-disable */

// custom service-worker.js

/*
 * You'll need to register this file in your web app and you should
 * disable HTTP caching for this file too.
 * See https://goo.gl/nhQhGp
 *
 */


self.__precacheManifest = [].concat(self.__precacheManifest || []);

// adjust log level for displaying workbox logs
workbox.setConfig({
  debug: true
});

// Set default workbox cache prefix
// workbox.core.setCacheNameDetails({prefix: "bilolok"});

// apply precaching. In the built version, the precacheManifest will
// be imported using importScripts (as is workbox itself) and we can
// precache this. This is all we need for precaching
// workbox.precaching.precacheAndRoute(self.__precacheManifest, {});
workbox.precaching.precacheAndRoute(self.WB_MANIFEST, {});

// Make sure to return a specific response for all navigation requests.
// Since we have a SPA here, this should be index.html always.
// https://stackoverflow.com/questions/49963982/vue-router-history-mode-with-pwa-in-offline-mode
workbox.routing.registerNavigationRoute('/index.html');

// Setup cache strategy for Google Fonts. They consist of two parts, a static one
// coming from fonts.gstatic.com (strategy CacheFirst) and a more ferquently updated on
// from fonts.googleapis.com. Hence, split in two registerroutes
workbox.routing.registerRoute(
  /^https:\/\/fonts\.googleapis\.com/,
  new workbox.strategies.StaleWhileRevalidate({
    cacheName: 'google-fonts-stylesheets',
  }),
);

workbox.routing.registerRoute(
  /^https:\/\/fonts\.gstatic\.com/,
  new workbox.strategies.CacheFirst({
    cacheName: 'google-fonts-webfonts',
    plugins: [
      new workbox.cacheableResponse.Plugin({
        statuses: [0, 200],
      }),
      new workbox.expiration.Plugin({
        maxAgeSeconds: 60 * 60 * 24 * 365,
        maxEntries: 30,
      }),
    ],
  }),
);

workbox.routing.registerRoute(
  /^https:\/\/stackpath\.bootstrapcdn\.com/,
  new workbox.strategies.StaleWhileRevalidate({
    cacheName: 'fontawesome',
  }),
);

const matchTileReqFunction = ({ url, request, e }) => {
  console.log(url, request, e)
  if (url.href.includes('tile.openstreetmap.org')) {
    return true;
  } else {
    return false;
  }
}

// cache tiles; works but fills cache quickly since storage is limited in cache
workbox.routing.registerRoute(
  matchTileReqFunction,
  new workbox.strategies.CacheFirst({
    cacheName: 'tiles',
    plugins: [
      new workbox.cacheableResponse.Plugin({
        statuses: [0, 200],
      }),
      new workbox.expiration.Plugin({
        maxAgeSeconds: 60,
        maxEntries: 100,
      })
    ]
  })
);

// This code listens for the user's confirmation to update the app.
self.addEventListener('message', (e) => {
  console.log(e, e.data)
  if (!e.data) {
    return;
  }

  if (e.data && e.data.type === 'SKIP_WAITING') {
    self.skipWaiting();
  }
});
// self.addEventListener('message', (e) => {
//   console.log('message')
//   if (!e.data) {
//     return;
//   }

//   switch (e.data) {
//     case 'skipWaiting':
//       self.skipWaiting();
//       break;
//     default:
//       // NOOP
//       break;
//   }
// });


let click_open_url;
// Web Push Notification
self.addEventListener('push', (e) => {
  let push_message = e.data.text();

  click_open_url = 'https://google.com';
  const options = {
    body: push_message,
    icon: './img/icon.png',
    image: './img/notification.jpg',
    vibrate: [200, 100, 200, 50, 50, 50, 50],
    tag: 'vibe-test',
  };
  e.waitUntil(
    self.registration.showNotification("My Notification", options)
  );
});

self.addEventListener('notificationclick', (e) => {
  const clickedNotification = e.notification;
  clickedNotification.close();
  if (click_open_url) {
    const promiseChain = clients.openWindow(click_open_url);
    e.waitUntil(promiseChain);
  };
});


// Below is from `zikes-web` found in a issue tracker - more complex than necessary perhaps by using DB
// importScripts('tileCacheDb.js');
// console.log('imported cacheDb')
// const ourDomains = ["localhost:8000"];
// const mapTilesDomain = "tile.openstreetmap.org/";
// const ignoreDomains = ["googleapis", "facebook", "gstatic"];
// function fetchApplicationAsset(event) {
//     if (ourDomains.reduce(function(cum, domain) {
//         return cum || event.request.url.indexOf(domain) != -1;
//     }, false)) {
//         return fetchUserAsset(event);
//     }

//     return caches.match(event.request).then(function(response) {
//         if (response) {
//             return response;
//         }
//         var isMapTilesReq = event.request.url.indexOf(mapTilesDomain) != -1;
//         if (isMapTilesReq) {
          
//             console.log(event.request.url)

//             var re = /\/(\d+)\/(\d+)\/(\d+).vector.pbf/;
//             var matched = event.request.url.match(re);
//             if (matched) {
//                 console.log(matched)
//                 var key = {z:matched[1],x:matched[2],y:matched[3]};
//                 return tileCacheDb.get(key)
//                 .then(function(tileBuffer) {
//                     if (tileBuffer) {
//                         return new Response(tileBuffer);
//                     }
//                     return fetch(event.request)
//                 });
//             }
//         }

//         if (!ignoreDomains.find(function(domain) {return event.request.url.indexOf(domain) != -1})) {
//             console.log("Unmatched URL '" + event.request.url+"'");
//         }
//         return fetch(event.request);
//     });
// }

// self.addEventListener('fetch', function(event) {
//     console.log('fetch')
//     // event.respondWith(fetchApplicationAsset(event));
// });

// Listen to Push
// self.addEventListener('push', (e) => {
//   let data;
//   if (e.data) {
//     data = e.data.json();
//   }

//   const options = {
//     body: data.body,
//     icon: '/img/icons/android-chrome-192x192.png',
//     image: '/img/autumn-forest.png',
//     vibrate: [300, 200, 300],
//     badge: '/img/icons/plint-badge-96x96.png',
//   };

//   e.waitUntil(self.registration.showNotification(data.title, options));
// });


// Below is an example I found on Github to cache map tiles

// this.addEventListener('install', function (event) {
//   console.log('Installing Service Worker');
//   event.waitUntil(this.skipWaiting());
// });

// this.addEventListener('activate', function (event) {
//   event.waitUntil(this.clients.claim());
// });

// self.addEventListener('fetch', (event) => {
//   var url = event.request.url;
//   console.log('fetch to', url)
  
//   if(url.startsWith('https://') && (url.includes('.tile.openstreetmap.org'))) {
//     console.log('tile found')
//     event.respondWith(
//       caches.match(event.request).then(function(resp) {
//         return resp || fetch(event.request).then(function(response) {
//           var cacheResponse = response.clone();
//           caches.open('tiles').then(function(cache) {
//             cache.put(event.request, cacheResponse);
//           });
//           return response;
//         });
//       })
//     );
//   }
// });
