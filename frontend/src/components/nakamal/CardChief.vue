<template>
  <v-card
    v-if="chief"
    class="mb-3"
    color="secondary darken-2"
    dark
  >
    <div class="d-flex flex-no-wrap justify-space-between">
      <div>
        <v-card-title class="text-h5 pb-0">{{ $t('nakamal.chief') }}</v-card-title>
        <v-card-text class="mt-0">
          <h5>{{ $t('nakamal.chief_checkins_this_month') }}:</h5>
          <span class="font-weight-bold text-h5">{{ userCheckinCountMonth(chief.id) }}</span>
        </v-card-text>
        <v-card-actions class="py-1">
          <v-btn
            text
            small
            color="secondary lighten-2"
            @click="show = !show"
          >
            {{ $t('nakamal.chief_what_is_this_btn') }}
          </v-btn>
        </v-card-actions>
      </div>
      <v-avatar
        class="ma-3 elevation-2 user-avatar"
        size="100"
        tile
        link
        v-ripple="{ center: true }"
        @click="$router.push({ name: 'User', params: { id: chief.id } })"
      >
        <v-img :src="chief.avatar"></v-img>
      </v-avatar>
    </div>
    <v-expand-transition>
      <v-card
        v-if="show"
        class="transition-fast-in-fast-out v-card--reveal"
        style="height: 100%;"
      >
        <v-card-text class="pb-0">
          <p class="text-h5 mb-1">
            {{ $t('nakamal.chief') }}
          </p>
          <p class="">
            {{ $t('nakamal.chief_what_is_this') }}
          </p>
        </v-card-text>
        <v-card-actions class="pt-0">
          <v-btn
            text
            color="primary lighten-2"
            @click="show = false"
          >
            {{ $t('buttons.close') }}
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-expand-transition>
  </v-card>
</template>

<script>
import { mapGetters } from 'vuex';
import dayjs from 'dayjs';

export default {
  name: 'CardChief',
  props: ['nakamal'],
  data() {
    return {
      show: false,
    };
  },
  computed: {
    ...mapGetters({
      getCheckins: 'checkin/nakamal',
    }),
    checkins() {
      return this.getCheckins(this.nakamal.id);
    },
    chief() {
      return this.nakamal.chief;
    },
  },
  methods: {
    userCheckinCountMonth(userId) {
      if (!this.checkins) return null;
      return this.checkins
        .filter((c) => dayjs(c.created_at).isAfter(dayjs().subtract(30, 'd')))
        .filter((c) => c.user === userId)
        .length;
    },
  },
};
</script>

<style>
.user-avatar {
  cursor: pointer;
}

.v-card--reveal {
  bottom: 0;
  opacity: 1 !important;
  position: absolute;
  width: 100%;
}
</style>
