<template>
  <div>
    <v-alert
      border="top"
      colored-border
      type="info"
      elevation="2"
    >
      <v-row align="center">
        <v-col class="grow">
          {{ $t('auth.login_available') }}
        </v-col>
        <v-col class="shrink">
          <v-btn @click.prevent="login">{{ $t('auth.login') }}</v-btn>
        </v-col>
      </v-row>
    </v-alert>

    <h1>{{ $t('auth.reset_password') }}</h1>

    <v-text-field
      v-model="password"
      :label="$t('auth.password')"
      type="password"
    ></v-text-field>
    <v-text-field
      v-model="confirmPassword"
      :label="$t('auth.confirm_password')"
      type="password"
    ></v-text-field>

    <v-btn @click="submit" :disabled="!isValid">{{ $t('auth.submit') }}</v-btn>

  </div>
</template>

<script>
import authApi from '@/api/auth';

export default {
  name: 'ResetPassword',
  data() {
    return {
      token: null,
      password: null,
      confirmPassword: null,
    };
  },
  computed: {
    isValid() {
      if (!this.token) return false;
      if (!this.password) return false;
      if (this.password.length < 6) return false;
      if (this.password !== this.confirmPassword) return false;
      return true;
    },
  },
  methods: {
    login() {
      this.$router.push({ name: 'Auth', params: { auth: 'login' } });
    },
    async submit() {
      try {
        await authApi.resetPassword({ token: this.token, password: this.password });
        this.$store.dispatch('notify/add', {
          title: this.$i18n.t('auth.alert.password_reset_success_title'),
          text: this.$i18n.t('auth.alert.password_reset_success_body'),
          type: 'info',
          duration: 10_000,
        });
      } catch (error) {
        if (error.response.data.detail === 'RESET_PASSWORD_BAD_TOKEN') {
          this.$store.dispatch('notify/add', {
            title: this.$i18n.t('auth.alert.password_reset_fail_title'),
            text: this.$i18n.t('auth.alert.password_reset_fail_body'),
            type: 'warning',
            duration: 10_000,
          });
        } else {
          this.$store.dispatch('notify/add', {
            title: this.$i18n.t('auth.alert.password_reset_fail_title'),
            text: error.response.data.detail,
            type: 'warning',
            duration: 10_000,
          });
        }
      }
      this.login();
    },
  },
  created() {
    this.token = this.$route.query.token;
    if (!this.token) {
      this.$store.dispatch('notify/add', {
        title: this.$i18n.t('auth.alert.password_reset_missing_token_title'),
        text: this.$i18n.t('auth.alert.password_reset_missing_token_body'),
        type: 'error',
      });
      this.login();
    }
  },
};
</script>

<style>

</style>
