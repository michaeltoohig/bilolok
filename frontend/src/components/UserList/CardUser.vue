<template>
  <v-card class="elevation-2 mb-3">
    <div class="d-flex flex-no-wrap justify-start">
      <v-avatar
        v-ripple="{ center: true }"
        class="ma-3 mr-0 elevation-2 user-avatar"
        size="100"
        tile
        link
        @click="$router.push({ name: 'User', params: { id: user.id } })"
      >
        <v-img :src="user.avatar"></v-img>
      </v-avatar>
      <div class="flex-grow-1 d-flex flex-column justify-start">
        <v-card-subtitle class="pt-2 pb-0">
          Latest Check-in:
          <strong>{{ formatTimeAgo(user.latest_checkin.created_at) }}</strong>
        </v-card-subtitle>
        <v-card-title class="text-h5 pt-0 d-flex justify-start">
          <h4 class="mr-3">{{ user.latest_checkin.nakamal.name }}</h4>
          <v-btn
            outlined
            small
            icon
            @click="goToNakamal(user.latest_checkin.nakamal.id)"
          >
            <v-icon>mdi-chevron-right</v-icon>
          </v-btn>
        </v-card-title>
        <v-card-text v-if="user.latest_checkin.message" class="pt-0 text-h6 font-weight-normal">
          {{ user.latest_checkin.message }}
        </v-card-text>
      </div>
    </div>
  </v-card>
</template>

<script>
import { mapGetters } from 'vuex';
import formatDatetime from '@/mixins/formatDatetime';

export default {
  name: 'CardUser',
  mixins: [formatDatetime],
  props: ['user'],
  computed: {
    ...mapGetters({
      getNakamalImages: 'image/nakamal',
    }),
  },
  methods: {
    nakamalAvatar(nakamalId) {
      const images = this.getNakamalImages(nakamalId);
      if (images.length > 0) {
        return images[0];
      }
      return null;
    },
    goToNakamal(nakamalId) {
      this.$router.push({ name: 'Nakamal', params: { id: nakamalId } });
    },
  },
};
</script>

<style>

</style>
