<template>
  <div>
    <h4>{{ $t('nakamal.attrs.resources') }}</h4>
    <span>
      <strong v-if="!nakamal.resources.length">
        {{ $t('nakamal.attrs.resources_none') }}
      </strong>
    </span>
    <v-chip
      v-for="resource in nakamal.resources"
      :key="resource.id"
      class="mr-2 mb-2"
    >
      {{ resource.name }}
    </v-chip>

    <v-list>
      <v-list-item two-line>
        <v-list-item-content>
          <v-list-item-title>{{ $t('nakamal.attrs.light') }}</v-list-item-title>
          <v-list-item-subtitle>{{ nakamal.light }}</v-list-item-subtitle>
        </v-list-item-content>
      </v-list-item>
      <v-list-item two-line>
        <v-list-item-content>
          <v-list-item-title>{{ $t('nakamal.attrs.area') }}</v-list-item-title>
          <v-list-item-subtitle>{{ nakamal.area.name }}</v-list-item-subtitle>
        </v-list-item-content>
      </v-list-item>
      <v-list-item two-line>
        <v-list-item-content>
          <v-list-item-title>{{ $t('nakamal.attrs.kava_source') }}</v-list-item-title>
          <v-list-item-subtitle>{{ kavaSource(nakamal.kava_source) }}</v-list-item-subtitle>
        </v-list-item-content>
      </v-list-item>
      <v-list-item two-line>
        <v-list-item-content>
          <v-list-item-title>{{ $t('nakamal.attrs.number_of_windows') }}</v-list-item-title>
          <v-list-item-subtitle>{{ nakamal.windows }}</v-list-item-subtitle>
        </v-list-item-content>
      </v-list-item>
      <v-list-item two-line>
        <v-list-item-content>
          <v-list-item-title>{{ $t('nakamal.attrs.other_names') }}</v-list-item-title>
          <v-list-item-subtitle>{{ aliasNames(nakamal.aliases) }}</v-list-item-subtitle>
        </v-list-item-content>
      </v-list-item>
      <v-list-item two-line>
        <v-list-item-content>
          <v-list-item-title>{{ $t('nakamal.attrs.owner') }}</v-list-item-title>
          <v-list-item-subtitle>{{ nakamal.owner }}</v-list-item-subtitle>
        </v-list-item-content>
      </v-list-item>
      <v-list-item two-line>
        <v-list-item-content>
          <v-list-item-title>{{ $t('nakamal.attrs.phone') }}</v-list-item-title>
          <v-list-item-subtitle>{{ nakamal.phone }}</v-list-item-subtitle>
        </v-list-item-content>
      </v-list-item>
      <v-list-item two-line>
        <v-list-item-content>
          <v-list-item-title>{{ $t('nakamal.attrs.checkins_today') }}</v-list-item-title>
          <v-list-item-subtitle>{{ checkinsCountToday }}</v-list-item-subtitle>
        </v-list-item-content>
      </v-list-item>
      <v-list-item two-line>
        <v-list-item-content>
          <v-list-item-title>{{ $t('nakamal.attrs.checkins_month') }}</v-list-item-title>
          <v-list-item-subtitle>{{ checkinsCountMonth }}</v-list-item-subtitle>
        </v-list-item-content>
      </v-list-item>
    </v-list>

  </div>
</template>

<script>
import { mapGetters } from 'vuex';
import dayjs from 'dayjs';

export default {
  name: 'TabDetails',
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
    aliasNames(aliases) {
      if (!aliases) return '-';
      return aliases.join(', ');
    },
    kavaSource(ks) {
      let v = ks.province;
      if (ks.island) {
        v += `: ${ks.island}`;
      }
      return v;
    },
  },
};
</script>

<style>

</style>
