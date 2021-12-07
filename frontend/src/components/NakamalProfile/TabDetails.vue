<template>
  <v-container>
    <v-card
      v-if="chief"
      class="mb-3"
      color="primary"
      dark
    >
      <div class="d-flex flex-no-wrap justify-space-between">
        <div>
          <v-card-title
            class="text-h5"
          >
            Current Chief
          </v-card-title>

          <v-card-subtitle v-text="chief.id"></v-card-subtitle>

          <v-card-text>
            <h5>Check ins this month:</h5>
            <span>{{ userCheckinCountMonth(chief.id) }}</span>
          </v-card-text>

          <v-card-actions>
            <v-tooltip bottom>
              <template v-slot:activator="{ on, attrs }">
                <v-btn
                  text
                  color="secondary"
                  v-bind="attrs"
                  v-on="on"
                >
                  What's This?
                </v-btn>
              </template>
              <v-responsive max-width="170">
                <span>The chief is the user who has
                  the most check-ins in the last 30 days.</span>
              </v-responsive>
            </v-tooltip>
          </v-card-actions>
        </div>

        <v-avatar
          class="ma-3 elevation-2"
          size="125"
          tile
          link
          @click="$router.push({ name: 'User', params: { id: chief.id } })"
        >
          <v-img :src="chief.avatar"></v-img>
        </v-avatar>
      </div>
    </v-card>

    <v-card>
      <v-list>
        <v-list-item two-line>
          <v-list-item-content>
            <v-list-item-title>Owner</v-list-item-title>
            <v-list-item-subtitle>{{ nakamal.owner }}</v-list-item-subtitle>
          </v-list-item-content>
        </v-list-item>
        <v-list-item two-line>
          <v-list-item-content>
            <v-list-item-title>Number</v-list-item-title>
            <v-list-item-subtitle>{{ nakamal.phone }}</v-list-item-subtitle>
          </v-list-item-content>
        </v-list-item>
        <v-list-item two-line>
          <v-list-item-content>
            <v-list-item-title>Light</v-list-item-title>
            <v-list-item-subtitle>{{ nakamal.light }}</v-list-item-subtitle>
          </v-list-item-content>
        </v-list-item>
        <v-list-item two-line>
          <v-list-item-content>
            <v-list-item-title>Checkins Today</v-list-item-title>
            <v-list-item-subtitle>{{ checkinsCountToday }}</v-list-item-subtitle>
          </v-list-item-content>
        </v-list-item>
        <v-list-item two-line>
          <v-list-item-content>
            <v-list-item-title>Checkins Month</v-list-item-title>
            <v-list-item-subtitle>{{ checkinsCountMonth }}</v-list-item-subtitle>
          </v-list-item-content>
        </v-list-item>
      </v-list>
    </v-card>
  </v-container>
</template>

<script>
import { mapGetters } from 'vuex';
import dayjs from 'dayjs';

export default {
  name: 'TabDetails',
  props: ['nakamal'],
  data() {
    return {
      show: true,
    };
  },
  computed: {
    ...mapGetters({
      getCheckins: 'checkin/nakamal',
    }),
    checkins() {
      return this.getCheckins(this.nakamal.id)
        .sort((a, b) => (dayjs(a.created_at).isAfter(dayjs(b.created_at)) ? -1 : 1));
    },
    chief() {
      if (!this.checkins) return null;
      // Limit checkins to last 30 days only
      const threshold = dayjs().startOf('d').subtract(30, 'd');
      const checkins = this.checkins.filter((c) => dayjs(c.created_at).isAfter(threshold));
      if (checkins.length === 0) return null;
      // Setup
      const checkinMap = {};
      let maxEl = checkins[0];
      let maxCount = 1;
      // Find user with most checkins
      for (let i = 0; i < checkins.length; i += 1) {
        const el = checkins[i];
        const userId = el.user.id;
        // Add userId to checkin map if not exists or increment count
        if (!checkinMap[userId]) {
          checkinMap[userId] = {
            count: 1,
            created: el.created_at,
          };
        } else {
          // Increment count and set latest created
          checkinMap[userId].count += 1;
          if (dayjs(maxEl.created_at).isBefore(el.created_at)) {
            checkinMap[userId].created = el.created_at;
          }
        }
        // Determine current user with most check-ins or if a tie then most recent check-in
        if (checkinMap[userId].count > maxCount) {
          maxCount = checkinMap[userId].count;
          maxEl = el;
        } else if (checkinMap[userId].count === maxCount) {
          if (dayjs(el.created_at).isAfter(dayjs(checkinMap[userId].created))) {
            maxEl = el;
          }
        }
      }
      return maxEl.user;
    },
    checkinsCountToday() {
      if (!this.checkins) return 0;
      const threshold = dayjs().startOf('d').subtract(1, 'd');
      return this.checkins
        .filter((c) => dayjs(c.created_at).isAfter(threshold))
        .length;
    },
    checkinsCountMonth() {
      if (!this.checkins) return 0;
      const threshold = dayjs().startOf('d').subtract(30, 'd');
      return this.checkins
        .filter((c) => dayjs(c.created_at).isAfter(threshold))
        .length;
    },
  },
  methods: {
    userCheckinCountMonth(userId) {
      if (!this.checkins) return null;
      return this.checkins
        .filter((c) => dayjs(c.created_at).isAfter(dayjs().subtract(30, 'd')))
        .filter((c) => c.user.id === userId)
        .length;
    },
  },
};
</script>

<style>

</style>
