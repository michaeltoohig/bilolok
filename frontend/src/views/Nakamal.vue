<template>
  <div class="nakamal">
    <div v-if="loading">
      <v-container fill-height>
        <v-layout align-center justify-center>
          <v-flex>
            <div class="text-center">
              <div class="headline my-5">Loading Kava Bar...</div>
              <v-progress-circular size="100" indeterminate color="primary"></v-progress-circular>
            </div>
          </v-flex>
        </v-layout>
      </v-container>
    </div>
    <div v-else>
      <v-container>
        <v-row>
          <v-col sm="4" cols="12">
            <v-card class="mb-3">
              <v-card-title>
                <v-avatar
                  v-if="nakamalProfile"
                  size="164"
                  class="mx-auto mb-3"
                  @click="tab = 'images'"
                >
                  <v-img
                    :src="nakamalProfile.thumbnail"
                  ></v-img>
                </v-avatar>
                <h1 class="mx-auto" v-text="nakamal.name"></h1>
              </v-card-title>
              <v-card-text class="px-3 pb-3">
                <v-alert
                  v-show="hasRecentCheckin"
                  outlined
                  icon="mdi-marker-check"
                  border="left"
                  class="ma-0 py-2"
                >
                  Has recent check-ins.
                </v-alert>
              </v-card-text>
              <v-card-actions v-show="hasAdminAccess">
                <v-btn
                  text
                  color="secondary lighten-2"
                  :to="{ name: 'NakamalEdit', params: { id: nakamal.id } }"
                >Edit</v-btn>
                <v-btn
                  text
                  color="secondary lighten-2"
                  @click="remove"
                >Delete</v-btn>
              </v-card-actions>
            </v-card>
            <CardChief :nakamal="nakamal"></CardChief>
            <v-list
              dense
              class="elevation-2"
            >
              <v-list-item-group
                color="primary"
              >
                <v-list-item @click="$router.push({ name: 'Map' })">
                  <v-list-item-icon>
                    <v-icon>mdi-map</v-icon>
                  </v-list-item-icon>
                  <v-list-item-content>
                    <v-list-item-title>View on map</v-list-item-title>
                  </v-list-item-content>
                </v-list-item>
                <v-list-item @click="onShare">
                  <v-list-item-icon>
                    <v-icon>mdi-share-variant</v-icon>
                  </v-list-item-icon>
                  <v-list-item-content>
                    <v-list-item-title>Share</v-list-item-title>
                  </v-list-item-content>
                </v-list-item>
              </v-list-item-group>
            </v-list>
          </v-col>
          <v-col sm="8" cols="12">
            <v-card>
              <v-tabs
                v-model="tab"
                color="primary lighten-2"
                background-color="transparent"
                :fixed-tabs="$vuetify.breakpoint.mdAndDown"
              >
                <v-tab href="#details">Details</v-tab>
                <v-tab href="#timeline">Timeline</v-tab>
                <v-tab href="#images">Images</v-tab>
              </v-tabs>

              <v-card-text>
                <v-tabs-items v-if="!loading" v-model="tab">
                  <v-tab-item value="details">
                    <TabDetails :nakamal="nakamal"></TabDetails>
                  </v-tab-item>
                  <v-tab-item value="timeline">
                    <TabTimeline :nakamal="nakamal"/>
                  </v-tab-item>
                  <v-tab-item value="images">
                    <TabImages :nakamal="nakamal"/>
                  </v-tab-item>
                </v-tabs-items>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>
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

    <v-dialog max-width="500" v-model="checkinDialog">
      <v-card>
        <v-card-title class="text-h5">
          Check-In
        </v-card-title>

        <v-card-text>
          <v-textarea
            filled
            counter
            maxlength="280"
            label="Message"
            rows="3"
            row-height="30"
            v-model="checkinMsg"
          ></v-textarea>
        </v-card-text>

        <v-divider></v-divider>

        <v-card-actions>
          <v-btn
            text
            @click="checkinDialog = false"
          >
            Close
          </v-btn>
          <v-spacer></v-spacer>
          <v-btn
            color="primary"
            text
            @click="submitCheckin"
          >
            Submit
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <NakamalImageUpload
      v-if="!loading"
      :nakamal="nakamal"
      :open="uploadImageDialog"
      @close-modal="() => this.uploadImageDialog = false"
    ></NakamalImageUpload>
  </div>
</template>

<script>
import { mapActions, mapGetters } from 'vuex';
import NakamalImageUpload from '@/components/NakamalProfile/NakamalImageUpload.vue';
import TabDetails from '@/components/NakamalProfile/TabDetails.vue';
import TabTimeline from '@/components/NakamalProfile/TabTimeline.vue';
import TabImages from '@/components/NakamalProfile/TabImages.vue';
import CardChief from '@/components/NakamalProfile/CardChief.vue';

