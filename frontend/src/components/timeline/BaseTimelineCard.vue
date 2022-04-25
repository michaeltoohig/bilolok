<template>
  <v-card class="elevation-2 mb-3">
    <v-list-item class="d-flex flex-row">
      <v-list-item-avatar
        color="grey darken-3 elevation-2 user-avatar"
        tile
        v-ripple="{ center: true }"
        @click="$router.push({ name: 'User', params: { id: user.id } })"
      >
        <v-img :src="user.avatar"></v-img>
      </v-list-item-avatar>
      <div class="d-flex flex-column justify-start align-start">
        <v-tooltip bottom>
          <template v-slot:activator="{ on, attrs }">
            <span
              v-bind="attrs"
              v-on="on"
              class="subtitle-2 text--secondary"
            >
              {{ formatTimeAgo(timestamp) }}
            </span>
          </template>
          <span>{{ formatTime(timestamp) }}</span>
        </v-tooltip>
        <div v-if="nakamal && linkNakamal">
          <a @click="$router.push({ name: 'Nakamal', params: { id: nakamal.id } })">
            <h3 class="primary--text">{{ nakamal.name }}</h3>
          </a>
        </div>
      </div>
      <v-spacer></v-spacer>
      <v-list-item-action>
        <!-- TODO delete option for owner or superuser, share, etc. in menu -->
      </v-list-item-action>
    </v-list-item>
    <!-- Content Slot! -->
    <slot></slot>
  </v-card>
</template>

<script>
import { mapGetters } from 'vuex';
import formatDatetime from '@/mixins/formatDatetime';

export default {
  name: 'BaseTimelineCard',
  props: {
    timestamp: {
      type: String,
      required: true,
    },
    user: {
      type: Object,
      required: true,
    },
    nakamal: {
      type: Object,
      required: false,
    },
    linkNakamal: {
      type: Boolean,
      default: false,
    },
  },
  mixins: [formatDatetime],
  components: {
  },
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
  },
};
</script>

<style scoped>
.nakamal-avatar,
.user-avatar {
  cursor: pointer;
}
</style>
