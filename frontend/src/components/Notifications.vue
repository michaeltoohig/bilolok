<template>
  <transition-group name="notification-list" tag="div" class="top-right">
    <v-alert
      v-for="(alert, i) in alerts"
      :key="i"
      :color="alert.type"
      border="left"
      elevation="2"
      min-width="300"
      colored-border
      @click="dismiss(alert)"
    >
      <div class="text-h6">
        {{ alert.title }}
      </div>
      <div>{{ alert.text }}</div>
    </v-alert>
  </transition-group>
</template>

<script>
export default {
  name: 'Notifications',
  computed: {
    alerts() {
      return this.$store.getters['notify/notifications'];
    },
  },
  methods: {
    dismiss(alert) {
      this.$store.dispatch('notify/dismiss', alert);
    },
  },
  // created() {
  //   this.$store.dispatch('notify/add', {
  //     title: 'Hello',
  //     text: 'World',
  //     type: 'primary',
  //     duration: 3000,
  //   });
  //   this.$store.dispatch('notify/add', {
  //     title: 'Hello 2',
  //     text: 'World 2',
  //     type: 'error',
  //     duration: 5000,
  //   });
  // },
};
</script>

<style lang="scss" scoped>
$margin: 15px;

.notification-wrapper {
  position: fixed;
}

.top-right {
    top: $margin;
    right: $margin;
    left: auto;
    width: 300px;
    //height: 600px;
    position: fixed;
    opacity: 0.95;
    z-index: 100;
    display: flex;
    flex-wrap: wrap;
    //background-color: red;
}

.slide-enter {
  opacity: 0;
}

.slide-move {
  transition: transform 1s;
}

.slide-enter-active {
  animation: slide-in 0.5s ease-out forwards;
  transition: opacity 0.5s;
}

.slide-leave-active {
  position: absolute;
  width: 100%;
  animation: slide-out 0.5s ease-out forwards;
  transition: opacity 0.5s;
  opacity: 0;
}

@keyframes slide-in {
  from {
    transform: translateY(-20px);
  }
  to {
    transform: translateY(0px);
  }
}

@keyframes slide-out {
  from {
    transform: translateX(0px);
  }
  to {
    transform: translateX(350px);
  }
}

.notification-list-enter,
.notification-list-leave-active {
    opacity: 0;
    transform: translateX(-90px);
}
.notification-list-leave-active {
    position: absolute;
}
</style>
