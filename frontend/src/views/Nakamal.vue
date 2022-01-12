<template>
  <div class="nakamal">
    <div v-if="loading">
      Loading...
    </div>
    <div v-else>
      <v-container>
        <v-card class="">
          <div class="pt-3 px-3 d-md-flex pa-sm-4 text-center text-md-start">
            <div v-if="nakamalProfile" >
              <v-badge
                v-if="hasRecentCheckin"
                avatar
                bordered
                :color="darkMode ? 'black' : 'primary darken-2'"
                overlap
                offset-x="45"
                offset-y="45"
              >
                <template v-slot:badge>
                  <v-avatar size="32" icon>
                    <v-icon>mdi-marker-check</v-icon>
                  </v-avatar>
                </template>
                <v-avatar class="ma-3" size="164">
                  <v-img
                    :src="nakamalProfile.thumbnail"
                  ></v-img>
                </v-avatar>
              </v-badge>
              <v-avatar class="ma-3" size="164" v-else>
                <v-img
                  :src="nakamalProfile.thumbnail"
                ></v-img>
              </v-avatar>
            </div>

            <h1 class="align-self-start">{{ nakamal.name }}</h1>
          </div>
          <v-card-actions>
            <v-btn
              v-show="hasAdminAccess"
              text
              color="secondary lighten-2"
              :to="{ name: 'NakamalEdit', params: { id: nakamal.id } }"
            >
              Edit
            </v-btn>
            <v-btn
              v-show="hasAdminAccess"
              text
              color="secondary lighten-2"
              @click="remove"
            >
              Remove
            </v-btn>
          </v-card-actions>

          <v-tabs
            v-model="tab"
            :fixed-tabs="$vuetify.breakpoint.mdAndDown"
            color="primary lighten-2"
            background-color="transparent"
          >
            <v-tab href="#details">Details</v-tab>
            <v-tab href="#timeline">Timeline</v-tab>
            <v-tab href="#images">Images</v-tab>
          </v-tabs>
        </v-card>
      </v-container>

      <v-tabs-items v-if="!loading" v-model="tab">
        <v-tab-item value="details">
          <TabDetails :nakamal="nakamal"/>
        </v-tab-item>
        <v-tab-item value="timeline">
          <TabTimeline :nakamal="nakamal"/>
        </v-tab-item>
        <v-tab-item value="images">
          <TabImages :nakamal="nakamal"/>
        </v-tab-item>
      </v-tabs-items>
    </div>

    <v-btn
      fixed
      fab
      small
      dark
      bottom
      left
      color="primary"
      @click="$router.push({ name: 'Map' })"
    >
      <v-icon>mdi-map</v-icon>
    </v-btn>

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

export default {
  name: 'Nakamal',
  components: {
    NakamalImageUpload,
    TabDetails,
    TabTimeline,
    TabImages,
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
