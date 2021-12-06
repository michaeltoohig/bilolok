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
          v-for="item in items"
          :key="item.id"
        >
          <v-card class="elevation-2 mb-3">
            <v-card-title>
              <h2 :class="`headline font-weight-light ${itemColor(item)}--text`">
                <span v-if="getItemType(item) === 'checkin'">
                  Check-in
                </span>
                <span v-else-if="getItemType(item) === 'image'">
                  Uploaded Image
                </span>
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
            <v-card-text v-if="item.src">
              <v-img
                contain
                :max-height="300"
                :src="item.src"
                :lazy-src="item.msrc"
              ></v-img>
            </v-card-text>
            <v-list-item>
              <v-list-item-avatar
                v-if="nakamalAvatar(item.nakamal.id)"
                color="grey darken-3"
              >
                <v-img
                  :src="nakamalAvatar(item.nakamal.id).thumbnail"
                ></v-img>
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
                  link :to="{ name: 'Nakamal', params: { id: item.nakamal.id } }"
                >
                  <v-icon>mdi-chevron-right</v-icon>
                </v-btn>
              </v-list-item-action>
            </v-list-item>
          </v-card>
        </div>
      </v-container>
    </div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex';
import formatDatetime from '@/mixins/formatDatetime';

export default {
  name: 'User',
  mixins: [formatDatetime],
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
    images() {
      const { id } = this.user;
      return this.getUserImages(id);
      // if (!images) return [];
      // return images;
    },
    checkins() {
      const { id } = this.user;
      return this.getUserCheckins(id);
      // if (!checkins) return [];
      // return checkins;
    },
    items() {
      const newList = this.images.concat(this.checkins);
      return newList.sort((a, b) => b.created_at.localeCompare(a.created_at));
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
    getItemType(item) {
      // TODO Hacky way to find object type - should be improved
      if ('private' in item) return 'checkin';
      if ('src' in item) return 'image';
      return 'other';
    },
    itemColor(item) {
      const type = this.getItemType(item);
      if (type === 'checkin') return 'red';
      if (type === 'image') return 'blue';
      return 'black';
    },
    itemIcon(item) {
      const type = this.getItemType(item);
      if (type === 'checkin') return 'mdi-check';
      if (type === 'image') return 'mdi-image';
      return 'mdi-info';
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
