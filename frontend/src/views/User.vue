<template>
  <div class="nakamal">
    <div v-if="loading">
      Loading...
    </div>
    <div v-else>
      <v-card flat color="secondary">
        <v-card-title>
          <v-avatar
            color="dark"
            size="64"
            tile
          >
            <v-img :src="user.avatar"></v-img>
          </v-avatar>
        </v-card-title>
        <v-card-text>
          <ul class="list-unstyled">
            <li>Check-ins: {{ checkins.length }}</li>
            <li>Images: {{ images.length }}</li>
          </ul>
        </v-card-text>
      </v-card>

      <v-container>
        <div
          v-for="item in timelineItems"
          :key="item.id"
        >
          <CardCheckin v-if="getItemType(item) === 'checkin'" :item="item" :linkNakamal="true"/>
          <CardImage v-if="getItemType(item) === 'image'" :item="item" :linkNakamal="true"/>
        </div>
      </v-container>
    </div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex';
import timeline from '@/mixins/timeline';
import formatDatetime from '@/mixins/formatDatetime';
import CardCheckin from '@/components/timeline/CardCheckin.vue';
import CardImage from '@/components/timeline/CardImage.vue';

export default {
  name: 'User',
  mixins: [formatDatetime, timeline],
  components: {
    CardCheckin,
    CardImage,
  },
  data() {
    return {
      loading: true,
    };
  },
  computed: {
    user() {
      const { id } = this.$route.params;
      return this.$store.getters['user/find'](id);
    },
    isMe() {
      if (!this.isLoggedIn) return false;
      return this.me.id === this.user.id;
    },
    ...mapGetters({
      isLoggedIn: 'auth/isLoggedIn',
      me: 'auth/user',
      hasAdminAccess: 'auth/hasAdminAccess',
      getUserCheckins: 'checkin/user',
      getUserImages: 'image/user',
      getNakamalImages: 'image/nakamal',
    }),
    checkins() {
      const { id } = this.user;
      return this.getUserCheckins(id);
    },
    images() {
      const { id } = this.user;
      return this.getUserImages(id);
    },
  },
  watch: {
    $route: 'fetchData',
  },
  methods: {
    async fetchData() {
      this.loading = true;
      const { id } = this.user;
      await this.$store.dispatch('checkin/getUser', id);
      await this.$store.dispatch('image/getUser', id);
      this.loading = false;
    },
    nakamalAvatar(nakamalId) {
      const images = this.getNakamalImages(nakamalId);
      if (images.length > 0) {
        return images[0];
      }
      return null;
    },
    // removeImage() {
    //   /* eslint-disable no-alert, no-restricted-globals */
    //   if (confirm('Are you sure you want to remove this image?')) {
    //     this.$store.dispatch('image/remove', this.selectedImageId);
    //   }
    // },
  },
  async mounted() {
    // XXX single user get endpoint not available publicly
    // const { id } = this.$route.params;
    // await this.$store.dispatch('user/getOne', id);
    await this.$store.dispatch('user/getUsers');
    await this.fetchData();
  },
};
</script>

<style>

</style>
