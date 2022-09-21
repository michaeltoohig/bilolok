<template>
  <BaseTimelineCard
    :timestamp="item.created_at"
    :user="user"
    :nakamal="nakamal"
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
import { mapActions, mapGetters } from 'vuex';
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
  data() {
    return {
      user: null,
      nakamal: null,
    };
  },
  computed: {
    image() {
      return { pid: this.item.id, ...this.item };
    },
    ...mapGetters({
      isLoggedIn: 'auth/isLoggedIn',
      currentUser: 'auth/user',
      hasAdminAccess: 'auth/hasAdminAccess',
    }),
    isMine() {
      if (!this.user || !this.isLoggedIn) return false;
      return this.user.id === this.currentUser.id;
    },
    userCanDelete() {
      return this.isMine || this.hasAdminAccess;
    },
  },
  methods: {
    async onShare() {
      const text = `Image of ${this.nakamal.name} on Bilolok!`;
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
      if (confirm(this.$i18n.t('image.confirm_delete'))) {
        this.$store.dispatch('image/remove', this.item.id);
      }
    },
    ...mapActions({
      loadUser: 'user/loadOne',
      loadNakamal: 'nakamal/loadOne',
    }),
  },
  async created() {
    if (this.item.nakamal) {
      this.nakamal = await this.loadNakamal(this.item.nakamal);
    }
    this.user = await this.loadUser(this.item.user);
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
