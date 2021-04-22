<template>
  <div>
    <v-card>
      <v-card-title class="headline">
        ASPATH Pre-release
      </v-card-title>
      <v-card-text>
        <p>
          <b>Warning:</b>
          Unexpected software behavior should definitely be expected on alpha builds. Kindly submit an issue on
          <a href="https://github.com/aspathproject/aspath/issues">ASPATH Github repo</a>
          in case a bug is discovered.
        </p>
      </v-card-text>
    </v-card>
    <h2 class="mt-2">Database Statistics</h2>
    <div v-if="statistics" style="display: flex">
      <div style="display: flex">
        <v-card class="my-2 mr-2 text-center">
          <div
            class="pa-2 py-4"
            style="display: flex; flex-direction: column; align-items: center; max-width: 200px;"
          >
            <span style="font-weight:900; font-size: 48px;">{{ statistics.route_collector_count }}</span>
            <span>Route collectors</span>
          </div>
        </v-card>
      </div>
      <div style="display: flex">
        <v-card class="my-2 mr-2 text-center">
          <div
            class="pa-2 py-4"
            style="display: flex; flex-direction: column; align-items: center; max-width: 200px;"
          >
            <span style="font-weight:900; font-size: 48px;">{{ statistics.ixp_count }}</span>
            <span>Internet Exchange Points</span>
          </div>
        </v-card>
      </div>
      <div>
        <v-card class="my-2 mr-2 text-center">
          <div
            class="pa-2 py-4"
            style="display: flex; flex-direction: column; align-items: center; max-width: 200px;"
          >
            <span style="font-weight:900; font-size: 48px;">{{ statistics.snapshots_count }}</span>
            <span>Routing snapshots</span>
          </div>
        </v-card>
      </div>
      <div>
        <v-card class="my-2 mr-2 text-center">
          <div
            class="pa-2 py-4"
            style="display: flex; flex-direction: column; align-items: center; max-width: 200px;"
          >
            <span style="font-weight:900; font-size: 48px;">{{ statistics.autonomous_systems }}</span>
            <span>Autonomous Systems</span>
          </div>
        </v-card>
      </div>
    </div>
  </div>
</template>

<script>

export default {
  components: {
  },
  data () {
    return {
      statistics: null
    }
  },
  async fetch () {
    this.statistics = await this.$http.$get('/statistics')
  }
}
</script>
