<template>
  <v-row justify="center" align="start">
    <v-col cols="12">
      <v-row no-gutters>
        <h1>Route Collectors</h1>
      </v-row>
      <v-row v-if="route_collectors.length === 0 || !route_collectors" justify="center" align="center">
        <v-col>
          <v-card class="text-center my-8">
            <v-card-text><span class="text-primary text-body-1">No route collectors found.</span></v-card-text>
          </v-card>
        </v-col>
      </v-row>
      <v-row>
        <v-col>
          <v-card
            v-for="collector in route_collectors"
            :key="collector.id"
            max-width="344"
          >
            <v-list-item three-line>
              <v-list-item-content>
                <div class="overline mb-4">
                  Route collector
                </div>
                <v-list-item-title class="headline mb-1">
                  {{ collector.name }}
                </v-list-item-title>
                <v-list-item-subtitle>last snapshot: {{ collector.last_snapshot_date || 'never' }}</v-list-item-subtitle>
              </v-list-item-content>
            </v-list-item>
            <v-card-actions>
              <NuxtLink
                v-if="collector.last_snapshot_id"
                style="text-decoration: none; color: inherit;"
                :to="'/route-collectors/' + collector.name + '/routes?snapshot=' + collector.last_snapshot_id"
              >
                <v-btn
                  color="primary"
                >
                  Go to last snapshot
                </v-btn>
              </NuxtLink>
              <v-btn v-else>
                No snapshot available
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-col>
      </v-row>
    </v-col>
  </v-row>
</template>

<script>

export default {
  components: {
  },
  data: () => ({
    route_collectors: []
  }),
  async fetch () {
    this.route_collectors = await this.$http.$get('/route-collectors/')
  }
}
</script>
