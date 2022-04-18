<template>
  <v-container>
    <div class="d-flex flex-column justify-start">
      <h3 class="text-h5">Verify My Email</h3>
      <p>
        Please click the following button to complete verification of your email address.
        Once complete, you will be able to upload images, check-in to kava bars and more.
      </p>
      <v-btn class="ma-3" large @click="verify">Verify My Email</v-btn>
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
