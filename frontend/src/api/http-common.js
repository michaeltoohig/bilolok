import axios from 'axios';
// import router from '@/router';

import { apiDomain } from '@/env';

const baseURL = `${apiDomain}/api/v1/`;

const http = axios.create({
  baseURL,
  timeout: 10_000,
  headers: {
    'Content-Type': 'application/json',
  },
});

const responseHandler = (response) => response;

const errorHandler = (error) => {
  console.log('API Error Handler:', error.response);
  if (error.response.status === 401) {
    // TODO this pattern fails for logged in users
    //  eg. an unverified user trying to add a nakamal
    console.log('!! Unauthorized');
    return Promise.reject(error);
    // TODO re-implement this functionality to redirect after login failure or
    //   allow user to choose to go to login when alerted to the failure
    // router.push('/auth/login?unauthorized=true');
  }
  return Promise.reject(error);
};

http.interceptors.response.use(
  (response) => responseHandler(response),
  (error) => errorHandler(error),
);

export default http;
