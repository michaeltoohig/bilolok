/* eslint-disable */

import Dexie from 'dexie';
// import {
//   setCacheNameDetails,
// } from 'workbox-core';
import {
  registerRoute,
  NavigationRoute,
} from 'workbox-routing';
import {
  NetworkOnly,
  NetworkFirst,
  StaleWhileRevalidate,
  CacheFirst,
  Strategy,
} from 'workbox-strategies';
import {
  createHandlerBoundToURL,
  PrecacheFallbackPlugin,
  precacheAndRoute,
} from 'workbox-precaching';
import { WorkboxError } from 'workbox-core/_private/WorkboxError.js';
// Used for filtering matches based on status code, header, or both
import { CacheableResponsePlugin } from 'workbox-cacheable-response';
// Used to limit entries in cache, remove entries after a certain period of time
import { ExpirationPlugin } from 'workbox-expiration';
import { timeout } from 'workbox-core/_private/timeout.js';

// Use with precache injection
precacheAndRoute(self.__WB_MANIFEST);

addEventListener('message', (event) => {
  console.log(event, event.data, event.data.type);
  if (!event.data) return;
  if (event.data && event.data.type === 'SKIP_WAITING') {
    self.skipWaiting();
  }
});

/* Map Tile Caching */

const tileValidSeconds = 60 * 60 * 24;

// Setup the cache DB
const db = new Dexie('map-tiles-cache');
db.version(2).stores({
  tiles: '++id,&coords,accessed'
});

const getTile = async (url) => {
  let key = urlToCacheKey(url);
  return db.tiles.where('coords').equals(key).first();
};

const saveTile = async ({ url, tile }) => {
  let key = urlToCacheKey(url)
  let cached;
  cached = await db.tiles.where('coords').equals(key).first();
  if (cached) {
    db.tiles.where('coords').equals(key).modify(t => {
      t.accessed = new Date();
      t.tile = tile;
    })
  }
  else {
    db.tiles.put({ coords: key, accessed: new Date(), tile: tile });
  }
};

const updateTileAccessedDate = async (key) => {
  db.tiles.where('coords').equals(key).modify(tile => {
    tile.accessed = new Date();
  });
};

// TODO use perhaps periodically to clear unused tiles after extended periods
const removeExpiredTiles = async () => {
  let threshold = new Date();
  threshold = threshold.setTime(threshold.getTime() - (1000 * tileValidSeconds));
  db.tiles.where('accessed').below(threshold).delete();
};

const urlToCacheKey = (url) => {
  // XXX theme provides a quick-fix to differentiate dark and light tiles in the cache.
  // It is a bit hacky but until multiple themes are availalble for the user to select
  // this will work although it theoretically doubles the amount of tiles in the cache.
  // An alternative may be to only allow one set of tiles in cache and have whatever 
  // triggers the change to the map tile source to dump all tiles and begin saving 
  // cached tiles all over again.
  let theme;
  if (url.includes('openstreetmap')) {
    theme = 'light';
  } else {
    theme = 'dark';
  }
  let segments = url.split('/').slice(-3);
  let x = segments[0];
  let y = segments[1];
  let z = segments[2].split('.')[0];
  return `theme:${theme}x:${x}y:${y}z:${z}`;
};

const expireCacheItems = async () => {};

const cacheMatch = async ({ url, event }) => {
  let cachedResponse;
  let cached = await getTile(url);
  if (cached) {
    let threshold = new Date();
    threshold = threshold.setTime(threshold.getTime() - (1000 * tileValidSeconds));
    if (cached.accessed < threshold) {
      if (process.env.NODE_ENV !== 'production') {
        console.log(`Stale cache tile found. Will revalidate.`);
      }
      event.waitUntil(fetchAndCachePut({ url: url }));
    }
    else {
      updateTileAccessedDate(cached.coords);
    }
    cachedResponse = new Response(cached.tile.stream());
  }
  if (process.env.NODE_ENV !== 'production') {
    if (process.env.NODE_ENV !== 'production') {
      if (cachedResponse) {
        console.log(`Found a cached map tile response.`);
      }
      else {
        console.log(`No cached map tile response found.`);
      }
    }
  }
  return cachedResponse;
};

