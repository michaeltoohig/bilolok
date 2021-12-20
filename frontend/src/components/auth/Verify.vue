<template>
  <div>
    <v-btn class="ma-3" large @click="verify">Verify My Email</v-btn>
  </div>
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
        title: 'Missing Token',
        text: 'Missing email verification token in request.',
        type: 'error',
      });
      this.home();
    }
  },
};
</script>

<style>

</style>
