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
    <v-card-text class="d-flex flex-row justify-start align-center">
      <v-icon>mdi-marker-check</v-icon>
      <h2>
        <span>{{ $t('checkin.title') }}</span>
      </h2>
    </v-card-text>
    <v-card-text v-if="item.message" class="pt-0 text-h5 font-weight-normal">
      {{ item.message }}
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
    ...mapGetters({
      isLoggedIn: 'auth/isLoggedIn',
      currentUser: 'auth/user',
      hasAdminAccess: 'auth/hasAdminAccess',
      // findNakamal: 'nakamal/find',
      // findUser: 'user/find',
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
      const text = `Check-in at ${this.nakamal.name} on Bilolok!`;
      const url = `${domain}/checkin/${this.item.id}`;
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
      if (confirm(this.$i18n.t('checkin.confirm_delete'))) {
        this.$store.dispatch('checkin/remove', this.item.id);
      }
    },
    ...mapActions({
      loadUser: 'user/loadOne',
      loadNakamal: 'nakamal2/fetch',
    }),
  },
  async created() {
    console.log('item.nakamal for checkin', this.item.nakamal);
    if (this.item.nakamal) {
      this.nakamal = await this.loadNakamal(this.item.nakamal.id);
    }
    this.user = await this.loadUser(this.item.user.id);
  },
};
</script>

<style>

</style>
