<template>
  <v-lazy
    v-model="show"
    :options="{
      threshold: .5
    }"
    min-height="100"
    transition="fade-transition"
  >
    <v-card class="elevation-2 mb-3">
      <v-list-item class="d-flex flex-row">
        <v-list-item-avatar
          v-if="hasUser"
          color="grey darken-3 elevation-2 user-avatar"
          tile
          v-ripple="{ center: true }"
          @click="toUser"
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
          <div v-if="hasNakamal && linkNakamal">
            <a @click="toNakamal">
              <h3 class="primary--text">{{ nakamal.name }}</h3>
            </a>
          </div>
        </div>
        <v-spacer></v-spacer>
        <v-list-item-action>
          <slot name="card-action">
            <!-- Place for putting a button or dropdown menu of options -->
          </slot>
        </v-list-item-action>
      </v-list-item>
      <!-- Content Slot! -->
      <slot></slot>
    </v-card>
  </v-lazy>
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
      required: false,
      default: null,
    },
    nakamal: {
      type: Object,
      required: false,
      default: null,
    },
    linkNakamal: {
      type: Boolean,
      default: false,
    },
  },
  mixins: [formatDatetime],
  data() {
    return {
      show: false,
    };
  },
  computed: {
    hasUser() {
      return this.user !== null;
    },
    hasNakamal() {
      return this.nakamal !== null;
    },
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
    toUser() {
      const { id } = this.user;
      this.$router.push({ name: 'User', params: { id } });
    },
    toNakamal() {
      const { id } = this.nakamal;
      this.$store.dispatch('nakamal/select', id)
        .then(() => {
          this.$router.push({ name: 'Nakamal', params: { id } });
        });
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
