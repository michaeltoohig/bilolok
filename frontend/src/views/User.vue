<template>
  <div class="user">
    <div v-if="loading">
      <v-container fill-height>
        <v-layout align-center justify-center>
          <v-flex>
            <div class="text-center">
              <div class="headline my-5">{{ $t('loading.user') }}</div>
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
                  color="dark"
                  size="144"
                  tile
                  class="mx-auto elevation-2"
                >
                  <v-img :src="user.avatar"></v-img>
                </v-avatar>
              </v-card-title>
              <v-list dense>
                <v-list-item-group color="primary">
                  <v-list-item v-if="isMe" @click="changeProfilePicture">
                    <v-list-item-icon>
                      <v-icon>mdi-camera-plus</v-icon>
                    </v-list-item-icon>
                    <v-list-item-content>
                      <v-list-item-title>{{ $t('user.change_profile_image') }}</v-list-item-title>
                    </v-list-item-content>
                  </v-list-item>
                  <v-list-item v-if="isMe && !isDefaultProfile" @click="removeUserProfile">
                    <v-list-item-icon>
                      <v-icon>mdi-camera-off</v-icon>
                    </v-list-item-icon>
                    <v-list-item-content>
                      <v-list-item-title>{{ $t('user.remove_profile_image') }}</v-list-item-title>
                    </v-list-item-content>
                  </v-list-item>
                  <v-list-item @click="onShare">
                    <v-list-item-icon>
                      <v-icon>mdi-share-variant</v-icon>
                    </v-list-item-icon>
                    <v-list-item-content>
                      <v-list-item-title>{{ $t('buttons.share') }}</v-list-item-title>
                    </v-list-item-content>
                  </v-list-item>
                </v-list-item-group>
              </v-list>
            </v-card>

            <v-list
              v-if="chiefOf.length > 0"
              color="secondary darken-2"
              dark
              subheader
              class="elevation-3 mb-3"
            >
              <v-subheader>
                {{ $tc('user.chief_of', chiefOf.length, { count: chiefOf.length }) }}
              </v-subheader>
              <v-list-item
                :to="{ name: 'Nakamal', params: { id: nakamal.id } }"
                v-for="(nakamal, i) in chiefOf"
                :key="nakamal.id"
              >
                <v-list-item-content>
                  <v-list-item-title v-if="i === 0">{{ nakamal.name }}</v-list-item-title>
                  <v-list-item-title v-else class="font-weight-light">
                    {{ nakamal.name }}
                  </v-list-item-title>
                </v-list-item-content>
                <v-list-item-avatar
                  v-if="nakamalAvatar(nakamal.id)"
                >
                  <v-img
                    :src="nakamalAvatar(nakamal.id).thumbnail"
                  ></v-img>
                </v-list-item-avatar>
              </v-list-item>
            </v-list>

            <v-list subheader class="elevation-3 mb-3">
              <v-subheader>{{ $t('user.favorite_nakamals') }}</v-subheader>
              <v-list-item v-if="topNakamalsByCheckins.length === 0">
                <v-list-item-icon class="mr-3">
                  <v-icon>mdi-emoticon-sad-outline</v-icon>
                </v-list-item-icon>
                <v-list-item-content>
                  <v-list-item-title>{{ $t('user.favorite_nakamals_none') }}</v-list-item-title>
                </v-list-item-content>
              </v-list-item>
              <v-list-item
                :to="{ name: 'Nakamal', params: { id: item.nakamal.id } }"
                v-for="(item, i) in topNakamalsByCheckins"
                :key="item.nakamal.id"
              >
                <v-list-item-action class="mr-0">{{ i + 1 }}</v-list-item-action>
                <v-list-item-content>
                  <v-list-item-title v-if="i === 0">{{ item.nakamal.name }}</v-list-item-title>
                  <v-list-item-title v-else class="font-weight-light">
                    {{ item.nakamal.name }}
                  </v-list-item-title>
                  <v-list-item-subtitle>
                    {{ $t('checkin.title') }}: {{ item.count }}
                  </v-list-item-subtitle>
                </v-list-item-content>
                <v-list-item-avatar
                  v-if="nakamalAvatar(item.nakamal.id)"
                >
                  <v-img
                    :src="nakamalAvatar(item.nakamal.id).thumbnail"
                  ></v-img>
                </v-list-item-avatar>
              </v-list-item>
            </v-list>

            <PushNotificationCard v-if="isMe"></PushNotificationCard>
          </v-col>
          <v-col sm="8" cols="12">
            <v-alert
              v-if="isMe && !isUserVerified"
              class="mb-3"
              type="info"
              prominent
              text
            >
              <h3 class="text-h5">
                {{ $t('auth.email_not_verified_title') }}
              </h3>
              <div>
                {{ $t('auth.email_not_verified_body') }}
              </div>
              <v-divider
                class="my-4 info"
                style="opacity: 0.22"
              ></v-divider>
              <div>
                <v-btn
                  color="info"
                  @click="sendVerificationEmail"
                >
                  {{ $t('auth.send_verification_email') }}
                </v-btn>
              </div>
            </v-alert>
            <div
              v-for="item in timelineItems"
              :key="item.data.id"
            >
              <CheckinTimelineCard
                v-if="item.type === 'checkin'"
                :item="item.data"
                :linkNakamal="true"
              />
              <ImageTimelineCard
                v-if="item.type === 'image'"
                :item="item.data"
                :linkNakamal="true"
              />
              <TripTimelineCard
                v-if="item.type === 'trip'"
                :item="item.data"
                :linkNakamal="true"
              />
              <VideoTimelineCard
                v-if="item.type === 'video'"
                :item="item.data"
                :linkNakamal="true"
              />
            </div>
            <div v-if="timelineItems.length === 0">
              <v-alert
                class="mb-3"
                type="warning"
                prominent
                text
              >
                <h3 class="text-h5">
                  {{ $t('user.no_activity_title') }}
                </h3>
                <div v-if="isMe">
                  {{ $t('user.no_activity_private_body') }}
                </div>
                <div v-else>
                  {{ $t('user.no_activity_public_body') }}
                </div>
              </v-alert>
            </div>
          </v-col>
        </v-row>
      </v-container>

      <UserVideoUpload v-if="isMe"></UserVideoUpload>
    </div>

    <ProfileImageUpload
      v-if="!loading"
      :open="uploadImageDialog"
      @close-modal="closeUploadDialog"
    ></ProfileImageUpload>
  </div>
