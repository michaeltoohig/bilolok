<template>
  <div>Verifying Email...</div>
</template>

<script>
export default {
  name: 'Verify',
  methods: {
    home() {
      this.$router.push({ name: 'Home' });
    },
  },
  async created() {
    const { token } = this.$route.query;
    if (!token) {
      this.$store.dispatch('notify/add', {
        title: 'Missing Token',
        text: 'Missing email verification token in request.',
        type: 'error',
      });
    } else {
      await this.$store.dispatch('auth/verify', token);
    }
    this.home();
  },
};
</script>

<style>

</style>
