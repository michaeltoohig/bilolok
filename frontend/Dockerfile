FROM node:14 as base

FROM base AS development

WORKDIR /app
COPY package.json yarn.lock ./
RUN yarn install

FROM base as build

WORKDIR /app
COPY . .
COPY --from=development /app/node_modules ./node_modules
RUN yarn build

FROM nginx:1.19-alpine as production

WORKDIR /usr/share/nginx/html
RUN rm -rf ./*
COPY --from=build /app/dist .
EXPOSE 80
ENTRYPOINT ["nginx", "-g", "daemon off;"]