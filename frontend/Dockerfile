FROM node:10 as base

RUN npm i -g yarn

FROM base AS dependencies

WORKDIR /app
COPY package.json yarn.lock ./
RUN yarn install

FROM base as build

WORKDIR /app
COPY . .
COPY --from=dependencies /app/node_modules ./node_modules
RUN yarn build

FROM nginx:1.19-alpine as deploy

WORKDIR /usr/share/nginx/html
RUN rm -rf ./*
COPY --from=build /app/dist .
EXPOSE 80
ENTRYPOINT ["nginx", "-g", "daemon off;"]