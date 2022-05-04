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
          {{ $t('auth.register_available') }}
        </v-col>
        <v-col class="shrink">
          <v-btn @click.prevent="signup">{{ $t('auth.register') }}</v-btn>
        </v-col>
      </v-row>
    </v-alert>

    <h1>{{ $t('auth.login') }}</h1>

    <v-text-field
      v-model.trim="username"
      :label="$t('auth.email')"
    ></v-text-field>
    <v-text-field
      v-model="password"
      :label="$t('auth.password')"
      type="password"
      @keydown.enter="submit"
    ></v-text-field>

    <v-btn @click="submit">{{ $t('buttons.submit') }}</v-btn>

    <a href="#" class="ml-3" @click.prevent="forgotPassword">{{ $t('auth.forgot_password') }}</a>
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
    forgotPassword() {
      this.$router.push({ name: 'Auth', params: { auth: 'forgotPassword' } });
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
