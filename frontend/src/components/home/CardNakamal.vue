<template>
  <v-card>
    <v-img
      v-if="profile"
      class="white--text align-end nakamal-avatar"
      max-height="300px"
      :src="profile.src"
      @click="viewPage(nakamal.id)"
    >
      <v-card-title></v-card-title>
    </v-img>
    <v-card-title class="pb-0 primary--text">
      <a @click="viewPage(nakamal.id)">
        {{ nakamal.name }}
      </a>
    </v-card-title>
    <v-card-subtitle v-if="nakamal.aliases.length" class="pt-2">
      {{ nakamal.aliases.join(', ') }}
    </v-card-subtitle>

    <v-card-text class="text--primary">
      <v-row>
        <v-col cols="6">
          <div class="font-weight-light">
            {{ $t('nakamal.attrs.light') }}:
            <span class="font-weight-bold">{{ nakamal.light }}</span>
          </div>
          <div class="font-weight-light">
            {{ $t('nakamal.attrs.number_of_windows') }}:
            <span class="font-weight-bold">{{ nakamal.windows || '-' }}</span>
          </div>
        </v-col>
        <v-col cols="6">
          <div class="font-weight-light">
            {{ $t('nakamal.attrs.area') }}:
            <span class="font-weight-bold">{{ nakamal.area.name }}</span>
          </div>
          <div class="font-weight-light">
            {{ $t('nakamal.attrs.kava_source') }}:
            <span class="font-weight-bold">{{ kavaSource(nakamal.kava_source) }}</span>
          </div>
          <div class="font-weight-light">
          </div>
        </v-col>
      </v-row>
    </v-card-text>
    <v-card-actions>
      <v-btn
        text
        outlined
        @click="viewPage(nakamal.id)"
      >
        {{ $t('nakamal.view_page') }}
      </v-btn>
      <v-btn
        text
        outlined
        @click="viewOnMap(nakamal.id)"
      >
        {{ $t('nakamal.view_on_map') }}
      </v-btn>
    </v-card-actions>
  </v-card>
</template>

<script>
import { mapActions } from 'vuex';

export default {
  name: 'CardNakamal',
  props: ['nakamal'],
  data() {
    return {
      profile: null,
    };
  },
  methods: {
    ...mapActions({
      loadProfile: 'image/loadOne',
    }),
    viewOnMap(id) {
      this.$store.dispatch('nakamal/select', id)
        .then(() => {
          this.$router.push({ name: 'Map' });
        });
    },
    viewPage(id) {
      this.$store.dispatch('nakamal/select', id)
        .then(() => {
          this.$router.push({ name: 'Nakamal', params: { id } });
        });
    },
    kavaSource(ks) {
      let v = ks.province;
      if (ks.island) {
        v += `: ${ks.island}`;
      }
      return v;
    },
  },
  async mounted() {
    if (this.nakamal.profile !== null) {
      this.profile = await this.loadProfile(this.nakamal.profile);
    }
  },
};
</script>

<style>

</style>
