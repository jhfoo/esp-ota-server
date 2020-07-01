<template>
  <div>
    <v-toolbar dense flat>
      <v-toolbar-title>Device Groups</v-toolbar-title>
      <v-spacer></v-spacer>
      <v-btn icon>
        <v-icon>mdi-magnify</v-icon>
      </v-btn>
      <v-btn icon>
        <v-icon>mdi-heart</v-icon>
      </v-btn>
      <v-btn icon>
        <v-icon>mdi-dots-vertical</v-icon>
      </v-btn>
    </v-toolbar>

    <v-simple-table>
      <template v-slot:default>
        <thead>
          <tr>
            <th class="text-left">Id</th>
            <th class="text-left">Name</th>
            <th class="text-left">Group Token</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in devices" :key="item.id">
            <td>{{ item.id }}</td>
            <td>{{ item.name }}</td>
            <td>{{ item.GroupToken }}</td>
          </tr>
        </tbody>
      </template>
    </v-simple-table>
  </div>
</template>

<script>
import { mapGetters} from 'vuex'
import constants from '../constants'
import axios from 'axios'

export default {
  data: () => ({
    devices: []
  }),
  mounted() {
    axios.get(constants.SocketIoService.HOST + ':' + constants.SocketIoService.PORT + '/api/devicegroup/list')
    .then((resp) => {
      console.log(resp.data)
      this.devices = resp.data
    }).catch ((err) => {
      console.error(err)
    })
  },
  computed: {
    ...mapGetters(['SocketIoStatus']),
  },
  watch: {
    SocketIoStatus(NewValue, OldValue) {
      console.log('Watched IsSocketIoConnected: %s => %s', OldValue, NewValue)
      this.isSocketIoConnected = NewValue === constants.SocketIoStatus.CONNECTED
    }
  }
};
</script>