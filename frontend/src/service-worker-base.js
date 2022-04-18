/* eslint-disable */

import Dexie from 'dexie';
// import {
//   setCacheNameDetails,
// } from 'workbox-core';
import {
  registerRoute,
  NavigationRoute,
  setDefaultHandler,
  setCatchHandler,
} from 'workbox-routing';
import {
  NetworkOnly,
  NetworkFirst,
  StaleWhileRevalidate,
  CacheFirst,
} from 'workbox-strategies';
import {
  precacheAndRoute,
  cleanupOutdatedCaches,
} from 'workbox-precaching';
import { BackgroundSyncPlugin } from 'workbox-background-sync';
import { WorkboxError } from 'workbox-core/_private/WorkboxError.js';
// Used for filtering matches based on status code, header, or both
import { CacheableResponsePlugin } from 'workbox-cacheable-response';
// Used to limit entries in cache, remove entries after a certain period of time
import { ExpirationPlugin } from 'workbox-expiration';

import { apiDomain } from '@/env';

const precacheUrls = [
  { revision: null, url: `${apiDomain}/api/v1/nakamal-areas` },
  { revision: null, url: `${apiDomain}/api/v1/nakamal-kava-sources` },
  { revision: null, url: `${apiDomain}/api/v1/nakamal-resources` },
  ...self.__WB_MANIFEST,
];

// Use with precache injection
precacheAndRoute(precacheUrls);

// Remove outdated pre-caches - not sure this does what I expect yet
cleanupOutdatedCaches();

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
    db.tiles.where('coords').equals(key).modify((t) => {
      t.accessed = new Date().getTime();
      t.tile = tile;
    })
      .then((result) => {
        return true;
      })
      .catch((error) => {
        if ((e.name === 'QuotaExceededError') ||
          (e.inner && e.inner.name === 'QuotaExceededError')) {
          // QuotaExceededError may occur as the inner error of an AbortError
          console.error('?!# QuotaExceeded error!');
          clearTileStore();
        } else {
          // Any other error
          console.error('?!##', error);
        }
      });
  }
  else {
    db.tiles.put({ coords: key, accessed: new Date(), tile: tile }).then(result => {
      return true;
    }).catch((error) => {
      if ((e.name === 'QuotaExceededError') ||
        (e.inner && e.inner.name === 'QuotaExceededError')) {
        // QuotaExceededError may occur as the inner error of an AbortError
        console.error('!# QuotaExceeded error!');
        clearTileStore();
      } else {
        // Any other error
        console.error('!##', error);
      }
    });
  }
};

const updateTileAccessedDate = async (key) => {
  db.tiles.where('coords').equals(key).modify(tile => {
    tile.accessed = new Date().getTime();
  });
};

// TODO use perhaps periodically to clear unused tiles after extended periods
const removeExpiredTiles = async () => {
  let threshold = new Date();
  threshold = threshold.setTime(threshold.getTime() - (1000 * tileValidSeconds));
  await db.tiles.where('accessed').below(threshold).delete();
};

