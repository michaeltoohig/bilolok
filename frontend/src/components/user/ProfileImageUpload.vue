<template>
  <div>
    <DashboardModal
      :uppy="uppy"
      :open="open"
      :plugins="[]"
      :props="{ theme }"
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
  props: ['open'],
  components: {
    DashboardModal,
  },
  computed: {
    ...mapGetters({
      user: 'auth/user',
      token: 'auth/token',
      darkMode: 'setting/darkMode',
    }),
    theme() {
      return this.darkMode ? 'dark' : 'light';
    },
    uppy() {
      return new Uppy({
        meta: {
          Target: 'USER_PROFILE',
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
          // setTimeout(() => {
          //   this.$store.dispatch('auth/getMe', this.token);
          // }, 500);
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
