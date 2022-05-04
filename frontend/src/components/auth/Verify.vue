<template>
  <v-container>
    <div class="d-flex flex-column justify-start">
      <h3 class="text-h5">{{ $t('auth.verify_email') }}</h3>
      <p>{{ $t('auth.verify_email_body') }}</p>
      <v-btn class="ma-3" large @click="verify">{{ $t('auth.verify_email') }}</v-btn>
    </div>
  </v-container>
</template>

<script>
export default {
  name: 'Verify',
  data() {
    return {
      token: null,
    };
  },
  methods: {
    home() {
      this.$router.push({ name: 'Home' });
    },
    async verify() {
      await this.$store.dispatch('auth/verify', this.token);
      this.home();
    },
  },
  async created() {
    this.token = this.$route.query.token;
    if (!this.token) {
      this.$store.dispatch('notify/add', {
        title: this.$i18n.t('auth.alert.email_verification_missing_token_title'),
        text: this.$i18n.t('auth.alert.email_verification_missing_token_body'),
        type: 'error',
      });
      this.home();
    }
  },
};
</script>

<style>

</style>
