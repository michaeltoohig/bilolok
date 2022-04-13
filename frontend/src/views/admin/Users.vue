/* eslint-disable */

<template>
  <div class="admin-users">
    <div>
      <v-toolbar light>
        <v-toolbar-title>
          Manage Users
        </v-toolbar-title>
        <v-spacer></v-spacer>
        <v-btn color="primary" :to="{ name: 'AdminUsersCreate' }">Create User</v-btn>
      </v-toolbar>
      <v-data-table :headers="headers" :items="users">
        <template slot="items" slot-scope="props">
          <td>{{ props.item.email }}</td>
          <td><v-icon v-if="props.item.is_active">checkmark</v-icon></td>
          <td><v-icon v-if="props.item.is_verified">checkmark</v-icon></td>
          <td><v-icon v-if="props.item.is_superuser">checkmark</v-icon></td>
        </template>
        <template v-slot:item.actions="{ item }">
          <v-btn icon :to="{ name: 'AdminUsersEdit', params: { id: item.id } }">
            <v-icon
              small
            >
              mdi-pencil
            </v-icon>
          </v-btn>
        </template>
      </v-data-table>
    </div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex';

export default {
  name: 'Users',
  data() {
    return {
      headers: [
        {
          text: 'Email',
          sortable: true,
          value: 'email',
          align: 'left',
        },
        {
          text: 'Is Active',
          sortable: true,
          value: 'is_active',
          align: 'left',
        },
        {
          text: 'Is Verified',
          sortable: true,
          value: 'is_verified',
          align: 'left',
        },
        {
          text: 'Is Superuser',
          sortable: true,
          value: 'is_superuser',
          align: 'left',
        },
        { text: 'Actions', value: 'actions', sortable: false },
      ],
    };
  },
  computed: {
    ...mapGetters({
      users: 'user/list',
    }),
  },
  async mounted() {
    await this.$store.dispatch('user/getUsers', { auth: true });
  },
};
</script>
