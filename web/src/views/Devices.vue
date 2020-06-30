<template>
  <div>
    <h1>Registered Devices</h1>
    <v-simple-table>
    <template v-slot:default>
      <thead>
        <tr>
          <th class="text-left">Id</th>
          <th class="text-left">Name</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="item in devices" :key="item.id">
          <td>{{ item.id }}</td>
          <td>{{ item.id }}</td>
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
    axios.get(constants.SocketIoService.HOST + ':' + constants.SocketIoService.PORT + '/api/device/list')
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