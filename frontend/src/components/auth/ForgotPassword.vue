<template>
  <div>
    <h1>Forgot Password</h1>
    <v-btn @click="login">Login</v-btn>

    <v-text-field
      v-model.trim="email"
      label="Email"
      :disabled="sent"
    ></v-text-field>

    <v-btn @click="submit" :disabled="sent">Submit</v-btn>

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
        title: 'Email Sent',
        text: 'An email was sent with instructions to reset your password.',
        type: 'info',
        duration: 10_000,
      });
    },
  },
};
</script>

<style>

</style>
