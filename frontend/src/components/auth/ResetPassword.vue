<template>
  <div>
    <h1>Reset Password</h1>
    <v-btn @click="login">Login</v-btn>

    <v-text-field
      v-model="password"
      label="Password"
      type="password"
    ></v-text-field>
    <v-text-field
      v-model="confirmPassword"
      label="Confirm Password"
      type="password"
    ></v-text-field>

    <v-btn @click="submit" :disabled="!isValid">Submit</v-btn>

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
          title: 'Password Reset',
          text: 'You may now login with your new password.',
          type: 'info',
          duration: 10_000,
        });
      } catch (error) {
        if (error.response.data.detail === 'RESET_PASSWORD_BAD_TOKEN') {
          this.$store.dispatch('notify/add', {
            title: 'Password Reset Failed',
            text: 'The password reset link is invalid or expired.',
            type: 'warning',
            duration: 10_000,
          });
        } else {
          this.$store.dispatch('notify/add', {
            title: 'Password Reset Failed',
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
        title: 'Missing Token',
        text: 'You may not reset your password without a valid token.',
        type: 'error',
      });
      this.login();
    }
  },
};
</script>

<style>

</style>
