<template>
  <v-row justify="center" align="start">
    <v-col cols="12">
      <v-row no-gutters>
        <h1>Internet Exchanges</h1>
        <v-row v-if="internet_exchanges.length === 0" justify="center" align="center">
          <v-col>
            <v-card class="text-center my-8">
              <v-card-text><span class="text-primary text-body-1">No internet exchanges found</span></v-card-text>
            </v-card>
          </v-col>
        </v-row>
      </v-row>
      <v-row>
        <v-col>
          <v-row
            v-for="exchange in internet_exchanges"
            :key="exchange.id"
          >
            <v-col>
              <NuxtLink :to="exchange.slug" style="text-decoration: none">
                <v-hover
                  v-slot="{ hover }"
                >
                  <v-card
                    class="pa-6 my-1"
                    :elevation="hover ? 3 : 2"
                  >
                    <v-row align="center" class="spacer">
                      <v-col
                        cols="4"
                        sm="2"
                        md="1"
                      >
                        <v-avatar size="48px" color="red">
                          <span class="white--text headline">IXP</span>
                        </v-avatar>
                      </v-col>
                      <v-col
                        sm="5"
                        md="3"
                      >
                        <h3>{{ exchange.name }}</h3>
                      </v-col>
                      <v-spacer />
                      <v-col
                        sm="5"
                        md="3"
                      >
                        <p class="mb-0">
                          route collectors: <span>{{ exchange.route_collectors }}</span>
                        </p>
                        <p class="mb-0">
                          last updated: <span>{{ exchange.last_snapshot_date }}</span>
                        </p>
                      </v-col>
                      <v-col v-if="exchange.last_snapshot_collector_name">
                        <NuxtLink
                          style="text-decoration: none; color: inherit;"
                          :to="'/route-collectors/' + exchange.last_snapshot_collector_name + '/routes?snapshot=' + exchange.last_snapshot_id"
                        >
                          <v-btn>Go to last snapshot</v-btn>
                        </NuxtLink>
                      </v-col>
                    </v-row>
                  </v-card>
                </v-hover>
              </NuxtLink>
            </v-col>
          </v-row>
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
    internet_exchanges: [
      {
        name: 'PIT Chile',
        route_collectors: 1,
        prefix_count: '15.000',
        last_snapshot: 'december 23th, 2020',
        slug: 'pit-chile'
      },
      {
        name: 'IX.BR',
        route_collectors: 0,
        prefix_count: 'unknown',
        last_snapshot: 'never',
        slug: 'ix-br'
      }
    ]
  }),
  async fetch () {
    this.internet_exchanges = await this.$http.$get('/exchange-points')
  }
}
</script>
