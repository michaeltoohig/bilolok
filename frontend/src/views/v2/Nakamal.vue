<template>
  <v-container>
    <v-row>
      <v-col sm="4" cols="12">
        <ProfileCard :nakamal="nakamal" :profile="nakamalProfile" />
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
            <v-tabs-items v-model="tab">
              <v-tab-item value="details">
                <TabDetails :nakamal="nakamal"></TabDetails>
              </v-tab-item>
              <v-tab-item value="timeline">
                <Timeline 
                  :nakamal="nakamal"
                  @select-checkin="() => this.showCheckinDialog = true" 
                  @select-image="() => this.showUploadImageDialog = true"
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

    <DialogCheckin
      :nakamal="nakamal"
      :open="showCheckinDialog"
      @close-modal="() => this.showCheckinDialog = false"
    ></DialogCheckin>

    <NakamalImageUpload
      :nakamal="nakamal"
      :open="showUploadImageDialog"
      @close-modal="() => this.showUploadImageDialog = false"
    ></NakamalImageUpload>

    <VideoUploadDialog
      :nakamal="nakamal"
      :open="showUploadVideoDialog"
      @close-modal="() => this.showUploadVideoDialog = false"
    ></VideoUploadDialog>
  </v-container>
</template>

<script>
// TODO review each Dialog and ensuring they update the appropriate store when pictures upload for example the nakamal profile should be set and images list should be updated
import { mapActions, mapGetters } from 'vuex';
import ProfileCard from '@/components/nakamal/v2/ProfileCard.vue';
import NakamalImageUpload from '@/components/nakamal/NakamalImageUpload.vue';
import DialogCheckin from '@/components/nakamal/DialogCheckin.vue';
import TabDetails from '@/components/nakamal/TabDetails.vue';
import Timeline from '@/components/nakamal/v2/Timeline.vue';
import TabImages from '@/components/nakamal/TabImages.vue';
import CardChief from '@/components/nakamal/CardChief.vue';
import VideoUploadDialog from '@/components/nakamal/VideoUploadDialog.vue';

export default {
  name: 'Nakamal2',
  // props: {
  //   nakamal: {
  //     type: Object,
  //     required: true,
  //   },
  // },
  components: {
    ProfileCard,
    VideoUploadDialog,
    DialogCheckin,
    NakamalImageUpload,
    TabDetails,
    Timeline,
    TabImages,
    CardChief,
  },
  data() {
    return {
      // nakamalProfile: null,
      // temp fake data
      // loading: true,
      isFeatured: true, // TODO
      tab: 'timeline',
      showCheckinDialog: false,
      showUploadImageDialog: false,
      showUploadVideoDialog: false,
    };
  },
  computed: {
    ...mapGetters({
      nakamal: 'nakamal2/selected',
      image: 'image2/get',

      isUserVerified: 'auth/isUserVerified',
    }),
    nakamalProfile() {
      return this.image(this.nakamal.profile);
    },
  },
  methods: {
    toggleCheckinDialog() {
      if (this.isUserVerified) {
        this.showCheckinDialog = !this.showCheckinDialog;
      } else {
        this.$store.dispatch('auth/setShowUserVerifiedModal', true);
      }
    },
    toggleUploadImageDialog() {
      if (this.isUserVerified) {
        this.showUploadImageDialog = !this.showUploadImageDialog;
      } else {
        this.$store.dispatch('auth/setShowUserVerifiedModal', true);
      }
    },
  },
  // mounted() {
  //   this.loading = false;
  // },
};
</script>
