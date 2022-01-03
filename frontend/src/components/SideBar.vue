<template>
  <div>
    <v-navigation-drawer
      v-model="drawer"
      app
    >
      <!-- :permanent="$vuetify.breakpoint.mdAndUp" -->
      <!-- :temporary="!$vuetify.breakpoint.mdAndUp" -->
      <v-list-item>
        <v-list-item-content>
          <v-list-item-title class="title">
            Bilolok
          </v-list-item-title>
          <v-list-item-subtitle>
            ...means kava
          </v-list-item-subtitle>
        </v-list-item-content>
      </v-list-item>
        <!-- I think this serves best as an actual menu to navigate
        save a FAB or something to open up a right side list of
        kava bars in the viewport -->
      <v-divider></v-divider>
      <v-list>
        <v-list-item
          v-show="hasAdminAccess"
          @click="goAdmin"
        >
          <v-list-item-icon>
            <v-icon>mdi-key</v-icon>
          </v-list-item-icon>
          <v-list-item-title>Admin</v-list-item-title>
        </v-list-item>
        <v-list-item
          v-for="item in items"
          :key="item.title"
          :to="item.link"
          exact
          :href="item.href"
        >
          <v-list-item-icon>
            <v-icon>{{ item.icon }}</v-icon>
          </v-list-item-icon>
          <v-list-item-title>{{ item.title }}</v-list-item-title>
        </v-list-item>
      </v-list>
      <v-divider></v-divider>

      <div v-show="isMapView">
        <v-subheader>Nakamals in view</v-subheader>
        <BoundedNakamalsList v-on:close-drawer="drawer = false"></BoundedNakamalsList>
        <v-divider></v-divider>
      </div>

      <v-list>
        <v-list-item
          dense
          v-for="item in remoteItems"
          :key="item.title"
          target="_blank"
          :href="item.href"
        >
          <v-list-item-icon>
            <v-icon>{{ item.icon }}</v-icon>
          </v-list-item-icon>
          <v-list-item-title>{{ item.title }}</v-list-item-title>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>

    <v-app-bar
      app
      dense
    >
      <v-app-bar-nav-icon
        @click="drawer = !drawer"
      ></v-app-bar-nav-icon>
        <!-- v-show="!$vuetify.breakpoint.mdAndUp" -->

      <v-toolbar-title>Bilolok</v-toolbar-title>

      <v-spacer></v-spacer>

      <v-btn
        icon
        @click="toggleDarkMode"
      >
        <v-icon v-if="darkMode">mdi-weather-sunny</v-icon>
        <v-icon v-else>mdi-weather-night</v-icon>
      </v-btn>

      <v-btn
        v-if="!isLoggedIn"
        small
        text
        outlined
        :to="{ name: 'Auth', params: { auth: 'login' } }"
      >
        Login
      </v-btn>

      <v-menu
        v-if="isLoggedIn"
        left
        bottom
        transition="slide-x-transition"
      >
        <template v-slot:activator="{ on, attrs }">
          <v-badge
            :value="!isUserVerified"
            bordered
            bottom
            color="red"
            icon="mdi-lock"
            overlap
            offset-x="20"
            offset-y="20"
          >
            <v-btn
              icon
              v-bind="attrs"
              v-on="on"
            >
              <v-icon>mdi-account</v-icon>
            </v-btn>
          </v-badge>
        </template>

        <v-list v-if="isLoggedIn">
          <v-list-item :to="{ name: 'User', params: { id: me.id } }">
            <v-list-item-icon>
              <v-icon>mdi-account</v-icon>
            </v-list-item-icon>
            <v-list-item-title>
              Profile
            </v-list-item-title>
          </v-list-item>
          <v-list-item v-if="!isUserVerified" @click="sendVerificationEmail">
            <v-list-item-icon>
              <v-icon color="red">mdi-lock</v-icon>
            </v-list-item-icon>
            <v-list-item-title>
              Send Verification Email
            </v-list-item-title>
          </v-list-item>

          <v-divider></v-divider>

          <v-list-item @click="logout">
            <v-list-item-icon>
              <v-icon>mdi-logout</v-icon>
            </v-list-item-icon>
            <v-list-item-title>
              Log Out
            </v-list-item-title>
          </v-list-item>
        </v-list>

      </v-menu>
    </v-app-bar>
  </div>
</template>

<script>
import { mapGetters } from 'vuex';
import BoundedNakamalsList from '@/components/BoundedNakamalsList.vue';

export default {
  name: 'SideBar',
  components: {
    BoundedNakamalsList,
  },
  data() {
    return {
      drawer: this.$vuetify.breakpoint.mdAndUp,
      items: [
        {
          title: 'Home',
          link: { name: 'Home' },
          icon: 'mdi-home',
        },
        {
          title: 'Map',
          link: { name: 'Map' },
          icon: 'mdi-map',
        },
        {
          title: 'About',
          link: { name: 'About' },
          icon: 'mdi-information-variant',
        },
      ],
      remoteItems: [
        {
          title: 'Follow our FB Page',
          href: 'https://www.facebook.com/bilolokapp',
          icon: 'mdi-facebook',
        },
        {
          title: 'Report A Bug',
          href: 'https://github.com/michaeltoohig/bilolok/issues',
          icon: 'mdi-bug',
        },
      ],
    };
  },
  computed: {
    ...mapGetters({
      isLoggedIn: 'auth/isLoggedIn',
      me: 'auth/user',
      hasAdminAccess: 'auth/hasAdminAccess',
      isUserVerified: 'auth/isUserVerified',
      darkMode: 'setting/darkMode',
    }),
    isMapView() {
      return this.$route.name === 'Map';
    },
  },
  methods: {
    sendVerificationEmail() {
      this.$store.dispatch('auth/requestVerification');
    },
    logout() {
      this.$store.dispatch('auth/userLogOut');
    },
    goAdmin() {
      this.$router.push({ name: 'AdminUsers' });
    },
    toggleDarkMode() {
      this.$store.dispatch('setting/setDarkMode', !this.darkMode);
    },
  },
};
</script>

<style>

</style>
