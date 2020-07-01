<template>
  <div>
    Devices in the same Device Group receive the same software updates. They should in most cases 
    belong to the same hardware and configuration.
    <v-toolbar dense flat>
      <v-toolbar-title>Device Groups</v-toolbar-title>
      <v-spacer></v-spacer>
      <v-btn icon>
        <v-icon>mdi-magnify</v-icon>
      </v-btn>
      <v-btn @click="updateList" color="green" text>
        <v-icon>mdi-refresh</v-icon> Refresh
      </v-btn>
      <v-btn text color="red">
        <v-icon>mdi-nuke</v-icon> Reset
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
    this.updateList()
  },
  computed: {
    ...mapGetters(['SocketIoStatus']),
  },
  methods: {
    updateList() {
      this.devices = []
      axios.get(constants.SocketIoService.HOST + ':' + constants.SocketIoService.PORT + '/api/devicegroup/list')
      .then((resp) => {
        console.log(resp.data)
        this.devices = resp.data
      }).catch ((err) => {
        console.error(err)
      })
    }
  },
  watch: {
    SocketIoStatus(NewValue, OldValue) {
      console.log('Watched IsSocketIoConnected: %s => %s', OldValue, NewValue)
      this.isSocketIoConnected = NewValue === constants.SocketIoStatus.CONNECTED
    }
  }
};
</script>