<template>
  <v-list
    v-if="nakamals.length > 0"
    color="secondary darken-2"
    dark
    subheader
    class="elevation-3 mb-3"
  >
    <v-subheader>
      {{ $tc('user.chief_of', nakamals.length, { count: nakamals.length }) }}
    </v-subheader>
    <v-list-item
      :to="{ name: 'Nakamal', params: { id: nakamal.id } }"
      v-for="(nakamal, i) in nakamals"
      :key="nakamal.id"
    >
      <v-list-item-content>
        <v-list-item-title v-if="i === 0">{{ nakamal.name }}</v-list-item-title>
        <v-list-item-title v-else class="font-weight-light">
          {{ nakamal.name }}
        </v-list-item-title>
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
  name: 'CardChiefOf',
  props: ['userId'],
  data() {
    return {
      nakamals: [],
    };
  },
  computed: {
    ...mapGetters({
      getChiefOf: 'nakamal/listByChief',
    }),
  },
  methods: {
    ...mapActions({
      loadChiefNakamals: 'nakamal/loadChiefNakamals',
    }),
    nakamalAvatar(profileId) {
      if (profileId === null) return null;
      return this.$store.getters['image/find'](profileId);
    },
  },
  async mounted() {
    await this.loadChiefNakamals(this.userId);
    this.getChiefOf(this.userId).forEach((n) => {
      if (n.profile !== null) {
        this.$store.dispatch('image/loadOne', n.profile);
      }
      this.nakamals.push(n);
    });
  }
};
</script>

<style>

</style>