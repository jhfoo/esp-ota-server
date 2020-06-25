<template>
  <v-app>
    <v-app-bar app color="primary" flat dense dark>
      <v-btn href="https://github.com/vuetifyjs/vuetify/releases/latest" target="_blank" text>
        <span class="mr-2">Latest Release</span>
        <v-icon>mdi-open-in-new</v-icon>
      </v-btn>
      <v-spacer></v-spacer>
      <v-btn href="https://github.com/vuetifyjs/vuetify/releases/latest" target="_blank" text>
        <span class="mr-2">{{ isSocketIoConnected ? 'CONNECTED' : 'OOPS' }}</span>
        <v-icon>mdi-open-in-new</v-icon>
      </v-btn>
    </v-app-bar>

    <v-main>
      <HelloWorld/>
    </v-main>
  </v-app>
</template>

<script>
import { mapGetters} from 'vuex'
import HelloWorld from './components/HelloWorld'
import constants from './constants'

export default {
  name: 'App',

  components: {
    HelloWorld,
  },

  data: () => ({
    isSocketIoConnected: false
  }),
  mounted() {
    this.isSocketIoConnected = this.$store.getters.IsSocketIoConnected
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
