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
    <v-card-text class="d-flex flex-row justify-start align-center">
      <v-icon>mdi-marker-check</v-icon>
      <h2>
        <span>Check-in</span>
      </h2>
    </v-card-text>
    <v-card-text v-if="item.message" class="pt-0 text-h5 font-weight-normal">
      {{ item.message }}
    </v-card-text>
  </BaseTimelineCard>
</template>

<script>
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
      if (confirm('Are you sure you want to remove this check-in?')) {
        this.$store.dispatch('checkin/remove', this.item.id);
      }
    },
  },
};
</script>

<style>

</style>
