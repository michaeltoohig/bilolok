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
        <v-card-text v-if="checkinsCountHighestUser">
          <h4>
            Current Chief
            <v-tooltip bottom>
              <template v-slot:activator="{ on, attrs }">
                <v-icon
                  color="primary"
                  v-bind="attrs"
                  v-on="on"
                >
                  mdi-information
                </v-icon>
              </template>
              <v-responsive max-width="170">
                <span>The chief is the user who has the most check-ins in the last 30 days.</span>
              </v-responsive>
            </v-tooltip>
          </h4>
          <v-avatar
            tile
            class="elevation-2"
            @click="$router.push({ name: 'User', params: { id: checkinsCountHighestUser.id } })"
          >
            <v-img
              :src="checkinsCountHighestUser.avatar"
            ></v-img>
          </v-avatar>
        </v-card-text>

        <v-card-actions>
          <v-btn
            v-show="hasAdminAccess"
            text
            color="primary"
            :to="{ name: 'NakamalEdit', params: { id: nakamal.id } }"
          >
            Edit
          </v-btn>
          <v-btn
            v-show="hasAdminAccess"
            text
            color="error"
            @click="remove"
          >
            Remove
          </v-btn>
        </v-card-actions>

        <v-tabs
          v-model="tab"
          background-color="transparent"
        >
          <v-tab href="#timeline">Timeline</v-tab>
          <v-tab href="#images">
            <v-badge
              color="green"
              :content="imageCount"
            >
             Images
            </v-badge>
          </v-tab>
        </v-tabs>
      </v-card>

      <v-container>
        <v-tabs-items v-model="tab">
          <v-tab-item value="timeline">
            <v-container>
              <v-row>
                <v-col cols="12" lg="3" md="5">
                  <v-card
                    tile
                    class="mx-auto"
                    max-width="300"
                  >
                    <v-list>
                      <v-subheader>
                        Details
                        <v-spacer></v-spacer>
                        <v-btn
                          icon
                          @click="expandDetails = !expandDetails"
                        >
                          <v-icon>
                            {{ expandDetails ? 'mdi-chevron-up' : 'mdi-chevron-down' }}
                          </v-icon>
                        </v-btn>
                      </v-subheader>
                      <v-expand-transition>
                        <v-list-item-group
                          v-show="expandDetails"
                          color="primary"
                        >
                          <v-list-item two-line>
                            <v-list-item-content>
                              <v-list-item-title>Owner</v-list-item-title>
                              <v-list-item-subtitle>{{ nakamal.owner }}</v-list-item-subtitle>
                            </v-list-item-content>
                          </v-list-item>
                          <v-list-item two-line>
                            <v-list-item-content>
                              <v-list-item-title>Number</v-list-item-title>
                              <v-list-item-subtitle>{{ nakamal.phone }}</v-list-item-subtitle>
                            </v-list-item-content>
                          </v-list-item>
                          <v-list-item two-line>
                            <v-list-item-content>
                              <v-list-item-title>Light</v-list-item-title>
                              <v-list-item-subtitle>{{ nakamal.light }}</v-list-item-subtitle>
                            </v-list-item-content>
                          </v-list-item>
                          <v-list-item two-line>
                            <v-list-item-content>
                              <v-list-item-title>Checkins Today</v-list-item-title>
                              <v-list-item-subtitle>{{ checkinsCountToday }}</v-list-item-subtitle>
                            </v-list-item-content>
                          </v-list-item>
                          <v-list-item two-line>
                            <v-list-item-content>
                              <v-list-item-title>Checkins Month</v-list-item-title>
                              <v-list-item-subtitle>{{ checkinsCountMonth }}</v-list-item-subtitle>
                            </v-list-item-content>
                          </v-list-item>
                        </v-list-item-group>
                      </v-expand-transition>
                    </v-list>
                  </v-card>
                </v-col>

                <v-col cols="12" lg="6" md="7">

                  <v-alert
                    v-show="!checkins.length"
                    class="mx-auto elevation-2"
                    color="info"
                    colored-border
                    prominent
                    icon="mdi-marker-check"
                    border="left"
                    max-width="500"
                  >
                    Be first to check-in!
                  </v-alert>
                  <CardCheckin
                    v-for="checkin in checkins"
                    :key="checkin.id"
                    :item="checkin"
                    :linkUser="true"
                  ></CardCheckin>
                </v-col>
              </v-row>
            </v-container>
          </v-tab-item>
          <v-tab-item value="images">
            <v-container class="px-0">
              <v-row v-if="!images.length">
                <v-col>
                  <h2>No Images Yet</h2>
                </v-col>
              </v-row>
              <Photoswipe v-else>
                <v-row>
                  <v-col
                    v-for="(image, i) in images"
                    :key="i"
                    class="d-flex flex-column child-flex"
                    cols="4"
                  >
                    <img
                      :data-image-id="image.id"
                      v-pswp="image"
                      :src="image.thumbnail"
                      :lazy-src="image.msrc"
                      :aspect-ratio="1"
                      @contextmenu="show"
                    />
                  </v-col>
                </v-row>

                <v-menu
                  v-model="showMenu"
                  :position-x="x"
                  :position-y="y"
                  absolute
                  offset-y
                >
                  <v-list>
                    <v-list-item link @click="removeImage">
                      <v-list-item-title>Remove</v-list-item-title>
                    </v-list-item>
                  </v-list>
                </v-menu>
              </Photoswipe>
            </v-container>
          </v-tab-item>
        </v-tabs-items>
      </v-container>
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

    <v-dialog v-model="checkinDialog">
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
      :open="openUploadDialog"
      @close-modal="() => this.openUploadDialog = false"
    ></NakamalImageUpload>
  </div>
