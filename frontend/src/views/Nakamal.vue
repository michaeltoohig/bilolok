<template>
  <div class="nakamal">
    <div v-if="loading">
      <v-container fill-height>
        <v-layout align-center justify-center>
          <v-flex>
            <div class="text-center">
              <div class="headline my-5">{{ $t('loading.nakamal') }}</div>
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
              <v-card-title class="d-flex flex-column justify-center text-center">
                <v-badge
                  v-if="nakamalProfile"
                  :color="nakamal.lightBadge.color"
                  :icon="nakamal.lightBadge.icon"
                  overlap
                  bordered
                  left
                  offset-x="35"
                  offset-y="25"
                  dark
                >
                  <v-avatar
                    size="164"
                    class="mb-5 nakamal-avatar"
                    v-ripple="{ center: true }"
                    @click="goToTabImages"
                  >
                    <v-img
                      :src="nakamalProfile.thumbnail"
                    ></v-img>
                  </v-avatar>
                </v-badge>
                <h1 v-text="nakamal.name"></h1>
              </v-card-title>
              <v-card-text class="px-3 pb-3">
                <v-alert
                  v-show="isFeatured"
                  color="accent"
                  outlined
                  icon="mdi-trophy-award"
                  border="left"
                  class="mx-0 mt-0 mb-1 py-2"
                >
                  {{ $t('nakamal.is_featured') }}
                </v-alert>
                <v-alert
                  v-show="hasRecentCheckin"
                  outlined
                  icon="mdi-marker-check"
                  border="left"
                  class="mx-0 mt-0 mb-1 py-2"
                >
                  {{ $t('nakamal.has_recent_checkins') }}
                </v-alert>
              </v-card-text>
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
                    <v-list-item-title>{{ $t('nakamal.view_on_map') }}</v-list-item-title>
                  </v-list-item-content>
                </v-list-item>
                <v-list-item :disabled="isFeatured" @click="setFeatured(nakamal.id)">
                  <v-list-item-icon>
                    <v-icon>mdi-trophy-award</v-icon>
                  </v-list-item-icon>
                  <v-list-item-content>
                    <v-list-item-title>{{ $t('nakamal.set_featured') }}</v-list-item-title>
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
                <v-spacer v-show="isUserVerified"></v-spacer>
                <v-list-item color="primary lighten-2" v-show="isUserVerified" @click="onEdit">
                  <v-list-item-icon>
                    <v-icon>mdi-pencil</v-icon>
                  </v-list-item-icon>
                  <v-list-item-content>
                    <v-list-item-title>{{ $t('buttons.edit') }}</v-list-item-title>
                  </v-list-item-content>
                </v-list-item>
                <v-list-item color="primary lighten-2" v-show="hasAdminAccess" @click="onRemove">
                  <v-list-item-icon>
                    <v-icon>mdi-trash-can-outline</v-icon>
                  </v-list-item-icon>
                  <v-list-item-content>
                    <v-list-item-title>{{ $t('buttons.delete') }}</v-list-item-title>
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
                <v-tab href="#details">{{ $t('nakamal.tab_details') }}</v-tab>
                <v-tab href="#timeline">{{ $t('nakamal.tab_timeline') }}</v-tab>
                <v-tab href="#images">{{ $t('nakamal.tab_images') }}</v-tab>
              </v-tabs>

              <v-card-text id="tab-content">
                <v-tabs-items v-if="!loading" v-model="tab">
                  <v-tab-item value="details">
                    <TabDetails :nakamal="nakamal"></TabDetails>
                  </v-tab-item>
                  <v-tab-item value="timeline">
                    <TabTimeline
                      :nakamal="nakamal"
                      @select-checkin="() => this.showCheckinDialog = true"
                      @select-video="() => this.showUploadVideoDialog = true"
                    />
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

    <DialogCheckin
      v-if="!loading"
      :nakamal="nakamal"
      :open="showCheckinDialog"
      @close-modal="() => this.showCheckinDialog = false"
    ></DialogCheckin>

    <NakamalImageUpload
      v-if="!loading"
      :nakamal="nakamal"
      :open="showUploadImageDialog"
      @close-modal="() => this.showUploadImageDialog = false"
    ></NakamalImageUpload>

    <VideoUploadDialog
      v-if="!loading"
      :nakamal="nakamal"
      :open="showUploadVideoDialog"
      @close-modal="() => this.showUploadVideoDialog = false"
    ></VideoUploadDialog>
  </div>
</template>

<script>
import { mapActions, mapGetters } from 'vuex';
import NakamalImageUpload from '@/components/nakamal/NakamalImageUpload.vue';
import DialogCheckin from '@/components/nakamal/DialogCheckin.vue';
import TabDetails from '@/components/nakamal/TabDetails.vue';
import TabTimeline from '@/components/nakamal/TabTimeline.vue';
import TabImages from '@/components/nakamal/TabImages.vue';
import CardChief from '@/components/nakamal/CardChief.vue';
import VideoUploadDialog from '@/components/nakamal/VideoUploadDialog.vue';

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
    VideoUploadDialog,
    DialogCheckin,
    NakamalImageUpload,
    TabDetails,
    TabTimeline,
    TabImages,
    CardChief,
  },
  data() {
    return {
      loading: true,
      tab: 'timeline',
      showUploadVideoDialog: false,
      showUploadImageDialog: false,
      showCheckinDialog: false,
    };
  },
  computed: {
    ...mapGetters({
      darkMode: 'setting/darkMode',
      hasAdminAccess: 'auth/hasAdminAccess',
      isUserVerified: 'auth/isUserVerified',
      nakamal: 'nakamal/selected',
      featured: 'nakamal/featured',
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
    isFeatured() {
      if (!this.nakamal || !this.featured) return false;
      return this.nakamal.id === this.featured.id;
    },
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
      setFeatured: 'nakamal/setFeatured',
    }),
    goToTabImages() {
      this.tab = 'images';
      setTimeout(() => {
        this.$vuetify.goTo('#tab-content');
      }, 200);
    },
    toggleUploadImageDialog() {
      if (this.isUserVerified) {
        this.showUploadImageDialog = !this.showUploadImageDialog;
      } else {
        this.$store.dispatch('auth/setShowUserVerifiedModal', true);
      }
    },
    toggleCheckinDialog() {
      if (this.isUserVerified) {
        this.showCheckinDialog = !this.showCheckinDialog;
      } else {
        this.$store.dispatch('auth/setShowUserVerifiedModal', true);
      }
    },
    onEdit() {
      this.$router.push({ name: 'NakamalEdit', params: { id: this.nakamal.id } });
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
    onRemove() {
      /* eslint-disable no-alert, no-restricted-globals */
      if (confirm(this.$i18n.t('nakamal.confirm_delete'))) {
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
    await this.$store.dispatch('checkin/getNakamal', id);
    await this.$store.dispatch('video/getNakamal', id);
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
.nakamal-avatar {
  cursor: pointer;
}
</style>
