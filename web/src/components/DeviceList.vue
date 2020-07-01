<template>
  <div>
    <v-toolbar dense flat>
      <v-toolbar-title>Registered Devices</v-toolbar-title>
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
    axios.get(constants.SocketIoService.HOST + ':' + constants.SocketIoService.PORT + '/api/device/list')
    .then((resp) => {
      console.log(resp.data)
      this.devices = resp.data
    }).catch ((err) => {
      console.error(err)
    })
  },
  computed: {
  },
  watch: {
  }
}
</script>
