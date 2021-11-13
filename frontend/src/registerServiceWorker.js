/* eslint-disable no-console */

import { register } from 'register-service-worker';

if (process.env.NODE_ENV === 'production') {
  register(`${process.env.BASE_URL}service-worker.js`, {
    ready() {
      console.log(
        'App is being served from cache by a service worker.\n'
        + 'For more details, visit https://goo.gl/AFskqB',
      );

      // TODO re-add this later once we actually have something to push to the user
      // Notification.requestPermission((status) => {
      //   console.log('Status: ', status);
      // });
    },
    registered() {
      console.log('Service worker has been registered.');
    },
    cached() {
      console.log('Content has been cached for offline use.');
    },
    updatefound() {
      console.log('New content is downloading.');
    },
    updated(registration) {
      console.log('New content is available! We\'ll show a refresh button for the user to click on and refresh');
      // Signal frontend that a new update is available
      document.dispatchEvent(new CustomEvent('swUpdated', { detail: registration }));
    },
    offline() {
      console.log('No internet connection found. App is running in offline mode.');
      // Signal frontend that internet connection is lost
      // document.dispatchEvent(new CustomEvent('swOffline'))
    },
    error(error) {
      console.error('Error during service worker registration:', error);
    },
  });
}
