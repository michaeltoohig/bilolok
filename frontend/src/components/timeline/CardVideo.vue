<template>
  <v-card class="elevation-2 mb-3">
    <v-list-item class="d-flex flex-row">
      <v-list-item-avatar
        color="grey darken-3 elevation-2 user-avatar"
        tile
        v-ripple="{ center: true }"
        @click="$router.push({ name: 'User', params: { id: item.user.id } })"
      >
        <v-img :src="item.user.avatar"></v-img>
      </v-list-item-avatar>
        <v-tooltip bottom>
          <template v-slot:activator="{ on, attrs }">
            <span
              v-bind="attrs"
              v-on="on"
            >
              <strong>{{ formatTimeAgo(item.created_at) }}</strong>
            </span>
          </template>
          <span>{{ formatTime(item.created_at) }}</span>
        </v-tooltip>
      <v-spacer></v-spacer>
      <v-list-item-action>
        <v-btn
          outlined
          small
          icon
          link
          :to="{ name: 'User', params: { id: item.user.id } }"
        >
          <v-icon>mdi-chevron-right</v-icon>
        </v-btn>
      </v-list-item-action>
    </v-list-item>
    <v-card-text v-if="item.status==='COMPLETE'">
      <video width="100%" :poster="item.cover" controls autoplay>
        <source :src="item.src" type="video/webm">
        <p>Sorry, your browser does not support embedded videos. Here is
        a <a :href="item.src">link to the video</a> instead.</p>
      </video>
    </v-card-text>
    <v-card-text v-else-if="item.status!=='ERROR'">
      Your video is still processing and not ready for playing yet.
    </v-card-text>
    <v-card-text v-else>
      Video Error. Something went wrong and we will try to fix it.
      Otherwise we will delete this video in the coming days.
    </v-card-text>
    <v-list-item v-if="linkNakamal">
      <v-list-item-avatar
        v-if="nakamalAvatar(item.nakamal.id)"
        color="grey darken-3"
        class="nakamal-avatar"
        v-ripple="{ center: true }"
        @click="$router.push({ name: 'Nakamal', params: { id: item.nakamal.id } })"
      >
        <v-img :src="nakamalAvatar(item.nakamal.id).thumbnail"></v-img>
      </v-list-item-avatar>
      <v-list-item-content>
        <v-list-item-title>
          {{ item.nakamal.name }}
        </v-list-item-title>
      </v-list-item-content>
      <v-list-item-action>
        <v-btn
          outlined
          small
          icon
          link
          :to="{ name: 'Nakamal', params: { id: item.nakamal.id } }"
        >
          <v-icon>mdi-chevron-right</v-icon>
        </v-btn>
      </v-list-item-action>
    </v-list-item>
  </v-card>
</template>

<script>
// import { mapGetters } from 'vuex';
import formatDatetime from '@/mixins/formatDatetime';

export default {
  name: 'CardVideo',
  props: {
    item: {
      type: Object,
      required: true,
    },
    linkUser: {
      type: Boolean,
      default: false,
    },
    linkNakamal: {
      type: Boolean,
      default: false,
    },
  },
  mixins: [formatDatetime],
  components: {
  },
  data() {
    return {
      color: 'yellow',
    };
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
