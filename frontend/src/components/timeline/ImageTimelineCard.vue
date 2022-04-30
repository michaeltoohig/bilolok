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
    <v-card-text class="d-flex justify-center">
      <Photoswipe :options="{ history: true }">
        <img
          class="timeline-image"
          :data-image-id="image.id"
          v-pswp="image"
          :src="image.src"
          :lazy-src="image.msrc"
        />
      </Photoswipe>
    </v-card-text>
  </BaseTimelineCard>
</template>

<script>
import { domain } from '@/env';
import { mapGetters } from 'vuex';
import BaseTimelineCard from '@/components/timeline/BaseTimelineCard.vue';
import BaseTimelineCardMenu from '@/components/timeline/BaseTimelineCardMenu.vue';

export default {
  name: 'CheckinTimelineCard',
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
    image() {
      return { pid: this.item.id, ...this.item };
    },
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
      const text = `Image of ${this.item.nakamal.name} on Bilolok!`;
      const url = `${domain}/image/${this.item.id}`;
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
      if (confirm('Are you sure you want to remove this check-in?')) {
        this.$store.dispatch('image/remove', this.item.id);
      }
    },
  },
};
</script>

<style>
.timeline-image {
  max-height: 300px;
  max-width: 100%;
  contain: cover;
}
</style>