const cachePut = async ({ url, response }) => {
  if (!response) {
    if (process.env.NODE_ENV !== 'production') {
      console.log(`Cannot cache non-existent response for ` +
        `'${url}'.`);
    }
    throw new WorkboxError('cache-put-with-no-response', {
      url: url,
    });
  }
  // TODO here run any cache expiration checks
  let responseToCache = await response.blob()
  if (process.env.NODE_ENV !== 'production') {
    console.log(`Updating the map tile cache with a new Response ` +
      `for ${url}.`);
  }
  try {
    await saveTile({ url: url, tile: responseToCache });
  }
  catch (error) {
    if ((error.name === 'QuotaExceededError') ||
      (error.inner && error.inner.name === 'QuotaExceededError')) {
      // QuotaExceededError may occur as the inner error of an AbortError
      console.error("QuotaExceeded error!");
      // TODO run quota exceeded callback
    } else {
      // Any other error
      console.error(error);
    }
    throw error;
  }
  return true;
};

const fetchAndCachePut = async ({ url }) => {
  const response = await fetch(url);
  const responseClone = response.clone();
  await cachePut({ url: url, response: responseClone })
  return response
};

const mapTileHandler = async ({ url, event, params }) => {
  /* 
   * This is a CacheFirst strategy using IndexedDB to hold 
   * tile blobs since they can fill a normal cache far too 
   * quickly. 
   * 
   * Perhaps there is way to do this cleanly by extending 
   * a workbox Strategy but for now I'll manually recreate 
   * a custom strategy and learn some things along the way.
   * 
   * Although in earlier commits you can find the same 
   * work recreated in an extended Workbox Strategy, I 
   * went this way since I'm not using cache storage.
   * It could be done by probably overriding the handler 
   * instead of the strategy since that is where the real 
   * work is done to put contents into cache.
   */
  let response = await cacheMatch({ url: url.href, event: event });
  let error;
  if (!response) {
    if (process.env.NODE_ENV !== 'production') {
      console.log(`No response found in the cache. ` +
        `Will respond with a network request.`);
    }
    try {
      response = await fetchAndCachePut({ url: url.href })
    }
    catch (err) {
      error = err;
    }
    if (process.env.NODE_ENV !== 'production') {
      if (response) {
        console.log(`Got response from network.`);
      }
      else {
        console.log(`Unable to get a response from the network.`);
      }
    }
  }
  else {
    if (process.env.NODE_ENV !== 'production') {
      console.log(`Found a cached response in the map tile cache.`);
    }
  }
  if (!response) {
    throw new WorkboxError('no-response', { url: url.href, error });
  }
  return response;
}

registerRoute(
  ({ url }) => url.href.includes('tile.openstreetmap.org'),
  mapTileHandler,
);

registerRoute(
  ({ url }) => url.href.includes('global.ssl.fastly.net/dark_all'),
  mapTileHandler,
);

// Not useful for our SPA I believe
// // Cache page navigations (html) with a Network First strategy
// registerRoute(
//   // Check to see if the request is a navigation to a new page
//   ({ request }) => request.mode === 'navigate',
//   // Use a Network First caching strategy
//   new NetworkFirst({
//     // Put all cached files in a cache named 'pages'
//     cacheName: 'pages',
//     plugins: [
//       // Ensure that only requests that result in a 200 status are cached
//       new CacheableResponsePlugin({
//         statuses: [200],
//       }),
//     ],
//   }),
// );

// Make sure to return a specific response for all navigation requests.
// Since we have a SPA here, this should be index.html always.
// https://stackoverflow.com/questions/49963982/vue-router-history-mode-with-pwa-in-offline-mode
// NavigationRoute('/index.html');

// // Setup cache strategy for Google Fonts. They consist of two parts, a static one
// // coming from fonts.gstatic.com (strategy CacheFirst) and a more ferquently updated on
// // from fonts.googleapis.com. Hence, split in two registerroutes
// registerRoute(
//   /^https:\/\/fonts\.googleapis\.com/,
//   new StaleWhileRevalidate({
//     cacheName: 'google-fonts-stylesheets',
//   }),
// );

