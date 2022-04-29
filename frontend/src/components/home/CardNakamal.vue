<template>
  <v-card>
    <v-img
      v-if="hasImages"
      class="white--text align-end"
      max-height="300px"
      :src="images[0].src"
    >
      <v-card-title></v-card-title>
    </v-img>
    <v-card-title class="pb-0 primary--text">
      <a @click="viewPage(nakamal.id)">
        {{ nakamal.name }}
      </a>
    </v-card-title>
    <v-card-subtitle v-if="nakamal.aliases.length" class="pt-2">
      {{ nakamal.aliases.join(', ') }}
    </v-card-subtitle>

    <v-card-text class="text--primary">
      <v-row>
        <v-col cols="6">
          <div class="font-weight-light">
            Light:
            <span class="font-weight-bold">{{ nakamal.light }}</span>
          </div>
          <div class="font-weight-light">
            Windows:
            <span class="font-weight-bold">{{ nakamal.windows || '-' }}</span>
          </div>
        </v-col>
        <v-col cols="6">
          <div class="font-weight-light">
            Area:
            <span class="font-weight-bold">{{ nakamal.area.name }}</span>
          </div>
          <div class="font-weight-light">
            Kava Source:
            <span class="font-weight-bold">{{ kavaSource(nakamal.kava_source) }}</span>
          </div>
          <div class="font-weight-light">
          </div>
        </v-col>
      </v-row>
    </v-card-text>
    <v-card-actions>
      <v-btn
        text
        outlined
        @click="viewPage(nakamal.id)"
      >
        Go to Kava Bar
      </v-btn>
    </v-card-actions>
  </v-card>
</template>

<script>
import { mapGetters } from 'vuex';

export default {
  name: 'CardNakamal',
  props: ['nakamal'],
  computed: {
    ...mapGetters({
      getImages: 'image/nakamal',
    }),
    hasImages() {
      return this.images.length > 0;
    },
    images() {
      return this.getImages(this.nakamal.id);
    },
  },
  methods: {
    // async onShare() {
    //   console.log('ok');
    // },
    viewPage(id) {
      this.$store.dispatch('nakamal/select', id)
        .then(() => {
          this.$router.push({ name: 'Nakamal', params: { id } });
        });
    },
    kavaSource(ks) {
      let v = ks.province;
      if (ks.island) {
        v += `: ${ks.island}`;
      }
      return v;
    },
  },
  beforeMount() {
    if (!this.hasImages) {
      this.$store.dispatch('image/getNakamal', this.nakamal.id);
    }
  },
};
</script>

<style>

</style>
