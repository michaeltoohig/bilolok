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
          <p v-html="$t('video.not_supported', { src: item.src })" />
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
        {{ $t('video.processing') }}
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
        {{ $t('video.error') }}
      </v-alert>
    </v-card-text>
  </BaseTimelineCard>
</template>

<script>
import { domain } from '@/env';
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
      isLoggedIn: 'auth/isLoggedIn',
      user: 'auth/user',
      hasAdminAccess: 'auth/hasAdminAccess',
    }),
    isMine() {
      if (!this.isLoggedIn) return false;
      return this.item.user.id === this.user.id;
    },
    userCanDelete() {
      return this.isMine || this.hasAdminAccess;
    },
  },
  methods: {
    async onShare() {
      const text = 'Video on Bilolok!';
      const url = `${domain}/video/${this.item.id}`;
      if (navigator.share) {
        const { title } = document;
        navigator.share({
          url,
          title,
          text,
        }).then(() => {
          this.$store.dispatch('notify/add', {
            title: 'Thanks For Sharing!',
            text: 'We appreciate you letting others know about Bilolok.',
            type: 'primary',
          });
        });
      } else {
        if (!navigator.clipboard) {
          await this.$store.dispatch('notify/add', {
            title: 'Share Not Available',
            text: 'Your device does not support sharing.',
            type: 'error',
          });
          return;
        }
        await navigator.clipboard.writeText(`${text} ${url}`);
        await this.$store.dispatch('notify/add', {
          title: 'Copied to Clipboard!',
          text: 'We appreciate you letting others know about Bilolok.',
          type: 'primary',
        });
      }
    },
    onDelete() {
      /* eslint-disable no-alert, no-restricted-globals */
      if (confirm(this.$i18n.t('video.confirm_delete'))) {
        this.$store.dispatch('video/remove', this.item.id);
      }
    },
  },
};
</script>

<style>

</style>
