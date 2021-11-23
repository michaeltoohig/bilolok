<template>
  <div>
    <div v-if="isLoggedIn">
      <DashboardModal
        :uppy="uppy"
        :open="open"
        :plugins="[]"
        :props="{theme: 'light'}"
      />
    </div>
    <div v-else>
      <v-dialog
        v-model="open"
      >
        <v-card>
          <v-card-title>Not Logged In</v-card-title>
          <v-card-text>To upload an image you must be logged in.</v-card-text>
        </v-card>
      </v-dialog>
    </div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex';
import { DashboardModal } from '@uppy/vue';
import { uploadDomain } from '@/env';

import '@uppy/core/dist/style.css';
import '@uppy/dashboard/dist/style.css';

import { Uppy } from '@uppy/core';
import Tus from '@uppy/tus';

export default {
  name: 'NakamalImageUpload',
  props: ['nakamal', 'open'],
  components: {
    DashboardModal,
  },
  computed: {
    ...mapGetters({
      isLoggedIn: 'auth/isLoggedIn',
      user: 'auth/user',
      token: 'auth/token',
    }),
    uppy() {
      return new Uppy({
        meta: {
          NakamalID: this.nakamal.id,
        },
      }).use(Tus, {
        endpoint: `${uploadDomain}/files/`,
        chunkSize: 2_000_000,
        headers: {
          authorization: `Bearer ${this.token}`,
        },
      }).on('dashboard:modal-closed', () => {
        this.$emit('close-modal');
      }).on('complete', (result) => {
        if (result.successful.length >= 1) {
          setTimeout(() => {
            this.$emit('close-modal');
            this.$store.dispatch('image/getNakamal', this.nakamal.id);
          }, 1000);
        }
      });
      // Doesn't work since image is not ready on backend so can not fetch new images
      // .on('complete', () => {
      //   this.$emit('upload-complete');
      // });
    },
  },
  beforeDestroy() {
    this.uppy.close();
  },
};
</script>

<style>

</style>
