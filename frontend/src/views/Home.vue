<template>
  <div class="home px-3">
    <v-container>
      <v-row>
        <v-col>
          <div class="d-flex flex-sm-row flex-column align-center justify-center">
            <v-responsive max-width="140" class="flex-shrink-1">
              <v-img :src="logo"/>
            </v-responsive>
            <h1 class="text-h1 font-weight-bold">Bilolok</h1>
          </div>

          <p class="text-center">
            Bilolok means <strong>Kava</strong> in the local language of a small
            village on the east, south-east side of Malekula island in Vanuatu.
          </p>

          <hr class="mb-5"/>
        </v-col>
      </v-row>
    </v-container>
    <v-container>
      <v-parallax
        :dark="darkMode"
        :src="mapImagePath"
      >
        <v-row
          align="center"
          justify="center"
        >
          <v-col
            class="text-center"
            cols="12"
          >
            <h1 class="text-h4 font-weight-bold mb-4" :class="{'black--text': !darkMode}">
              Explore the kava bars!
            </h1>
            <v-btn
              x-large
              tile
              color="primary"
              :to="{ name: 'Map' }"
            >
              Go to the Map
              <v-icon>mdi-chevron-right</v-icon>
            </v-btn>
          </v-col>
        </v-row>
      </v-parallax>
    </v-container>
    <v-responsive class="mx-auto" max-width="600">
      <SectionFeaturedNakamal />
      <SectionRecentTimeline />
      <div v-if="!isLoggedIn" class="text-center">
        <hr class="my-5"/>
        <h2 class="headline text-h4">Join Bilolok</h2>
        <v-btn
          text
          outlined
          color="primary"
          @click="goToSignup"
        >
          Create an Account
          <v-icon>mdi-chevron-right</v-icon>
        </v-btn>
      </div>
    </v-responsive>

    <hr class="mt-5"/>
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
  </div>
</template>

<script>
import { mapGetters } from 'vuex';
import SectionFeaturedNakamal from '@/components/home/SectionFeaturedNakamal.vue';
import SectionRecentTimeline from '@/components/home/SectionRecentTimeline.vue';

const lightMapImage = require('../assets/PortVilaMap-light.jpg');
const darkMapImage = require('../assets/PortVilaMap-dark.jpg');
const logo = require('../assets/logo.png');

export default {
  name: 'Home',
  components: {
    SectionFeaturedNakamal,
    SectionRecentTimeline,
  },
  data() {
    return {
      darkMapImage,
      lightMapImage,
      logo,
    };
  },
  computed: {
    ...mapGetters({
      isLoggedIn: 'auth/isLoggedIn',
      darkMode: 'setting/darkMode',
    }),
    mapImagePath() {
      if (this.darkMode) {
        return darkMapImage;
      }
      return lightMapImage;
    },
  },
  methods: {
    goToSignup() {
      this.$router.push({ name: 'Auth', params: { auth: 'signup' } });
    },
  },
};
</script>

<style>

</style>
