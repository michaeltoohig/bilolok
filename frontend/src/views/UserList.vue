<template>
  <div class="users-list">
    <div v-if="users===null">
      <v-container fill-height>
        <v-layout align-center justify-center>
          <v-flex>
            <div class="text-center">
              <div class="headline my-5">Loading Users...</div>
              <v-progress-circular size="100" indeterminate color="primary"></v-progress-circular>
            </div>
          </v-flex>
        </v-layout>
      </v-container>
    </div>
    <div v-else>
      <v-container>
        <CardUser
          v-for="user in users"
          :key="user.id"
          :user="user"
        ></CardUser>
      </v-container>
    </div>
  </div>
</template>

<script>
import dayjs from 'dayjs';
import usersApi from '@/api/users';
import CardUser from '@/components/UserList/CardUser.vue';

export default {
  name: 'UserList',
  components: {
    CardUser,
  },
  data() {
    return {
      users: null,
    };
  },
  async mounted() {
    const resp = await usersApi.getUsers(null, { includeDetails: true });
    this.users = resp.data.filter((u) => u.latest_checkin !== null)
      .sort((a, b) => dayjs(a.latest_checkin.created_at).isBefore(b.latest_checkin.created_at));
  },
};
</script>

<style>

</style>
