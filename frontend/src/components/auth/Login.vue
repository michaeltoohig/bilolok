<template>
  <div>
    <h1>Log In</h1>
    <v-btn @click="signup">Sign Up</v-btn>

    <v-text-field
      v-model="username"
      label="Username"
    ></v-text-field>
    <v-text-field
      v-model="password"
      label="Password"
      type="password"
      @keydown.enter="submit"
    ></v-text-field>

    <v-btn @click="submit">Submit</v-btn>

  </div>
</template>

<script>
export default {
  name: 'Login',
  data() {
    return {
      username: null,
      password: null,
    };
  },
  methods: {
    signup() {
      this.$router.push({ name: 'Auth', params: { auth: 'signup' } });
    },
    submit() {
      this.$store.dispatch('auth/jwtLogin', {
        username: this.username,
        password: this.password,
      });
    },
  },
  created() {
    // Catch redirect from 401 error in axios response interceptor
    if (this.$route.query.unauthorized) {
      this.$store.dispatch('notify/add', {
        title: 'Not Authorized',
        text: 'You need to be logged in to do that.',
        type: 'error',
      });
    }
  },
};
</script>

<style>

</style>
