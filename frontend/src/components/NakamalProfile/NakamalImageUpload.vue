<template>
  <div>
    <DashboardModal
      :uppy="uppy"
      :open="open"
      :plugins="[]"
      :props="{theme: 'light'}"
    />
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
      user: 'auth/user',
      token: 'auth/token',
    }),
    uppy() {
      return new Uppy({
        meta: {
          NakamalID: this.nakamal.id,
        },
      })
        .use(Tus, {
          endpoint: `${uploadDomain}/files/`,
          chunkSize: 2_000_000,
          headers: {
            authorization: `Bearer ${this.token}`,
          },
        })
        .on('dashboard:modal-closed', () => {
          this.$emit('close-modal');
        })
        .on('complete', () => {
          this.$emit('close-modal');
          setTimeout(() => {
            this.$store.dispatch('image/getNakamal', this.nakamal.id);
          }, 500);
        })
        .on('upload-error', (_, error) => {
          this.$emit('close-modal');
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
  beforeDestroy() {
    this.uppy.close();
  },
};
</script>

<style>

</style>
