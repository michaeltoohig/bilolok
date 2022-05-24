<template>
  <div class="app-level-alerts-wrap">
    <div class="d-flex justify-center">
      <v-alert
        v-if="noServiceWorker"
        class="my-5"
        max-width="600"
        type="warning"
        dark
        :prominent="!$vuetify.breakpoint.xsOnly"
        transition="scale-transition"
        dismissible
      >
        <div class="title">
          {{ $t('app.no_service_worker_title') }}
        </div>
        <div v-html="$t('app.no_service_worker_body')" />
      </v-alert>
      <v-alert
        v-if="updateExists"
        class="my-5"
        max-width="450"
        type="info"
        dark
        :prominent="!$vuetify.breakpoint.xsOnly"
        transition="scale-transition"
      >
        <v-row align="center">
          <v-col class="grow">
            {{ $t('app.update_available_title') }}
          </v-col>
          <v-col class="shrink">
            <v-btn @click="refreshApp">{{ $t('app.update_available_btn') }}</v-btn>
          </v-col>
        </v-row>
      </v-alert>
    </div>
  </div>
</template>

<script>
import UpdateMixin from '@/mixins/update';

export default {
  name: 'AlertUpdateExists',
  mixins: [UpdateMixin],
};
</script>

<style scoped>
.app-level-alerts-wrap {
  pointer-events: none;
  position: fixed;
  z-index: 3001;
  width: 100%;
}

.v-alert {
  pointer-events: auto;
}
</style>
