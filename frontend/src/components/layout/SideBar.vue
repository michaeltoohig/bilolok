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
            {{ $t('tagline') }}
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
          <v-list-item-title>{{ $t('menu.admin') }}</v-list-item-title>
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
          <v-list-item-title>{{ $t(item.title) }}</v-list-item-title>
        </v-list-item>
      </v-list>
      <v-divider></v-divider>

      <div v-if="isMapView">
        <v-subheader>{{ $t('menu.nakamals_in_view') }}</v-subheader>
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
          <v-list-item-title>{{ $t(item.title) }}</v-list-item-title>
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

      <SelectLocale />

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
        {{ $t('auth.login') }}
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
            icon="mdi-email-alert"
            overlap
            offset-x="10"
            offset-y="10"
          >
            <v-avatar
              v-bind="attrs"
              v-on="on"
              size="30"
            >
              <img :src="userAvatar">
            </v-avatar>
          </v-badge>
        </template>

        <v-list v-if="isLoggedIn && me">
          <v-list-item :to="{ name: 'User', params: { id: me.id } }">
            <v-list-item-icon>
              <v-icon>mdi-account</v-icon>
            </v-list-item-icon>
            <v-list-item-title>
              {{ $t('user.profile') }}
            </v-list-item-title>
          </v-list-item>
          <v-list-item v-if="!isUserVerified" @click="sendVerificationEmail">
            <v-list-item-icon>
              <v-icon color="red">mdi-email-alert</v-icon>
            </v-list-item-icon>
            <v-list-item-title>
              {{ $t('auth.send_verification_email') }}
            </v-list-item-title>
          </v-list-item>

          <v-divider></v-divider>

          <v-list-item @click="logout">
            <v-list-item-icon>
              <v-icon>mdi-logout</v-icon>
            </v-list-item-icon>
            <v-list-item-title>
              {{ $t('auth.logout') }}
            </v-list-item-title>
          </v-list-item>
        </v-list>

      </v-menu>
    </v-app-bar>
  </div>
</template>

<script>
import { mapGetters } from 'vuex';
import SelectLocale from '@/components/layout/SelectLocale.vue';
import BoundedNakamalsList from '@/components/layout/BoundedNakamalsList.vue';

export default {
  name: 'SideBar',
  components: {
    SelectLocale,
    BoundedNakamalsList,
  },
  data() {
    return {
      drawer: this.$vuetify.breakpoint.mdAndUp,
      items: [
        {
          title: 'menu.home',
          link: { name: 'Home' },
          icon: 'mdi-home',
        },
        {
          title: 'menu.map',
          link: { name: 'Map' },
          icon: 'mdi-map',
        },
        {
          title: 'menu.users',
          link: { name: 'UserList' },
          icon: 'mdi-account-box-multiple',
        },
        {
          title: 'menu.about',
          link: { name: 'About' },
          icon: 'mdi-information-variant',
        },
      ],
      remoteItems: [
        {
          title: 'menu.fb_page',
          href: 'https://www.facebook.com/bilolokapp',
          icon: 'mdi-facebook',
        },
        {
          title: 'menu.fb_group',
          href: 'https://www.facebook.com/groups/573807847105108',
          icon: 'mdi-facebook',
        },
        // {
        //   title: 'Report A Bug',
        //   href: 'https://github.com/michaeltoohig/bilolok/issues',
        //   icon: 'mdi-bug',
        // },
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
    userAvatar() {
      if (!this.isLoggedIn) return null;
      return this.$store.getters['user/find'](this.me.id).avatar;
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
      this.$store.dispatch('setting/updateDarkMode', !this.darkMode);
    },
    toggleLang() {
      console.log('lang', this.$i18n.locale);
      this.$i18n.locale = 'bi';
    },
  },
};
</script>

<style>

</style>
