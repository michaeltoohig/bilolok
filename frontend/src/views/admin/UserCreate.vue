<template>
  <v-container fluid>
    <v-card class="ma-3 pa-3">
      <v-card-title primary-title>
        <div class="headline primary--text">Create User</div>
      </v-card-title>
      <v-card-text>
        <template>
          <v-form ref="form">
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
              <span v-else>(currently is not a superuser)</span>
            </div>
            <v-checkbox
              label="Is Superuser"
              v-model="isSuperuser"
            ></v-checkbox>
            <div class="subheading secondary--text text--lighten-2">
              User verified
              <span v-if="isSuperuser">(currently verified)</span>
              <span v-else>(currently not verified)</span>
            </div>
            <v-checkbox
              label="Is Verified"
              v-model="isVerified"
            ></v-checkbox>
            <div class="subheading secondary--text text--lighten-2">
              User is active
              <span v-if="isActive">(currently active)</span>
              <span v-else>(currently not active)</span>
            </div>
            <v-checkbox
              label="Is Active"
              v-model="isActive"
            ></v-checkbox>
            <v-layout align-center>
              <v-flex>
                <v-text-field
                  type="password"
                  label="Set Password"
                  v-model="$v.password1.$model"
                  :error="$v.password1.$error"
                ></v-text-field>
                <v-text-field type="password"
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
        <v-btn @click="submit">Save</v-btn>
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
  name: 'UserCreate',
  mixins: [validationMixin],
  data() {
    return {
      valid: false,
      email: '',
      isActive: true,
      isVerified: false,
      isSuperuser: false,
      setPassword: false,
      password1: '',
      password2: '',
    };
  },
  validations: {
    email: {
      required,
      email,
    },
    password1: {
      required,
      minLength: minLength(6),
    },
    password2: {
      sameAsPassword: sameAs('password1'),
    },
  },
  methods: {
    reset() {
      this.password1 = '';
      this.password2 = '';
      this.email = '';
      this.isActive = true;
      this.isVerified = false;
      this.isSuperuser = false;
      this.$v.$reset();
    },
    cancel() {
      this.$router.back();
    },
    async submit() {
      this.$v.$touch();
      if (this.$v.$invalid) return;

      const payload = {
        email: this.email,
      };
      if (this.password1) {
        payload.password = this.password1;
      }
      payload.is_active = this.isActive;
      payload.is_verified = this.isVerified;
      payload.is_superuser = this.isSuperuser;
      this.$store.dispatch('user/createUser', payload);
      this.$router.push({ name: 'AdminUsers' });
    },
  },
  async mounted() {
    this.$store.dispatch('user/getUsers');
    this.reset();
  },
};
</script>
