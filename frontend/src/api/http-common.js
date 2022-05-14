// import axios from 'axios';
// // import store from '@/store';
// // import router from '@/router';

// import { apiDomain } from '@/env';

// const baseURL = `${apiDomain}/api/v1/`;

// const http = axios.create({
//   baseURL,
//   timeout: 10,
//   headers: {
//     'Content-Type': 'application/json',
//   },
// });

// const responseHandler = (response) => response;

// const errorHandler = (error) => {
//   console.log('API Error Handler:', error.message);
//   if (error.response) {
//     if (error.response.status === 401) {
//       // TODO this pattern fails for logged in users
//       //  eg. an unverified user trying to add a nakamal so
//       //  be sure to wrap all requests that require auth in
//       //  a check user auth and show auth modal instead of allowing
//       //  the user action.
//       console.log('!! Unauthorized');
//       // router.push('/auth/login?unauthorized=true');
//       return Promise.reject(error);
//     }
//   } else if (error.request) {
//     if (error.message.startsWith('timeout')) {
//       // Timeout error server took too long to respond
//       console.log('timeout error');
//       // store.dispatch('notify/add', {
//       //   title: 'Timeout Error',
//       //   text: 'Sorry, the server did not respond in time.',
//       //   type: 'error',
//       // });
//     }
//   } else {
//     // Something happened in setting up the request that triggered an Error
//     console.log('Error', error.message);
//   }
//   console.log(error.config);
//   return Promise.reject(error);
// };

// http.interceptors.response.use(
//   (response) => responseHandler(response),
//   (error) => errorHandler(error),
// );

// export default http;
