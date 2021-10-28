<template>
  <div class="nakamal">
    <div v-if="loading">
      Loading...
    </div>
    <div v-else>
      <v-card flat color="secondary">
        <v-card-title>
          <h1>{{ nakamal.name }}</h1>
        </v-card-title>
        <v-card-text>
          <ul class="list-unstyled">
            <li>Owner: {{ nakamal.owner }}</li>
            <li>Number: {{ nakamal.number }}</li>
            <li>Light: {{ nakamal.light }}</li>
          </ul>
        </v-card-text>
      </v-card>

      <v-container>
        <v-tabs-items v-model="tab">
          <v-tab-item value="images">
            <v-container class="px-0">
              <v-row v-if="images.length === 0">
                <v-col>
                  <h2>No Images Yet</h2>
                </v-col>
              </v-row>
              <v-row v-else>
                <v-col
                  v-for="(image, i) in images"
                  :key="i"
                  class="d-flex child-flex"
                  cols="4"
                >
                  <v-img
                    :src="image.src"
                    :lazy-src="image.thumbnail"
                    aspect-ratio="1"
                    class="grey lighten-2"
                  >
                    <template v-slot:placeholder>
                      <v-row
                        class="fill-height ma-0"
                        align="center"
                        justify="center"
                      >
                        <v-progress-circular
                          indeterminate
                          color="grey lighten-5"
                        ></v-progress-circular>
                      </v-row>
                    </template>
                  </v-img>
                </v-col>
              </v-row>
            </v-container>
          </v-tab-item>
        </v-tabs-items>
      </v-container>
    </div>

    <v-fab-transition>
      <v-btn
        :key="activeFab.icon"
        fixed
        fab
        large
        dark
        bottom
        right
        :color="activeFab.color"
        @click="activeFab.action"
      >
        <v-icon>{{ activeFab.icon }}</v-icon>
      </v-btn>
    </v-fab-transition>

    <NakamalImageUpload
      v-if="nakamal"
      :nakamal="nakamal"
      :open="openUploadDialog"
      @close-modal="() => this.openUploadDialog = false"
    ></NakamalImageUpload>
  </div>
</template>

<script>
import { mapGetters } from 'vuex';
import NakamalImageUpload from '@/components/NakamalProfile/NakamalImageUpload.vue';
import nakamalsApi from '@/api/nakamals';

export default {
  name: 'Nakamal',
  components: {
    NakamalImageUpload,
  },
  data() {
    return {
      tab: 'images',
      openUploadDialog: false,
      images: [],
    };
  },
  computed: {
    ...mapGetters({
      hasAdminAccess: 'auth/hasAdminAccess',
      nakamal: 'nakamal/selected',
    }),
    loading() {
      return !this.nakamal;
    },
    activeFab() {
      switch (this.tab) {
        case 'timeline': return { color: 'success', icon: 'mdi-share-variant', action: () => {} };
        case 'images': return { color: 'red', icon: 'mdi-pencil', action: () => { this.openUploadDialog = !this.openUploadDialog; } };
        default: return {};
      }
    },
  },
  methods: {
    remove() {
      this.$store.dispatch('nakamal/remove', this.nakamal.id)
        .then(() => {
          this.$router.push({ name: 'Home' });
        });
    },
    fetchImages(id) {
      nakamalsApi.get_images(id)
        .then((response) => {
          this.images = response.data;
        });
    },
  },
  async mounted() {
    const { id } = this.$route.params;
    this.fetchImages(id);
    await this.$store.dispatch('nakamal/select', id)
      .then(() => {
        if (!this.nakamal) {
          this.$store.dispatch('nakamal/loadOne', id);
        }
      });
  },
};
</script>

<style>

</style>