// registerRoute(
//   /^https:\/\/fonts\.gstatic\.com/,
//   new CacheFirst({
//     cacheName: 'google-fonts-webfonts',
//     plugins: [
//       new CacheableResponsePlugin({
//         statuses: [0, 200],
//       }),
//       new ExpirationPlugin({
//         maxAgeSeconds: 60 * 60 * 24 * 365,
//         maxEntries: 30,
//       }),
//     ],
//   }),
// );

// // Cache CSS, JS, and Web Worker requests with a Stale While Revalidate strategy
// registerRoute(
//   // Check to see if the request's destination is style for stylesheets, script for JavaScript, or worker for web worker
//   ({ request }) =>
//     request.destination === 'style' ||
//     request.destination === 'script' ||
//     request.destination === 'worker',
//   // Use a Stale While Revalidate caching strategy
//   new StaleWhileRevalidate({
//     // Put all cached files in a cache named 'assets'
//     cacheName: 'assets',
//     plugins: [
//       // Ensure that only requests that result in a 200 status are cached
//       new CacheableResponsePlugin({
//         statuses: [200],
//       }),
//     ],
//   }),
// );

// TODO cache thumbnails separate from full-size images
// Cache images with a Cache First strategy
registerRoute(
  // Check to see if the request's destination is for an image
  ({ request }) => request.destination === 'image',
  // Use a Cache First caching strategy
  new CacheFirst({
    // Put all cached files in a cache named 'images'
    cacheName: 'bilolok-images',
    plugins: [
      // Ensure that only requests that result in a 200 status are cached
      new CacheableResponsePlugin({
        statuses: [200],
      }),
      // Don't cache more than 60 items, and expire them after 30 days
      new ExpirationPlugin({
        maxEntries: 60,
        maxAgeSeconds: 60 * 60 * 24 * 30, // 30 Days
      }),
    ],
  }),
);

// const ourDomains = ["localhost:8000"];
// const mapTilesDomain = "tile.openstreetmap.org/";
// const ignoreDomains = ["googleapis", "facebook", "gstatic"];
// function fetchApplicationAsset(event) {
//   if (ourDomains.reduce(function(cum, domain) {
//     return cum || event.request.url.indexOf(domain) != -1;
//   }, false)) {
//     return fetchUserAsset(event);
//   }

//   return caches.match(event.request).then(function(response) {
//     if (response) {
//       return response;
//     }
//     var isMapTilesReq = event.request.url.indexOf(mapTilesDomain) != -1;
//     if (isMapTilesReq) {
    
//       console.log(event.request.url)

//       var re = /\/(\d+)\/(\d+)\/(\d+).vector.pbf/;
//       var matched = event.request.url.match(re);
//       if (matched) {
//         console.log(matched)
//         var key = {z:matched[1],x:matched[2],y:matched[3]};
//         return tileCacheDb.get(key)
//         .then(function(tileBuffer) {
//           if (tileBuffer) {
//             return new Response(tileBuffer);
//           }
//           return fetch(event.request)
//         });
//       }
//     }

//     if (!ignoreDomains.find(function(domain) {return event.request.url.indexOf(domain) != -1})) {
//       console.log("Unmatched URL '" + event.request.url+"'");
//     }
//     return fetch(event.request);
//   });
// }

/* Web Push Notifications */

self.addEventListener('push', (e) => {
  if (!(self.Notification && self.Notification.permission === 'granted')) {
    return;
  };
  let push_data = e.data.json();
  const options = {
    actions: push_data.actions,
    body: push_data.body,
    icon: './img/icon.png',
    image: './img/notification.jpg',
  };
  e.waitUntil(
    self.registration.showNotification(push_data.title, options)
  )
})

// Could make click on the notification open our app
self.addEventListener('notificationclick', (e) => {
  if (e.action === 'some_action') {
    // Do something...
  } else {
    self.clients.openWindow('/');
  };
})