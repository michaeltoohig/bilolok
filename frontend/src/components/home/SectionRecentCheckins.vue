<template>
  <v-container>
    <h2>Recent Check-ins</h2>
    <v-list>
      <v-list-item
        v-for="checkin in checkins"
        :key="checkin.id"
        :to="{ name: 'Nakamal', params: { id: checkin.nakamal.id } }"
      >
        <v-list-item-avatar>
          <v-img
            :alt="`${checkin.user_id} avatar`"
            :src="checkin.user_id"
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
      </v-list-item>
    </v-list>
  </v-container>
</template>

<script>
import { mapGetters } from 'vuex';
import dayjs from 'dayjs';
import RelativeTime from 'dayjs/plugin/relativeTime';
import LocalizedFormat from 'dayjs/plugin/localizedFormat';

dayjs.extend(RelativeTime);
dayjs.extend(LocalizedFormat);

export default {
  name: 'SectionRecentCheckins',
  computed: {
    ...mapGetters({
      checkins: 'checkin/recent',
    }),
  },
  methods: {
    formatTimeAgo(d) {
      return dayjs(d).fromNow();
    },
    formatTime(d) {
      return dayjs(d).format('LLL');
    },
  },
  beforeMount() {
    this.$store.dispatch('checkin/getRecent');
  },
};
</script>

<style>

</style>
