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

    <h1>{{ $t('auth.forgot_password') }}</h1>

    <v-text-field
      v-model.trim="email"
      :label="$t('auth.email')"
      :disabled="sent"
    ></v-text-field>

    <v-btn @click="submit" :disabled="sent">{{ $t('buttons.submit') }}</v-btn>

  </div>
</template>

<script>
import authApi from '@/api/auth';

export default {
  name: 'ForgotPassword',
  data() {
    return {
      email: null,
      sent: false,
    };
  },
  methods: {
    login() {
      this.$router.push({ name: 'Auth', params: { auth: 'login' } });
    },
    async submit() {
      this.sent = true;
      await authApi.forgotPassword({ email: this.email });
      this.$store.dispatch('notify/add', {
        title: this.$i18n.t('auth.alert.email_verification_sent_title'),
        text: this.$i18n.t('auth.alert.email_verification_sent_body'),
        type: 'info',
        duration: 10_000,
      });
    },
  },
};
</script>

<style>

</style>
