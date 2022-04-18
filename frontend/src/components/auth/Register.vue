<template>
  <div>
    <h1>Sign Up</h1>
    <v-btn @click="login">Log In</v-btn>

    <v-text-field
      v-model.trim="email"
      label="Email"
    ></v-text-field>
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

    <v-btn :disabled="!isValid" @click="submit">Submit</v-btn>

  </div>
</template>

<script>
export default {
  name: 'Register',
  data() {
    return {
      email: null,
      password: null,
      confirmPassword: null,
    };
  },
  computed: {
    isValid() {
      if (!this.email) return false;
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
    submit() {
      this.$store.dispatch('auth/register', {
        email: this.email,
        password: this.password,
      });
    },
  },
};
</script>

<style>

</style>
