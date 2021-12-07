<template>
  <v-container>
    <v-alert
      v-show="!checkins.length"
      class="mx-auto elevation-2"
      color="info"
      colored-border
      prominent
      icon="mdi-marker-check"
      border="left"
      max-width="500"
    >
      Be first to check-in!
    </v-alert>
    <CardCheckin
      v-for="checkin in checkins"
      :key="checkin.id"
      :item="checkin"
      :linkUser="true"
    ></CardCheckin>
  </v-container>
</template>

<script>
import { mapGetters } from 'vuex';
import dayjs from 'dayjs';
import CardCheckin from '@/components/timeline/CardCheckin.vue';

export default {
  name: 'TabTimeline',
  props: ['nakamal'],
  components: {
    CardCheckin,
  },
  computed: {
    ...mapGetters({
      getImages: 'image/nakamal',
      getCheckins: 'checkin/nakamal',
    }),
    checkins() {
      return this.getCheckins(this.nakamal.id)
        .sort((a, b) => (dayjs(a.created_at).isAfter(dayjs(b.created_at)) ? -1 : 1));
    },
    images() {
      return this.getImages(this.nakamal.id)
        .sort((a, b) => (dayjs(a.created_at).isAfter(dayjs(b.created_at)) ? -1 : 1));
    },
  },
};
</script>

<style>

</style>
