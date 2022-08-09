<template>
  <div>
    <h1>{{ $t('auth.register') }}</h1>

    <v-text-field
      v-model.trim="email"
      :label="$t('auth.email')"
    ></v-text-field>
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

    <v-btn :disabled="!isValid" @click="submit">{{ $t('buttons.submit') }}</v-btn>

    <v-alert
      v-show="!isValid"
      border="top"
      colored-border
      type="info"
      elevation="2"
      class="mt-6"
      transition="scroll-y-transition"
      mode="in-out"
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
