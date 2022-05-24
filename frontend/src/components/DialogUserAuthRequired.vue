<template>
  <div>
    <v-dialog
      v-model="showUserVerifiedModal"
      persistent
      max-width="400"
    >
      <v-card>
        <v-card-title>{{ $t('auth.alert.email_verification_required_title') }}</v-card-title>
        <v-card-subtitle>
          {{ $t('auth.alert.email_verification_required_subtitle') }}
        </v-card-subtitle>
        <div class="d-flex justify-center">
          <v-icon size="100">mdi-email-alert</v-icon>
        </div>
        <v-card-text>
          <p>{{ $t('auth.alert.email_verification_required_body') }}</p>
        </v-card-text>
        <v-card-actions>
          <v-btn text @click="closeUserVerifiedModal">
            {{ $t('buttons.close') }}
          </v-btn>
          <v-spacer></v-spacer>
          <v-btn
            text
            outlined
            color="primary"
            @click="sendVerificationEmail"
          >
            {{ $t('auth.send_verification_email') }}
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-dialog
      v-model="showAuthModal"
      persistent
      max-width="400"
    >
      <v-card>
        <v-card-title>{{ $t('auth.alert.auth_required_title') }}</v-card-title>
        <v-card-subtitle>
          {{ $t('auth.alert.auth_required_subtitle') }}
        </v-card-subtitle>
        <v-card-text>
          <p>{{ $t('auth.alert.auth_required_body') }}</p>
        </v-card-text>
        <v-card-actions>
          <v-btn
            text
            outlined
            @click="goToLogin"
          >
            {{ $t('auth.login') }}
          </v-btn>
          <v-btn
            text
            outlined
            @click="goToSignup"
          >
            {{ $t('auth.register') }}
          </v-btn>
          <v-spacer></v-spacer>
          <v-btn text @click="closeAuthModal">
            {{ $t('buttons.close') }}
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
import { mapGetters } from 'vuex';

export default {
  name: 'DialogUserAuthRequired',
  computed: {
    ...mapGetters({
      showAuthModal: 'auth/showAuthModal',
      showUserVerifiedModal: 'auth/showUserVerifiedModal',
    }),
  },
  methods: {
    closeAuthModal() {
      this.$store.dispatch('auth/setShowAuthModal', false);
    },
    closeUserVerifiedModal() {
      this.$store.dispatch('auth/setShowUserVerifiedModal', false);
    },
    goToLogin() {
      this.closeAuthModal();
      this.$router.push({ name: 'Auth', params: { auth: 'login' } });
    },
    goToSignup() {
      this.closeAuthModal();
      this.$router.push({ name: 'Auth', params: { auth: 'signup' } });
    },
    sendVerificationEmail() {
      this.$store.dispatch('auth/requestVerification');
    },
  },
};
</script>

<style>

</style>
