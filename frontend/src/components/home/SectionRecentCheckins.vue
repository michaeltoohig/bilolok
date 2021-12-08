<template>
  <v-container>
    <h2>Recent Check-ins</h2>
    <v-list>
      <v-list-item
        v-for="checkin in checkins"
        :key="checkin.id"
        class="elevation-2 mb-3"
      >
        <v-list-item-avatar tile link class="elevation-2">
          <v-img
            :alt="`${checkin.user.id} avatar`"
            :src="checkin.user.avatar"
            @click="goToUser(checkin.user.id)"
          ></v-img>
        </v-list-item-avatar>

        <v-list-item-content>
          <v-list-item-title v-text="checkin.nakamal.name"></v-list-item-title>
          <v-list-item-subtitle>
            <v-tooltip bottom>
              <template v-slot:activator="{ on, attrs }">
                <span
                  v-bind="attrs"
                  v-on="on"
                >{{ formatTimeAgo(checkin.created_at) }}</span>
              </template>
              <span>{{ formatTime(checkin.created_at) }}</span>
            </v-tooltip>
          </v-list-item-subtitle>
        </v-list-item-content>
        <v-list-item-action>
          <v-btn
            outlined
            small
            @click="goToNakamal(checkin.nakamal.id)"
            icon
          >
            <v-icon>mdi-chevron-right</v-icon>
          </v-btn>
        </v-list-item-action>
      </v-list-item>
    </v-list>
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

</style>
