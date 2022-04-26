<template>
  <BaseTimelineCard
    :timestamp="item.created_at"
    :user="item.user"
    :nakamal="item.nakamal"
    :linkNakamal="linkNakamal"
  >
    <template v-slot:card-action>
      <BaseTimelineCardMenu
        :on-share="onShare"
        :on-delete="onDelete"
        :user-can-delete="userCanDelete"
      ></BaseTimelineCardMenu>
    </template>
    <v-card-text v-if="item.status==='COMPLETE'">
      <video width="100%" :poster="item.cover" controls>
        <source :src="item.src" type="video/webm">
        <v-alert
          class="mx-auto elevation-2"
          color="warning"
          colored-border
          prominent
          icon="mdi-video"
          border="left"
        >
          Sorry, your browser does not support embedded videos. Here is
          a <a target="_blank" :href="item.src">link to the video</a> instead.
        </v-alert>
      </video>
    </v-card-text>
    <v-card-text v-else-if="item.status!=='ERROR'">
      <v-alert
        class="mx-auto elevation-2"
        color="info"
        colored-border
        prominent
        icon="mdi-video"
        border="left"
      >
        Your video is still processing and not ready for playing yet.
      </v-alert>
    </v-card-text>
    <v-card-text v-else>
      <v-alert
        class="mx-auto elevation-2"
        color="error"
        colored-border
        prominent
        icon="mdi-video"
        border="left"
      >
        Video Error. Something went wrong and we will try to fix it.
        Otherwise we will delete this video in the coming days.
      </v-alert>
    </v-card-text>
  </BaseTimelineCard>
</template>

<script>
import { mapGetters } from 'vuex';
import BaseTimelineCard from '@/components/timeline/BaseTimelineCard.vue';
import BaseTimelineCardMenu from '@/components/timeline/BaseTimelineCardMenu.vue';

export default {
  name: 'VideoTimelineCard',
  components: {
    BaseTimelineCard,
    BaseTimelineCardMenu,
  },
  props: {
    item: {
      type: Object,
      required: true,
    },
    linkNakamal: {
      type: Boolean,
      default: false,
    },
  },
  computed: {
    ...mapGetters({
      user: 'auth/user',
      hasAdminAccess: 'auth/hasAdminAccess',
    }),
    isMine() {
      return this.item.user.id === this.user.id;
    },
    userCanDelete() {
      return this.isMine || this.hasAdminAccess;
    },
  },
  methods: {
    onShare() {
      console.log('TODO share');
    },
    onDelete() {
      /* eslint-disable no-alert, no-restricted-globals */
      if (confirm('Are you sure you want to remove this video?')) {
        this.$store.dispatch('video/remove', this.item.id);
      }
    },
  },
};
</script>

<style>

</style>
