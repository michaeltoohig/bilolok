<template>
  <v-container fluid>
    <v-card class="ma-3 pa-3">
      <v-card-title primary-title>
        <div class="headline primary--text">Edit User</div>
      </v-card-title>
      <v-card-text>
        <template>
          <div class="my-3">
            <div class="subheading secondary--text text--lighten-2">Username</div>
            <div
              class="title primary--text text--darken-2"
              v-if="user"
            >{{user.email}}</div>
            <div
              class="title primary--text text--darken-2"
              v-else
            >-----</div>
          </div>
          <v-form
            v-model="valid"
            ref="form"
            lazy-validation
          >
            <v-text-field
              label="E-mail"
              type="email"
              v-model.trim="$v.email.$model"
              :error="$v.email.$error"
              required
            ></v-text-field>
            <div class="subheading secondary--text text--lighten-2">
              User is superuser
              <span v-if="isSuperuser">(currently is a superuser)</span>
              <span v-else>(currently is not a superuser)</span></div>
            <v-checkbox
              label="Is Superuser"
              v-model="isSuperuser"
            ></v-checkbox>
            <div class="subheading secondary--text text--lighten-2">
              User is verified
              <span v-if="isSuperuser">(currently verified)</span>
              <span v-else>(currently not verified)</span></div>
            <v-checkbox
              label="Is Verified"
              v-model="isVerified"
            ></v-checkbox>
            <div class="subheading secondary--text text--lighten-2">
              User is active
              <span v-if="isActive">(currently active)</span>
              <span v-else>(currently not active)</span></div>
            <v-checkbox
              label="Is Active"
              v-model="isActive"
            ></v-checkbox>
            <v-layout align-center>
              <v-flex shrink>
                <v-checkbox
                  v-model="setPassword"
                  class="mr-2"
                ></v-checkbox>
              </v-flex>
              <v-flex>
                <v-text-field
                  :disabled="!setPassword"
                  type="password"
                  label="Set Password"
                  v-model="$v.password1.$model"
                  :error="$v.password1.$error"
                ></v-text-field>
                <v-text-field type="password"
                  :disabled="!setPassword"
                  label="Confirm Password"
                  v-model="$v.password2.$model"
                  :error="$v.password2.$error"
                ></v-text-field>
              </v-flex>
            </v-layout>
          </v-form>
        </template>
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn @click="cancel">Cancel</v-btn>
        <v-btn @click="reset">Reset</v-btn>
        <v-btn
          @click="submit"
          :disabled="!valid"
        >
          Save
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-container>
</template>

<script>
import {
  validationMixin,
} from 'vuelidate';
import {
  required,
  email,
  minLength,
  sameAs,
} from 'vuelidate/lib/validators';

export default {
  name: 'UserEdit',
  mixins: [validationMixin],
  data() {
    return {
      valid: true,
      email: '',
      isActive: true,
      isVerified: false,
      isSuperuser: false,
      setPassword: false,
      password1: '',
      password2: '',
    };
  },
  validations() {
    const valid = {
      email: {
        required,
        email,
      },
      password1: {},
      password2: {},
    };
    if (this.setPassword) {
      valid.password1 = {
        required,
        minLength: minLength(6),
      };
      valid.password2 = {
        sameAsPassword: sameAs('password1'),
      };
    }
    return valid;
  },
  computed: {
    user() {
      return this.$store.getters['user/find'](this.$router.currentRoute.params.id);
    },
  },
  methods: {
    reset() {
      this.setPassword = false;
      this.password1 = '';
      this.password2 = '';
      this.$v.$reset();
      if (this.user) {
        this.email = this.user.email;
        this.isActive = this.user.is_active;
        this.isVerified = this.user.is_verified;
        this.isSuperuser = this.user.is_superuser;
      }
    },
    cancel() {
      this.$router.back();
    },
    submit() {
      this.$v.$touch();
      if (this.$v.$invalid) return;

      const payload = {
        email: this.email,
      };
      if (this.setPassword) {
        payload.password = this.password1;
      }
      payload.is_active = this.isActive;
      payload.is_verified = this.isVerified;
      payload.is_superuser = this.isSuperuser;
      this.$store.dispatch('user/updateUser', { userId: this.user.id, payload });
      this.$router.push({ name: 'AdminUsers' });
    },
  },
  async mounted() {
    this.$store.dispatch('user/loadOne', this.$router.currentRoute.params.id, { auth: true });
    this.reset();
  },
};
</script>