export default {
  name: 'Nakamal',
  metaInfo() {
    return {
      title: this.nakamal ? this.nakamal.name : undefined,
      titleTemplate: 'Bilolok - %s',
      meta: [
        {
          property: 'og:title',
          content: this.nakamal ? this.nakamal.name : undefined,
          // following template options are identical
          // template: '%s - My page',
          template: (chunk) => `Bilolok - ${chunk}`,
          vmid: 'og:title',
        },
        {
          property: 'og:image',
          content: this.nakamalProfile ? this.nakamalProfile.src : undefined,
          vmid: 'og:image',
        },
        {
          property: 'og:image:type',
          content: this.nakamalProfile ? 'image/jpeg' : undefined,
          vmid: 'og:image:type',
        },
        {
          property: 'og:image:width',
          content: this.nakamalProfile ? '1280' : undefined,
          vmid: 'og:image:width',
        },
        {
          property: 'og:image:height',
          content: this.nakamalProfile ? '720' : undefined,
          vmid: 'og:image:height',
        },
      ],
    };
  },
  components: {
    NakamalImageUpload,
    TabDetails,
    TabTimeline,
    TabImages,
    CardChief,
  },
  data() {
    return {
      loading: true,
      tab: 'details',
      uploadImageDialog: false,
      checkinDialog: false,
      checkinMsg: null,
    };
  },
  computed: {
    ...mapGetters({
      darkMode: 'setting/darkMode',
      hasAdminAccess: 'auth/hasAdminAccess',
      isUserVerified: 'auth/isUserVerified',
      nakamal: 'nakamal/selected',
      getImages: 'image/nakamal',
      getCheckins: 'checkin/nakamal',
      recentNakamalIds: 'checkin/recentNakamalIds',
    }),
    nakamalProfile() {
      if (!this.nakamal) return null;
      return this.$store.getters['image/nakamalProfile'](this.nakamal.id);
    },
    hasRecentCheckin() {
      if (!this.nakamal) return false;
      return this.recentNakamalIds.includes(this.nakamal.id);
    },
    // loading() {
    //   return !this.nakamal;
    // },
    // images() {
    //   if (this.loading) return [];
    //   return this.getImages(this.nakamal.id)
    //     .sort((a, b) => (dayjs(a.created_at).isAfter(dayjs(b.created_at)) ? -1 : 1));
    // },
    // imageCount() {
    //   if (!this.images.length) return '0';
    //   return this.images.length;
    // },
    // checkins() {
    //   if (this.loading) return [];
    //   return this.getCheckins(this.nakamal.id)
    //     .sort((a, b) => (dayjs(a.created_at).isAfter(dayjs(b.created_at)) ? -1 : 1));
    // },
    activeFab() {
      switch (this.tab) {
        case 'details': return { color: 'secondary', icon: 'mdi-marker-check', action: () => this.toggleCheckinDialog() };
        case 'timeline': return { color: 'secondary', icon: 'mdi-marker-check', action: () => this.toggleCheckinDialog() };
        case 'images': return { color: 'red', icon: 'mdi-image-plus', action: () => this.toggleUploadImageDialog() };
        default: return {};
      }
    },
  },
  methods: {
    ...mapActions({
      checkin: 'checkin/add',
    }),
    toggleUploadImageDialog() {
      if (this.isUserVerified) {
        this.uploadImageDialog = !this.uploadImageDialog;
      } else {
        this.$store.dispatch('auth/setShowUserVerifiedModal', true);
      }
    },
    toggleCheckinDialog() {
      if (this.isUserVerified) {
        this.checkinDialog = !this.checkinDialog;
      } else {
        this.$store.dispatch('auth/setShowUserVerifiedModal', true);
      }
    },
    async onShare() {
      const text = `Check out ${this.nakamal.name} on Bilolok!`;
      const url = document.querySelector('link[rel=canonical]')
        ? document.querySelector('link[rel=canonical]').href
        : document.location.href;
      if (navigator.share) {
        const { title } = document;
        navigator.share({
          url,
          title,
          text,
        }).then(() => {
          this.$store.dispatch('notify/add', {
            title: 'Thanks For Sharing!',
            text: 'We appreciate you letting others know about Bilolok.',
            type: 'primary',
          });
        });
      } else {
        if (!navigator.clipboard) {
          await this.$store.dispatch('notify/add', {
            title: 'Share Not Available',
            text: 'Your device does not support sharing.',
            type: 'error',
          });
          return;
        }
        await navigator.clipboard.writeText(`${text} ${url}`);
        await this.$store.dispatch('notify/add', {
          title: 'Copied to Clipboard!',
          text: 'We appreciate you letting others know about Bilolok.',
          type: 'primary',
        });
      }
    },
    submitCheckin() {
      this.checkinDialog = false;
      this.checkin({ nakamal_id: this.nakamal.id, message: this.checkinMsg });
    },
    remove() {
      /* eslint-disable no-alert, no-restricted-globals */
      if (confirm('Are you sure you want to remove this nakamal?')) {
        this.$store.dispatch('nakamal/remove', this.nakamal.id)
          .then(() => {
            this.$router.push({ name: 'Home' });
          });
      }
    },
  },
  async mounted() {
    const { id } = this.$route.params;
    await this.$store.dispatch('image/getNakamal', id);
    this.$store.dispatch('checkin/getNakamal', id);
    await this.$store.dispatch('nakamal/select', id)
      .then(() => {
        if (!this.nakamal) {
          this.$store.dispatch('nakamal/loadOne', id);
        }
      })
      .then(() => { this.loading = false; });
  },
};
</script>

<style>

</style>
