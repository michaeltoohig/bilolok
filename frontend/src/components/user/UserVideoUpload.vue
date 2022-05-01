<template>
  <div>
    <v-btn
      fab
      color="secondary"
      bottom
      right
      fixed
      @click="toggleUploadVideoDialog"
    >
      <v-icon>mdi-video-plus</v-icon>
    </v-btn>

    <!-- TODO limit video duration for user uploads and process videos into square videos -->
    <v-btn
      v-show="false"
      fab
      color="secondary"
      bottom
      left
      fixed
      @click="openUppy = !openUppy"
    >
      <v-icon>mdi-upload</v-icon>
    </v-btn>

    <DashboardModal
      :uppy="uppy"
      :open="openUppy"
      :plugins="[]"
      :props="{ theme }"
    />

    <v-dialog
      v-model="dialog"
      persistent
      max-width="400px"
    >
      <v-card class="pa-0">
        <v-btn
          id="closeBtn"
          @click="dialog = false"
          small
          outlined
          color="red"
        ><v-icon>mdi-close</v-icon></v-btn>
        <VideoJSRecord :enable="dialog" v-on:recorded-data="addVideoFile" />
        <StatusBar :uppy="uppy" />
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
import { mapGetters } from 'vuex';
import VideoJSRecord from '@/components/VideoJSRecord.vue';
import { DashboardModal, StatusBar } from '@uppy/vue';
import { uploadDomain } from '@/env';

import '@uppy/core/dist/style.css';
import '@uppy/status-bar/dist/style.css';
import '@uppy/dashboard/dist/style.css';

import { Uppy } from '@uppy/core';
import Tus from '@uppy/tus';

export default {
  name: 'UserVideoUpload',
  components: {
    DashboardModal,
    StatusBar,
    VideoJSRecord,
  },
  data() {
    return {
      dialog: false,
      openUppy: false,
    };
  },
  computed: {
    ...mapGetters({
      user: 'auth/user',
      token: 'auth/token',
      isUserVerified: 'auth/isUserVerified',
      darkMode: 'setting/darkMode',
    }),
    theme() {
      return this.darkMode ? 'dark' : 'light';
    },
    uppy() {
      return new Uppy({
        meta: {
          Target: 'USER_VIDEO',
        },
        hideUploadButton: true,
        hideAfterFinish: false,
        restrictions: {
          maxNumberOfFiles: 1,
          maxFileSize: 3_000_000,
          allowedFileTypes: ['.mp4', '.mkv', '.webm'],
        },
      })
        .use(Tus, {
          endpoint: `${uploadDomain}/files/`,
          chunkSize: 2_000_000,
          headers: {
            authorization: `Bearer ${this.token}`,
          },
        })
        .on('complete', () => {
          console.log('complete upload');
          this.openUppy = false;
          // Short timeout delay to allow video to process before fetching
          setTimeout(() => {
            this.$store.dispatch('video/getUser', this.user.id);
          }, 1000);
        })
        .on('upload-error', (_, error) => {
          // this.$emit('close-modal');
          this.openUppy = false;
          if (error.isNetworkError) {
            this.$store.dispatch('notify/add', {
              title: 'Network Error',
              text: 'Upload failed due to network issues. Try again later.',
              type: 'warning',
            });
          } else {
            this.$store.dispatch('notify/add', {
              title: 'Upload Error',
              text: 'Upload failed due to some unknown issues. Try again later.',
              type: 'warning',
            });
          }
        });
    },
  },
  watch: {
    dialog(val) {
      if (!val) {
        this.uppy.reset();
      }
    },
  },
  methods: {
    toggleUploadVideoDialog() {
      if (this.isUserVerified) {
        this.dialog = !this.dialog;
      } else {
        this.$store.dispatch('auth/setShowUserVerifiedModal', true);
      }
    },
    addVideoFile(blob) {
      console.log('got file', blob);
      this.uppy.addFile({
        name: blob.name,
        type: blob.type,
        data: blob,
      });
      this.uppy.upload()
        .then((result) => {
          console.info('Successful uploads:', result.successful);
          this.dialog = false;
        });
    },
  },
  beforeDestroy() {
    this.uppy.close();
  },
};
</script>

<style>
#closeBtn {
  position: absolute;
  z-index: 10;
  top: 10px;
  left: 10px;
}
</style>
