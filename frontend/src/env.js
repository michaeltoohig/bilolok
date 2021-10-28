const env = process.env.VUE_APP_ENV;

let envApiDomain = '';

if (env === 'production') {
  envApiDomain = `https://${process.env.VUE_APP_DOMAIN_PROD}`;
} else if (env === 'staging') {
  envApiDomain = `https://${process.env.VUE_APP_DOMAIN_STAG}`;
} else {
  envApiDomain = `http://${process.env.VUE_APP_DOMAIN_DEV}`;
}

export const apiDomain = envApiDomain;

let envUploadDomain = '';

if (env === 'production') {
  envUploadDomain = `https://${process.env.VUE_APP_UPLOAD_DOMAIN_PROD}`;
} else if (env === 'staging') {
  envUploadDomain = `https://${process.env.VUE_APP_UPLOAD_DOMAIN_STAG}`;
} else {
  envUploadDomain = `http://${process.env.VUE_APP_UPLOAD_DOMAIN_DEV}`;
}

export const uploadDomain = envUploadDomain;
export const appName = process.env.VUE_APP_NAME;
