<template>
  <v-card class="elevation-2 mb-3">
    <v-card-title class="d-flex flex-row justify-space-between">
      <h2 :class="`headline font-weight-light ${this.color}--text`">
        Check-in
      </h2>
    </v-card-title>
    <v-card-subtitle>
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
    </v-card-subtitle>
    <v-card-text v-if="item.message" class="text-h5 font-weight-bold">
      {{ item.message }}
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
    <v-list-item v-if="linkUser">
      <v-list-item-avatar
        color="grey darken-3 elevation-2 user-avatar"
        tile
        v-ripple="{ center: true }"
        @click="$router.push({ name: 'User', params: { id: item.user.id } })"
      >
        <v-img :src="item.user.avatar"></v-img>
      </v-list-item-avatar>
      <v-list-item-content>
        <v-list-item-title>
        </v-list-item-title>
      </v-list-item-content>
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
  </v-card>
</template>

<script>
import { mapGetters } from 'vuex';
import formatDatetime from '@/mixins/formatDatetime';

export default {
  name: 'CardCheckin',
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
  data() {
    return {
      color: 'red',
    };
  },
  computed: {
    ...mapGetters({
      getNakamalImages: 'image/nakamal',
      getNakamalCheckins: 'checkin/nakamal',
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
    // async onShare() {
    //   return;
    //   // TODO below
    //   if (navigator.share) {
    //     // const { title } = document;
    //     const title = `Check out this ${this.item.nakamal.name}`;
    //     const text = this.item.message ? this.item.message : `Check`
    //     const url = document.querySelector('link[rel=canonical]')
    //       ? document.querySelector('link[rel=canonical]').href
    //       : document.location.href;
    //     navigator.share({
    //       url,
    //       title,
    //       text: ,
    //     }).then(() => {
    //       this.$store.dispatch('notify/add', {
    //         title: 'Thanks For Sharing!',
    //         text: 'We appreciate you letting others know about Bilolok.',
    //         type: 'primary',
    //       });
    //     });
    //   } else {
    //     await this.$store.dispatch('notify/add', {
    //       title: 'Share Not Available',
    //       text: 'Your device does not support sharing.',
    //       type: 'error',
    //     });
    //   }
    // },
  },
};
</script>

<style>
.nakamal-avatar,
.user-avatar {
  cursor: pointer;
}
</style>
