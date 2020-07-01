<template>
  <div>
    Every device should report a globally unique identifier, regardless of hardware. Devices failing 
    to ping within 30min intervals are considered stale and incommunicable.
    <v-toolbar dense flat>
      <v-toolbar-title>Registered Devices</v-toolbar-title>
      <v-spacer></v-spacer>
      <v-btn icon>
        <v-icon>mdi-magnify</v-icon>
      </v-btn>
      <v-btn @click="updateList" color="green" text>
        <v-icon>mdi-refresh</v-icon> Refresh
      </v-btn>
      <v-btn @click="resetTable" text color="red">
        <v-icon>mdi-nuke</v-icon> Reset
      </v-btn>
    </v-toolbar>

    <v-simple-table>
      <template v-slot:default>
        <thead>
          <tr>
            <th class="text-left">Id</th>
            <th class="text-left">Last Known Ip</th>
            <th class="text-left">Last Ping</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in devices" :key="item.id">
            <td>{{ item.id }}</td>
            <td>{{ item.LastKnownIp }}</td>
            <td>{{ item.LastPing ? item.LastPing : 'NA'}}</td>
          </tr>
        </tbody>
      </template>
    </v-simple-table>
  </div>
</template>

<script>
import constants from '../constants'
import axios from 'axios'

export default {
  data: () => ({
    devices: [],
    ActiveTab: 0
  }),
  mounted() {
    this.updateList()
  },
  methods: {
    resetTable() {
      axios.get(constants.SocketIoService.HOST + ':' + constants.SocketIoService.PORT + '/api/device/reset')
      .then((resp) => {
        console.log(resp.data)
        this.updateList()
      }).catch ((err) => {
        console.error(err)
      })
    },
    updateList() {
      this.devices = []

      axios.get(constants.SocketIoService.HOST + ':' + constants.SocketIoService.PORT + '/api/device/list')
      .then((resp) => {
        console.log(resp.data)
        this.devices = resp.data
      }).catch ((err) => {
        console.error(err)
      })
    }
  },
  computed: {
  },
  watch: {
  }
}
</script>
