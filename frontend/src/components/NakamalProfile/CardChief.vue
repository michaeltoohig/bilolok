<template>
  <v-card
    v-if="chief"
    class="mb-3"
    color="secondary darken-2"
    dark
  >
    <div class="d-flex flex-no-wrap justify-space-between">
      <div>
        <v-card-title class="text-h5 pb-0">Chief</v-card-title>
        <v-card-text class="mt-0">
          <h5>Check-ins this month:</h5>
          <span class="font-weight-bold text-h5">{{ userCheckinCountMonth(chief.id) }}</span>
        </v-card-text>
        <v-card-actions class="py-1">
          <v-btn
            text
            small
            color="secondary lighten-2"
            @click="show = !show"
          >
            What's This?
          </v-btn>
        </v-card-actions>
      </div>
      <v-avatar
        class="ma-3 elevation-2"
        size="100"
        tile
        link
        @click="$router.push({ name: 'User', params: { id: chief.id } })"
      >
        <v-img :src="chief.avatar"></v-img>
      </v-avatar>
    </div>
    <v-expand-transition>
      <v-card
        v-if="show"
        class="transition-fast-in-fast-out v-card--reveal"
        style="height: 100%;"
      >
        <v-card-text class="pb-0">
          <p class="text-h5 mb-1">
            Chief
          </p>
          <p class="">
            This is the user who has
            the most check-ins in the last 30 days.
          </p>
        </v-card-text>
        <v-card-actions class="pt-0">
          <v-btn
            text
            color="primary lighten-2"
            @click="show = false"
          >
            Close
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-expand-transition>
  </v-card>
</template>

<script>
import { mapGetters } from 'vuex';
import dayjs from 'dayjs';

export default {
  name: 'CardChief',
  props: ['nakamal'],
  data() {
    return {
      show: false,
    };
  },
  computed: {
    ...mapGetters({
      getCheckins: 'checkin/nakamal',
    }),
    checkins() {
      return this.getCheckins(this.nakamal.id);
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
.v-card--reveal {
  bottom: 0;
  opacity: 1 !important;
  position: absolute;
  width: 100%;
}
</style>
