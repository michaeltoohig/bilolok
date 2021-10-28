<template>
  <v-timeline
    dense
    clipped
  >
    <v-timeline-item
      fill-dot
      class="white--text mb-12"
      color="orange"
      large
    >
      <template v-slot:icon>
        <span></span>
      </template>
      <v-text-field
        v-model="input"
        hide-details
        flat
        label="Leave a comment..."
        solo
        @keydown.enter="comment"
      >
        <template v-slot:append>
          <v-btn
            class="mx-0"
            depressed
            @click="comment"
          >
            Post
          </v-btn>
        </template>
      </v-text-field>
    </v-timeline-item>

    <v-slide-x-transition
      group
    >
      <v-timeline-item
        v-for="event in timeline"
        :key="event.id"
        class="mb-4"
        color="pink"
        small
      >
        <v-row justify="space-between">
          <v-col
            cols="7"
            v-text="event.text"
          ></v-col>
          <v-col
            class="text-right"
            cols="5"
            v-text="event.time"
          ></v-col>
        </v-row>
      </v-timeline-item>
    </v-slide-x-transition>

    <v-timeline-item
      class="mb-6"
      hide-dot
    >
      <span>Not working yet</span>
    </v-timeline-item>
  </v-timeline>
</template>

<script>
export default {
  name: 'Timeline',
  data() {
    return {
      events: [],
      input: null,
      nonce: 0,
    };
  },
  computed: {
    timeline() {
      return this.events.slice().reverse();
    },
  },
  methods: {
    comment() {
      const time = (new Date()).toTimeString();
      this.events.push({
        id: this.nonce += 1,
        text: this.input,
        time,
      });
      this.input = null;
    },
  },
};
</script>

<style>

</style>
