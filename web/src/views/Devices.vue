<template>
  <div>
    <v-tabs v-model="ActiveTab" background-color="blue-grey lighten-4" centered>
      <v-tab v-for="name in TabNames" v-bind:key="name">{{ name }}</v-tab>
    </v-tabs>
    <v-tabs-items v-model="ActiveTab">
      <v-tab-item>
        <DeviceList/>
      </v-tab-item>
      <v-tab-item>
        <v-lazy>
          <DeviceGroupList/>
        </v-lazy>
      </v-tab-item>
      <v-tab-item>
        3
      </v-tab-item>
    </v-tabs-items>
  </div>
</template>

<script>
import { mapGetters} from 'vuex'
import constants from '../constants'
import DeviceList from '../components/DeviceList'
import DeviceGroupList from '../components/DeviceGroupList'

export default {
  components: {
    DeviceList,
    DeviceGroupList
  },
  data: () => ({
    TabNames: ['Devices', 'Device Groups', 'Policies'],
    ActiveTab: null
  }),
  mounted() {
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