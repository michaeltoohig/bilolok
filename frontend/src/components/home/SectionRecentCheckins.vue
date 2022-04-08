<template>
  <v-container>
    <h2>Recent Check-ins</h2>

    <v-card
      v-for="checkin in checkins"
      :key="checkin.id"
      class="elevation-2 mb-3"
    >
      <div class="d-flex flex-no-wrap justify-start">
        <v-avatar
          v-ripple="{ center: true }"
          class="ma-3 elevation-2 user-avatar"
          size="100"
          tile
          link
          @click="$router.push({ name: 'User', params: { id: checkin.user.id } })"
        >
          <v-img :src="checkin.user.avatar"></v-img>
        </v-avatar>
        <div class="flex-grow-1 d-flex flex-column justify-space-between">
          <v-card-text class="pb-0 pt-2">
            <v-tooltip bottom>
              <template v-slot:activator="{ on, attrs }">
                <span
                  v-bind="attrs"
                  v-on="on"
                >
                  <span class="font-weight-normal text--secondary">Checked-in: </span>
                  <strong>{{ formatTimeAgo(checkin.created_at) }}</strong>
                </span>
              </template>
              <span>{{ formatTime(checkin.created_at) }}</span>
            </v-tooltip>
          </v-card-text>
          <v-card-text v-if="checkin.message" class="pt-0 text-h6 font-weight-normal">
            {{ checkin.message }}
          </v-card-text>
          <v-card-title class="text-h5 pt-0 d-flex justify-space-between">
            <h4 class="mr-3">{{ checkin.nakamal.name }}</h4>
            <v-btn
              outlined
              small
              @click="goToNakamal(checkin.nakamal.id)"
            >
              Go To Kava Bar
              <v-icon>mdi-chevron-right</v-icon>
            </v-btn>
          </v-card-title>
        </div>
      </div>
    </v-card>
  </v-container>
</template>

<script>
import { mapGetters } from 'vuex';
import formatDatetime from '@/mixins/formatDatetime';

export default {
  name: 'SectionRecentCheckins',
  mixins: [formatDatetime],
  computed: {
    ...mapGetters({
      recentCheckins: 'checkin/recent',
    }),
    checkins() {
      const n = Math.min(this.recentCheckins.length, 3);
      return this.recentCheckins.slice(0, n);
    },
  },
  methods: {
    goToNakamal(id) {
      this.$router.push({ name: 'Nakamal', params: { id } });
    },
    goToUser(id) {
      this.$router.push({ name: 'User', params: { id } });
    },
  },
  beforeMount() {
    this.$store.dispatch('checkin/getRecent');
  },
};
</script>

<style>
.user-avatar {
  cursor: pointer;
}
</style>
