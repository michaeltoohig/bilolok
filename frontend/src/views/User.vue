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

            <CardChiefOf :userId="user.id"></CardChiefOf>

            <CardFavoriteNakamals :userId="user.id"></CardFavoriteNakamals>

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
            <SectionTimeline :userId="user.id"></SectionTimeline>
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
import { mapGetters } from 'vuex';
import formatDatetime from '@/mixins/formatDatetime';
import PushNotificationCard from '@/components/user/PushNotificationCard.vue';
import ProfileImageUpload from '@/components/user/ProfileImageUpload.vue';
import UserVideoUpload from '@/components/user/UserVideoUpload.vue';
import CardChiefOf from '@/components/user/CardChiefOf.vue';
import CardFavoriteNakamals from '@/components/user/CardFavoriteNakamals.vue';
import SectionTimeline from '@/components/user/SectionTimeline.vue';

export default {
  name: 'User',
  mixins: [formatDatetime],
  components: {
    PushNotificationCard,
    ProfileImageUpload,
    UserVideoUpload,
    CardChiefOf,
    CardFavoriteNakamals,
    SectionTimeline,
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
      if (!this.user || !this.isLoggedIn) return false;
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
    }),
  },
  watch: {
    $route: 'fetchData',
  },
  methods: {
    async fetchData(userId) {
      await Promise.all([
        this.$store.dispatch('checkin/getUser', userId),
        this.$store.dispatch('image/getUser', userId),
        this.$store.dispatch('trip/getUser', userId),
        this.$store.dispatch('video/getUser', userId),
      ]);
    },
    async sendVerificationEmail() {
      this.$store.dispatch('auth/requestVerification');
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
    this.loading = true;
    const { id } = this.$route.params;
    await this.$store.dispatch('user/loadOne', id);
    // Load data here so it is available for sub-components
    await this.fetchData(id);
    this.loading = false;
  },
};
</script>

<style>

</style>