</template>

<script>
import { mapActions, mapGetters } from 'vuex';
import dayjs from 'dayjs';
import NakamalImageUpload from '@/components/NakamalProfile/NakamalImageUpload.vue';
import CardCheckin from '@/components/timeline/CardCheckin.vue';

export default {
  name: 'Nakamal',
  components: {
    NakamalImageUpload,
    CardCheckin,
  },
  data() {
    return {
      expandDetails: true,
      tab: 'timeline',
      checkinDialog: false,
      checkinMsg: null,
      openUploadDialog: false,
      x: 0,
      y: 0,
      selectedImageId: null,
      showMenu: false,
    };
  },
  computed: {
    ...mapGetters({
      hasAdminAccess: 'auth/hasAdminAccess',
      nakamal: 'nakamal/selected',
      getImages: 'image/nakamal',
      getCheckins: 'checkin/nakamal',
    }),
    loading() {
      return !this.nakamal;
    },
    images() {
      if (this.loading) return [];
      return this.getImages(this.nakamal.id)
        .sort((a, b) => (dayjs(a.created_at).isAfter(dayjs(b.created_at)) ? -1 : 1));
    },
    imageCount() {
      if (!this.images.length) return '0';
      return this.images.length;
    },
    checkins() {
      if (this.loading) return [];
      return this.getCheckins(this.nakamal.id)
        .sort((a, b) => (dayjs(a.created_at).isAfter(dayjs(b.created_at)) ? -1 : 1));
    },
    checkinsCountToday() {
      if (this.loading) return 0;
      const threshold = dayjs().startOf('d').subtract(1, 'd');
      return this.checkins
        .filter((c) => dayjs(c.created_at).isAfter(threshold))
        .length;
    },
    checkinsCountMonth() {
      if (this.loading) return 0;
      const threshold = dayjs().startOf('d').subtract(30, 'd');
      return this.checkins
        .filter((c) => dayjs(c.created_at).isAfter(threshold))
        .length;
    },
    checkinsCountHighestUser() {
      if (!this.checkins) return null;
      // Limit checkins to last 30 days only
      const threshold = dayjs().startOf('d').subtract(30, 'd');
      const checkins = this.checkins.filter((c) => dayjs(c.created_at).isAfter(threshold));
      if (checkins.length === 0) return null;
      // Setup
      const checkinMap = {};
      let maxEl = checkins[0];
      let maxCount = 1;
      // Find user with most checkins
      for (let i = 0; i < checkins.length; i += 1) {
        const el = checkins[i];
        const userId = el.user.id;
        // Add userId to checkin map if not exists or increment count
        if (!checkinMap[userId]) {
          checkinMap[userId] = {
            count: 1,
            created: el.created_at,
          };
        } else {
          // Increment count and set latest created
          checkinMap[userId].count += 1;
          if (dayjs(maxEl.created_at).isBefore(el.created_at)) {
            checkinMap[userId].created = el.created_at;
          }
        }
        // Determine current user with most check-ins or if a tie then most recent check-in
        if (checkinMap[userId].count > maxCount) {
          maxCount = checkinMap[userId].count;
          maxEl = el;
        } else if (checkinMap[userId].count === maxCount) {
          if (dayjs(el.created_at).isAfter(dayjs(checkinMap[userId].created))) {
            maxEl = el;
          }
        }
      }
      return maxEl.user;
    },
    activeFab() {
      switch (this.tab) {
        case 'timeline': return { color: 'success', icon: 'mdi-marker-check', action: () => { this.checkinDialog = !this.checkinDialog; } };
        case 'images': return { color: 'red', icon: 'mdi-image-plus', action: () => { this.openUploadDialog = !this.openUploadDialog; } };
        default: return {};
      }
    },
  },
  methods: {
    ...mapActions({
      checkin: 'checkin/add',
    }),
    submitCheckin() {
      this.checkin({ nakamal_id: this.nakamal.id, message: this.checkinMsg });
      this.checkinDialog = false;
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
    show(e) {
      e.preventDefault();
      this.showMenu = false;
      this.selectedImageId = e.target.getAttribute('data-image-id');
      this.x = e.clientX;
      this.y = e.clientY;
      this.$nextTick(() => {
        this.showMenu = true;
      });
    },
    removeImage() {
      if (confirm('Are you sure you want to remove this image?')) {
        this.$store.dispatch('image/remove', this.selectedImageId);
      }
    },
  },
  async mounted() {
    const { id } = this.$route.params;
    this.$store.dispatch('checkin/getNakamal', id);
    this.$store.dispatch('image/getNakamal', id);
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
