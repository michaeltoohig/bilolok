<template>
  <v-container class="about">
    <v-responsive max-width="500" class="mx-auto">
      <h1>About Bilolok</h1>

      <p>Bilolok literally means <strong>Kava</strong> in the local language of a small
        village on the east, south-east side of Malekula island in Vanuatu.</p>

      <div id="map-wrapper" class="my-5">
        <l-map
          style="z-index: 0;"
          ref="map"
          :zoom="zoom"
          :min-zoom="minZoom"
          :max-zoom="maxZoom"
          :center="center"
          :max-bounds="maxBounds"
        >
          <l-tile-layer
            :url="url"
            :attribution="attribution"
          />
          <l-circle
            :radius="radius"
            :lat-lng="center"
          ></l-circle>
        </l-map>
      </div>

      <h2>History</h2>

      <p>I had been wanting an app to map the kava bars around town for about 5 years.
        I have some old attempts at starting this project, since abandoned, still on
        my harddrive. The attempt I made a few years ago even had a name and custom
        icons, but ultimately I was distracted by other projects, friends, work, etc.
        and did not continue it.</p>

      <v-card outlined elevation="2" class="my-5 pt-3">
        <v-img class="ml-5" :src="malokayLogo"></v-img>
        <v-card-subtitle>Original logo. The name was a mix of
          <i>Malok</i> and <i>Okay</i>. The idea was to find kava that
          was okay to drink.</v-card-subtitle>
      </v-card>

      <div class="d-flex flex-row justify-space-between justify-md-space-around my-5">
        <v-card outlined elevation="2" max-width="170">
          <v-img class="mt-3" :src="malokayKavaMarker"></v-img>
          <v-card-subtitle>Malokay map marker for kava bars</v-card-subtitle>
        </v-card>
        <v-card outlined elevation="2" max-width="170">
          <v-img class="mt-3" :src="malokayKavaBeerMarker"></v-img>
          <v-card-subtitle>Malokay map marker for kava bars with alcohol for sale</v-card-subtitle>
        </v-card>
      </div>

      <p>It wasn't until I saw the old Kava-World site that I started to build this project again.
        The Kava-World project is similar but their focus seems to be more
        towards the international market and was built on WordPress and did not have
        a single, unified map view to browse the kava bars. Now, they have moved to using
        Svelte on their frontend and focus their page around a map but I had already
        gone so far with this project so I'm not going to stop.</p>

      <p>Before Kava-World I know Hunter Sizemore had built a WordPress
        site (now missing?) for voting on kava bars called <i>kava.buzz</i> but I don't know what
        happened afterwards.</p>

      <h2>This Project</h2>

      <p>I made this project open-source in hopes to find individuals interested in
        learning web development and help build this project. I thought that would
        make this project more sustainable and help develop a small local scene of
        developers who could build apps focused on local interests.</p>

      <v-alert
        text
        color="info"
        icon="mdi-github"
      >
        <v-row align="center">
          <v-col class="grow">
            <h3 class="text-h5">
              Want to Contribute?
            </h3>
          </v-col>
          <v-col class="shrink">
            <v-btn icon @click="openGithubDropDown = !openGithubDropDown">
              <v-icon v-if="openGithubDropDown">mdi-chevron-up</v-icon>
              <v-icon v-else>mdi-chevron-down</v-icon>
            </v-btn>
          </v-col>
        </v-row>

        <v-expand-transition>
          <div v-show="openGithubDropDown">
            <v-divider
              class="my-4 info"
              style="opacity: 0.22"
            ></v-divider>
            <h4>Want to join the development?</h4>
            <p>
              For anyone in Vanuatu, especially CS students, interested in learning
              software development, I will be happy to work with you and help you
              contribute your ideas to this project.
            </p>
            <v-btn
              v-show="false"
              color="info"
              outlined
              @click="openGithub"
              class="mb-3"
            >
              View Source Code
            </v-btn>
          </div>
        </v-expand-transition>
      </v-alert>

      <p>This project also scratches an itch I've had with a desire to experiment with
        PWA technologies that allow this app to work offline and is why you can find
        this app on the Google Play even though it is built with web technologies.
      </p>

      <div class="my-5 d-flex justify-center">
        <a
          href='https://play.google.com/store/apps/details?id=com.bilolok.twa&pcampaignid=pcampaignidMKT-Other-global-all-co-prtnr-py-PartBadge-Mar2515-1'
        >
          <img
            width="175"
            alt='Get it on Google Play'
            src='https://play.google.com/intl/en_us/badges/static/images/badges/en_badge_web_generic.png'
          />
        </a>
      </div>

      <p>The frontend of this app is built with Vue.js and the backend API is built
        with FastAPI a Python web framework.</p>

      <h2>Roadmap</h2>

      <p>I would say the application itself is nearly at a version 1.0, meaning
        I only have one behind the scenes feature for the database to add and
        some minor tweaks to the frontend to have what I would call a <i>complete</i>
        app.</p>

      <p>Version 2.0 would include more social features such as user badges and
        leader boards for being active on the app. Special map views that show
        your history of check-ins and other interactive elements or charts. And,
        I already have in mind a way to help track which windows are most popular
        at a given kava bar.</p>

      <h2>Special Thanks</h2>

      <v-list>
        <v-list-item two-line>
          <v-list-item-content>
            <v-list-item-title>My Wife</v-list-item-title>
            <v-list-item-subtitle>
              Thank you for being supportive.
            </v-list-item-subtitle>
          </v-list-item-content>
        </v-list-item>
      </v-list>
    </v-responsive>
  </v-container>
</template>

<script>
import {
  latLngBounds,
} from 'leaflet';
import {
  LMap, LTileLayer, LCircle,
} from 'vue2-leaflet';
import { mapGetters } from 'vuex';

const malokayLogo = require('../assets/MalokayLogo.svg');
const malokayKavaMarker = require('../assets/KavaMarker.svg');
const malokayKavaBeerMarker = require('../assets/KavaBeerMarker.svg');

export default {
  name: 'About',
  components: {
    LMap,
    LTileLayer,
    LCircle,
  },
  data() {
    return {
      openGithubDropDown: false,
      // Malokay
      malokayKavaMarker,
      malokayKavaBeerMarker,
      malokayLogo,
      // Map
      zoom: 15,
      maxZoom: 15,
      minZoom: 10,
      radius: 500,
      center: [-16.2185, 167.5715],
      maxBounds: latLngBounds([
        [-16.20, 167.55],
        [-16.23, 167.59],
      ]),
    };
  },
  computed: {
    ...mapGetters({
      darkMode: 'setting/darkMode',
    }),
    url() {
      if (this.darkMode) {
        return 'https://cartodb-basemaps-{s}.global.ssl.fastly.net/dark_all/{z}/{x}/{y}.png';
      }
      return 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';
    },
    attribution() {
      if (this.darkMode) {
        return 'Map tiles by Carto, under CC BY 3.0. Data by OpenStreetMap, under ODbL.';
      }
      return '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors';
    },
  },
  methods: {
    openGithub() {
      window.open('https://github.com/michaeltoohig/bilolok');
    },
  },
};
</script>

<style scoped>
#map-wrapper {
  height: 400px;
}
</style>
