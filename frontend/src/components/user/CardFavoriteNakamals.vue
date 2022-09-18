<template>
  <v-list subheader class="elevation-3 mb-3">
    <v-subheader>{{ $t('user.favorite_nakamals') }}</v-subheader>
    <v-list-item v-if="nakamals.length === 0">
      <v-list-item-icon class="mr-3">
        <v-icon>mdi-emoticon-sad-outline</v-icon>
      </v-list-item-icon>
      <v-list-item-content>
        <v-list-item-title>{{ $t('user.favorite_nakamals_none') }}</v-list-item-title>
      </v-list-item-content>
    </v-list-item>
    <v-list-item
      :to="{ name: 'Nakamal', params: { id: nakamal.id } }"
      v-for="(nakamal, i) in nakamals"
      :key="nakamal.id"
    >
      <v-list-item-action class="mr-0">{{ i + 1 }}</v-list-item-action>
      <v-list-item-content>
        <v-list-item-title v-if="i === 0">{{ nakamal.name }}</v-list-item-title>
        <v-list-item-title v-else class="font-weight-light">
          {{ nakamal.name }}
        </v-list-item-title>
        <v-list-item-subtitle>
          {{ $t('checkin.title') }}: {{ checkinCount[nakamal.id] }}
        </v-list-item-subtitle>
      </v-list-item-content>
      <v-badge
        v-if="nakamalAvatar(nakamal.profile)"
        :color="nakamal.lightBadge.color"
        dot
        overlap
        bordered
        left
        offset-x="24"
        offset-y="18"
        dark
      >
        <v-list-item-avatar>
          <v-img
            :src="nakamalAvatar(nakamal.profile).thumbnail"
          ></v-img>
        </v-list-item-avatar>
      </v-badge>
    </v-list-item>
  </v-list>
</template>

<script>
import { mapActions, mapGetters } from 'vuex';

export default {
  name: 'CardFavoriteNakamals',
  props: ['userId'],
  data() {
    return {
      nakamals: [],
      checkinCount: {},
    };
  },
  computed: {
    ...mapGetters({
      getFavoriteNakamals: 'checkin/favoriteNakamals',
    }),
  },
  methods: {
    ...mapActions({
      loadNakamal: 'nakamal/loadOne',
    }),
    nakamalAvatar(profileId) {
      if (profileId === null) return null;
      return this.$store.getters['image/find'](profileId);
    },
  },
  async mounted() {
    const favorites = this.getFavoriteNakamals(this.userId);
    for (let i = 0; i < favorites.length; i++) {
      let n = await this.loadNakamal(favorites[i].nakamal);
      this.nakamals.push(n);
      this.checkinCount[n.id] = favorites[i].count;
    };
  },
};
</script>

<style>

</style>