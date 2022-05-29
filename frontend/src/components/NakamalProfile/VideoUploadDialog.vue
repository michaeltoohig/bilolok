<template>
  <div>
    <DashboardModal
      :uppy="uppy"
      :open="openUppy"
      :plugins="[]"
      :props="{ theme }"
    />

    <v-dialog
      v-model="open"
      persistent
      max-width="400px"
    >
      <v-card class="pa-0">
        <v-btn
          id="closeBtn"
          @click="close"
          small
          outlined
          color="red"
        ><v-icon>mdi-close</v-icon></v-btn>
        <VideoJSRecord :enable="open" v-on:recorded-data="addVideoFile" />
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
  name: 'VideoUploadDialog',
  props: {
    open: {
      type: Boolean,
      required: true,
    },
    nakamal: {
      type: Object,
      default: false,
      required: false
    },
  },
  components: {
    DashboardModal,
    StatusBar,
    VideoJSRecord,
  },
  data() {
    return {
      // dialog: false,
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
          Target: 'NAKAMAL_VIDEO',
          NakamalID: this.nakamal.id,
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
    open(val) {
      if (!val) {
        this.uppy.reset();
      }
    },
  },
  methods: {
    close() {
      this.$emit('close-modal');
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
          this.close();
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
