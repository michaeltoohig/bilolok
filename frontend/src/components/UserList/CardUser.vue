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
        <v-card-title class="py-0">{{ user.latest_checkin.nakamal.name }}</v-card-title>
        <v-card-text class="pb-0" v-if="user.latest_checkin.message">
          - {{ user.latest_checkin.message }}
        </v-card-text>
      </div>
    </div>
  </v-card>
</template>

<script>
import formatDatetime from '@/mixins/formatDatetime';

export default {
  name: 'CardUser',
  mixins: [formatDatetime],
  props: ['user'],
};
</script>

<style>

</style>
