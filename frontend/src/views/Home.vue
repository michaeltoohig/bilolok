<template>
  <div class="home px-3">
    <v-container>
      <v-row>
        <v-col>
          <h1 class="text-h1 text-center">Bilolok</h1>

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
              outlined
              color="primary"
              :to="{ name: 'Map' }"
            >
              View the Map
            </v-btn>
          </v-col>
        </v-row>
      </v-parallax>
    </v-container>
    <SectionRecentCheckins />
    <SectionRecentImages />

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
import SectionRecentImages from '@/components/home/SectionRecentImages.vue';
import SectionRecentCheckins from '@/components/home/SectionRecentCheckins.vue';

const lightMapImage = require('../assets/PortVilaMap-light.jpg');
const darkMapImage = require('../assets/PortVilaMap-dark.jpg');

export default {
  name: 'Home',
  components: {
    SectionRecentImages,
    SectionRecentCheckins,
  },
  data() {
    return {
      darkMapImage,
      lightMapImage,
    };
  },
  computed: {
    ...mapGetters({
      darkMode: 'setting/darkMode',
    }),
    mapImagePath() {
      if (this.darkMode) {
        return darkMapImage;
      }
      return lightMapImage;
    },
  },
};
</script>

<style>

</style>