</template>

<script>
import dayjs from 'dayjs';
import { mapGetters } from 'vuex';
import formatDatetime from '@/mixins/formatDatetime';
import PushNotificationCard from '@/components/user/PushNotificationCard.vue';
import ProfileImageUpload from '@/components/user/ProfileImageUpload.vue';
import UserVideoUpload from '@/components/user/UserVideoUpload.vue';

import CheckinTimelineCard from '@/components/timeline/CheckinTimelineCard.vue';
import ImageTimelineCard from '@/components/timeline/ImageTimelineCard.vue';
import TripTimelineCard from '@/components/timeline/TripTimelineCard.vue';
import VideoTimelineCard from '@/components/timeline/VideoTimelineCard.vue';

export default {
  name: 'User',
  mixins: [formatDatetime],
  components: {
    PushNotificationCard,
    ProfileImageUpload,
    UserVideoUpload,

    CheckinTimelineCard,
    ImageTimelineCard,
    TripTimelineCard,
    VideoTimelineCard,
  },
  data() {
    return {
      loading: true,
      notificationsSupported: false,
      uploadImageDialog: false,
    };
  },
  computed: {
    user() {
      const { id } = this.$route.params;
      return this.$store.getters['user/find'](id);
    },
    isMe() {
      if (!this.isLoggedIn) return false;
      return this.me.id === this.user.id;
    },
    isDefaultProfile() {
      // XXX hardcoded value
      return this.user.avatar.endsWith('default.png');
    },
    ...mapGetters({
      isLoggedIn: 'auth/isLoggedIn',
      me: 'auth/user',
      token: 'auth/token',
      isUserVerified: 'auth/isUserVerified',
      hasAdminAccess: 'auth/hasAdminAccess',
      getUserCheckins: 'checkin/user',
      getUserImages: 'image/user',
      getUserTrips: 'trip/user',
      getUserVideos: 'video/user',
      getNakamalImages: 'image/nakamal',
      getChiefOf: 'nakamal/listByChief',
    }),
    checkins() {
      const { id } = this.user;
      return this.getUserCheckins(id);
    },
    images() {
      const { id } = this.user;
      return this.getUserImages(id);
    },
    trips() {
      const { id } = this.user;
      return this.getUserTrips(id);
    },
    videos() {
      const { id } = this.user;
      return this.getUserVideos(id);
    },
    timelineItems() {
      let items = this.checkins.map((i) => ({ type: 'checkin', data: i }));
      items = items.concat(this.images.map((i) => ({ type: 'image', data: i })));
      items = items.concat(this.trips.map((i) => ({ type: 'trip', data: i })));
      items = items.concat(this.videos.map((i) => ({ type: 'video', data: i })));
      return items.sort((a, b) => (dayjs(b.data.created_at).isAfter(a.data.created_at) ? 1 : -1));
    },
    chiefOf() {
      return this.getChiefOf(this.$route.params.id);
    },
    topNakamalsByCheckins() {
      if (!this.checkins) return null;
      const count = {};
      let checkins = [...this.checkins];
      if (!this.isMe) {
        checkins = checkins.filter((c) => !c.private);
      }
      const threshold = dayjs().subtract(30, 'd');
      checkins = checkins.filter((c) => threshold.isBefore(dayjs(c.created_at)));
      checkins.forEach((c) => {
        const nId = c.nakamal.id;
        if (Object.keys(count).includes(nId)) {
          count[nId].count += 1;
          if (dayjs(count[nId].created_at).isBefore(c.created_at)) {
            count[nId].created_at = c.created_at;
          }
        } else {
          count[nId] = {
            count: 1,
            created_at: c.created_at,
            nakamal: c.nakamal,
          };
        }
      });
      const sorted = Object.values(count).sort((a, b) => {
        if (a.count === b.count) {
          return dayjs(b.created_at).isBefore(dayjs(a.created_at)) ? -1 : 1;
        }
        return a.count > b.count ? -1 : 1;
      });
      return sorted.slice(0, 3);
    },
  },
  watch: {
    $route: 'fetchData',
  },
  methods: {
    async sendVerificationEmail() {
      this.$store.dispatch('auth/requestVerification');
    },
    async fetchData() {
      this.loading = true;
      const { id } = this.$route.params;
      await this.$store.dispatch('checkin/getUser', id);
      await this.$store.dispatch('image/getUser', id);
      await this.$store.dispatch('trip/getUser', id);
      await this.$store.dispatch('video/getUser', id);
      // await this.$store.dispatch('chief/getUser', id);
      this.loading = false;
    },
    async changeProfilePicture() {
      if (this.isUserVerified) {
        this.uploadImageDialog = true;
      } else {
        this.$store.dispatch('auth/setShowUserVerifiedModal', true);
      }
    },
    async removeUserProfile() {
      /* eslint-disable no-alert, no-restricted-globals */
      if (confirm(this.$i18n.t('user.remove_profile_image_confirm'))) {
        await this.$store.dispatch('user/removeProfile');
      }
    },
    async closeUploadDialog() {
      this.uploadImageDialog = false;
      setTimeout(() => {
        this.fetchData();
      }, 500);
    },
    nakamalAvatar(nakamalId) {
      const images = this.getNakamalImages(nakamalId);
      if (images.length > 0) {
        return images[0];
      }
      return null;
    },
    // removeImage() {
    //   /* eslint-disable no-alert, no-restricted-globals */
    //   if (confirm('Are you sure you want to remove this image?')) {
    //     this.$store.dispatch('image/remove', this.selectedImageId);
    //   }
    // },
    async onShare() {
      let text;
      if (this.isMe) {
        text = 'Check out my profile on Bilolok!';
      } else {
        text = 'Check out this user on Bilolok!';
      }
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
  },
  async mounted() {
    const { id } = this.$route.params;
    await this.$store.dispatch('user/getOne', id);
    await this.fetchData();
  },
};
</script>

<style>

</style>
