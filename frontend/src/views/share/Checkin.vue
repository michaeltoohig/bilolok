<template>
  <div class="checkin">
    <div v-if="loading">
      <v-container fill-height>
        <v-layout align-center justify-center>
          <v-flex>
            <div class="text-center">
              <div class="headline my-5">Loading Check-in...</div>
              <v-progress-circular size="100" indeterminate color="primary"></v-progress-circular>
            </div>
          </v-flex>
        </v-layout>
      </v-container>
    </div>
    <div v-else>
      <v-container class="d-flex justify-center align-center">
        <v-responsive max-width="600" class="pa-3">
          <CheckinTimelineCard
            :item="checkin"
            :linkNakamal="true"
          />
        </v-responsive>
      </v-container>
    </div>
  </div>
</template>

<script>
import { mapActions } from 'vuex';
import CheckinTimelineCard from '@/components/timeline/CheckinTimelineCard.vue';

export default {
  name: 'Checkin',
  metaInfo() {
    return {
      title: this.checkin ? `Checkin at ${this.checkin.nakamal.name}` : undefined,
      titleTemplate: 'Bilolok - %s',
      meta: [
        {
          property: 'og:title',
          content: this.checkin ? `Checkin at ${this.checkin.nakamal.name}` : undefined,
          // following template options are identical
          // template: '%s - My page',
          template: (chunk) => `Bilolok - ${chunk}`,
          vmid: 'og:title',
        },
        {
          property: 'og:image',
          content: this.checkin ? this.checkin.user.avatar : undefined,
          vmid: 'og:image',
        },
        {
          property: 'og:image:type',
          content: this.checkin ? 'image/jpeg' : undefined,
          vmid: 'og:image:type',
        },
        {
          property: 'og:image:width',
          content: this.checkin ? '100' : undefined,
          vmid: 'og:image:width',
        },
        {
          property: 'og:image:height',
          content: this.checkin ? '100' : undefined,
          vmid: 'og:image:height',
        },
      ],
    };
  },
  components: {
    CheckinTimelineCard,
  },
  data() {
    return {
      loading: true,
    };
  },
  computed: {
    checkin() {
      const { id } = this.$route.params;
      return this.$store.getters['checkin/find'](id);
    },
  },
  methods: {
    ...mapActions({
      load: 'checkin/getOne',
    }),
  },
  async mounted() {
    this.loading = true;
    const { id } = this.$route.params;
    await this.load(id);
    this.loading = false;
  },
};
</script>

<style>

</style>