const clearTileStore = async () => {
  let now = new Date().getTime();
  const deleteCount = await db.tiles.where('accessed').below(now).delete();
  console.log("Deleted " + deleteCount + " objects");
  return true;
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
    console.log('###', error);
    if ((error.name === 'QuotaExceededError') ||
      (error.inner && error.inner.name === 'QuotaExceededError')) {
      // QuotaExceededError may occur as the inner error of an AbortError
      console.error("###!! QuotaExceeded error!");
      // TODO run quota exceeded callback
    } else {
      // Any other error
      console.error('###!', error);
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
  ({ url }) => url.href.includes('tile.openstreetmap.org') ||
               url.href.includes('global.ssl.fastly.net/dark_all'),
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

// Nakamal API cache
registerRoute(
  ({ request }) => request.url.includes('/api/v1/nakamals'),
  new NetworkFirst({
    cacheName: 'bilolok-api-nakamals',
    plugins: [
      // Ensure that only requests that result in a 200 status are cached
      new CacheableResponsePlugin({
        statuses: [200],
      }),
    ],
  }),
);

// User API cache
registerRoute(
  ({ request }) => request.url.includes('/api/v1/users'),
  new NetworkFirst({
    cacheName: 'bilolok-api-users',
    plugins: [
      // Ensure that only requests that result in a 200 status are cached
      new CacheableResponsePlugin({
        statuses: [200],
      }),
    ],
  }),
);

// Nakamal image cache
registerRoute(
  // Check to see if the request's destination is for an image
  ({ request }) => request.destination === 'image' && request.url.includes('/nakamals/'),
  // Use a Cache First caching strategy
  new CacheFirst({
    // Put all cached files in a cache named 'images'
    cacheName: 'bilolok-images',
    plugins: [
      // Ensure that only requests that result in a 200 status are cached
      new CacheableResponsePlugin({
        statuses: [200],
      }),
      // Don't cache more than 50 items, and expire them after 7 days
      new ExpirationPlugin({
        maxEntries: 50,
        maxAgeSeconds: 60 * 60 * 24 * 7, // 7 Days
        // Automatically cleanup if quota is exceeded.
        purgeOnQuotaError: true,
      }),
    ],
  }),
);

// User image cache
registerRoute(
  // Check to see if the request's destination is for an image
  ({ request }) => request.destination === 'image' && request.url.includes('/users/'),
  // Use a Cache First caching strategy
  new CacheFirst({
    // Put all cached files in a cache named 'images'
    cacheName: 'bilolok-avatars',
    plugins: [
      // Ensure that only requests that result in a 200 status are cached
      new CacheableResponsePlugin({
        statuses: [200],
      }),
      // Don't cache more than 50 items, and expire them after 1 days
      new ExpirationPlugin({
        maxEntries: 50,
        maxAgeSeconds: 60 * 60 * 24 * 1, // 1 Days
        // Automatically cleanup if quota is exceeded.
        purgeOnQuotaError: true,
      }),
    ],
  }),
);

// Use a stale-while-revalidate strategy for all other requests.
setDefaultHandler(new StaleWhileRevalidate());

// https://stackoverflow.com/questions/60036010/keep-the-precache-while-deleting-other-cache-in-workbox-service-worker
// Clear old caches
var clearOldCaches = function (event) {
  event.waitUntil(
    caches.keys().then(function (cacheNames) {
      let validCacheSet = new Set(Object.values(workbox.core.cacheNames));
      return Promise.all(
        cacheNames
          .filter(function (cacheName) {
            return !validCacheSet.has(cacheName);
          })
          .map(function (cacheName) {
            return caches.delete(cacheName);
          })
      );
    })
  );
};

self.addEventListener("activate", function (event) {
  clearOldCaches(event);
});

// This "catch" handler is triggered when any of the other routes fail to
// generate a response.
setCatchHandler(async ({event}) => {
  // The FALLBACK_URL entries must be added to the cache ahead of time, either
  // via runtime or precaching. If they are precached, then call
  // `matchPrecache(FALLBACK_URL)` (from the `workbox-precaching` package)
  // to get the response from the correct cache.
  //
  // Use event, request, and url to figure out how to respond.
  // One approach would be to use request.destination, see
  // https://medium.com/dev-channel/service-worker-caching-strategies-based-on-request-types-57411dd7652c
  switch (event.request.destination) {
    case 'document':
      // If using precached URLs:
      // return matchPrecache(FALLBACK_HTML_URL);
      return caches.match('/index.html');
    break;

    // case 'image':
    //   return caches.match('/wifi-connection-offline.png');
    // break;

    default:
      // If we don't have a fallback, just return an error response.
      return Response.error();
  }
});

const bgSyncCheckinPlugin = new BackgroundSyncPlugin('api-checkin-queue', {
  maxRetentionTime: 60 * 60 * 24, // Retry for 24 hours
});

registerRoute(
  ({ request }) => request.url.includes('/api/v1/checkins'),
  new NetworkOnly({
    plugins: [bgSyncCheckinPlugin],
  }),
  'POST',
);

const bgSyncTripPlugin = new BackgroundSyncPlugin('api-trip-queue', {
  maxRetentionTime: 60 * 60 * 24, // Retry for 24 hours
});

registerRoute(
  ({ request }) => request.url.includes('/api/v1/trips'),
  new NetworkOnly({
    plugins: [bgSyncTripPlugin],
  }),
  'POST',
);

const bgSyncNakamalPlugin = new BackgroundSyncPlugin('api-nakamal-queue', {
  maxRetentionTime: 60 * 60 * 24, // Retry for 24 hours
});

registerRoute(
  ({ request }) => request.url.includes('/api/v1/nakamals'),
  new NetworkOnly({
    plugins: [bgSyncNakamalPlugin],
  }),
  'POST',
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
  console.log('got push!', e.data);

  if (!(self.Notification && self.Notification.permission === 'granted')) {
    console.log('push not available :(');
    return;
  };

  const push_data = e.data.json();
  const title = push_data.title || 'Bilolok'
  const options = {
    // actions: push_data.actions,
    // image: './img/BilolokCover.png',
    body: push_data.body,
    icon: './img/AppImages/192x192.png',
    tag: 'tag-1',
    vibrate: [500, 100, 100, 100],
    data: {
      id: push_data.id,
    },
  };
  e.waitUntil(
    self.registration.showNotification(title, options)
  );
});

// Hard to test since can't seem to manually trigger this event in dev
// self.addEventListener('pushsubscriptionchange', function (e) {
//   console.log('Subscription expired');
//   e.waitUntil(
//     self.registration.pushManager.subscribe({ userVisibleOnly: true })
//       .then(function (subscription) {
//         console.log('Subscribed after expiration', subscription.endpoint, subscription);
//         // return fetch('register', {
//         //   method: 'post',
//         //   headers: {
//         //     'Content-type': 'application/json'
//         //   },
//         //   body: JSON.stringify({
//         //     endpoint: subscription.endpoint
//         //   })
//         // });
//       })
//   );
// });

// Could make click on the notification open our app
self.addEventListener('notificationclick', (e) => {
  console.log('notificationclick', e.notification);
  // Close notification.
  e.notification.close();
  
  self.clients.matchAll().then(function (clis) {
    var client = clis.find(function (c) {
      c.visibilityState === 'visible';
    });
    if (client !== undefined) {
      client.navigate('/map');
      client.focus();
    } else {
      // there are no visible windows. Open one.
      self.clients.openWindow('/map');
    }
  });
  
  // close all notifications with tag of 'id1'
  // var options = { tag: e.notification.tag };
  // self.registration.getNotifications(options).then(function (notifications) {
  //   notifications.forEach(function (notification) {
  //     notification.close();
  //   });
  // });
});