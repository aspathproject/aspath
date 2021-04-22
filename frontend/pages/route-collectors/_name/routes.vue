<template>
  <v-row justify="center" align="start">
    <v-col md="4">
      <h3 class="mb-4">
        Filters:
      </h3>

      <v-text-field
        v-model="cidrBlockFilter"
        label="IP Block:"
        outlined
        clearable
        :rules="[validCIDR]"
      />
      <v-text-field
        v-model="asPathFilter"
        label="AS Path contains:"
        outlined
        clearable
      />
      <v-text-field
        v-model="originFilter"
        label="Origin AS:"
        outlined
        clearable
      />
      <p>Prefix Length:</p>
      <v-range-slider
        v-model="prefixLengthRange"
        :max="maxPrefixLength"
        :min="minPrefixLength"
        hide-details
        class="align-center"
      >
        <template #prepend>
          <v-text-field
            :value="prefixLengthRange[0]"
            class="mt-0 pt-0"
            hide-details
            single-line
            type="number"
            style="width: 60px"
            @change="$set(prefixLengthRange, 0, $event)"
          />
        </template>
        <template #append>
          <v-text-field
            :value="prefixLengthRange[1]"
            class="mt-0 pt-0"
            hide-details
            single-line
            type="number"
            style="width: 60px"
            @change="$set(prefixLengthRange, 1, $event)"
          />
        </template>
      </v-range-slider>
    </v-col>
    <v-col cols="12" sm="8" md="8">
      <v-card>
        <v-card-text>
          <v-row no-gutters class="routes-header">
            <v-col cols="3" xs="3" md="2">
              <h4>IP Block</h4>
            </v-col>
            <v-col class="hidden-md-and-down">
              <h4>AS Path</h4>
            </v-col>
            <v-col>
              <h4>Origin</h4>
            </v-col>
          </v-row>
          <v-virtual-scroll
            height="500"
            item-height="16"
            :items="filteredRoutes"
            style="overflow-y: overlay;"
          >
            <template #default="{ item }">
              <v-row no-gutters class="route-item black--text">
                <v-col cols="3" md="2">
                  {{ item.block }}
                </v-col>
                <v-col class="text-truncate hidden-md-and-down">
                  {{ item.path.join(', ') }}
                </v-col>
                <v-col class="text-truncate">
                  {{ item.origin }} - {{ item.name }}
                </v-col>
              </v-row>
            </template>
          </v-virtual-scroll>
          <hr class="my-3">
          <div class="text-xs-right">
            <em><small>Showing {{ filteredRoutes.length }} routes.</small></em>
          </div>
        </v-card-text>
      </v-card>
    </v-col>
  </v-row>
</template>

<script>
import * as ipaddr from 'ipaddr.js'

export default {
  components: {
  },
  data: () => ({
    announcements: [],
    loading: true,
    originFilter: null,
    asPathFilter: null,
    cidrBlockFilter: null,
    validatedCIDRBlock: null,
    minPrefixLength: 1,
    maxPrefixLength: 48,
    prefixLengthRange: [1, 48]
  }),
  async fetch () {
    this.announcements = await this.$http.$get(
      `/route-collectors/${this.$route.params.name}/snapshots/${this.$route.query.snapshot}/routes`
    )

    if (!this.announcements) {
      this.$nuxt.error({ statusCode: 404, message: 'Data not found' })
    }
  },
  computed: {
    filteredRoutes () {
      if (!this.announcements) {
        return []
      }
      return this.announcements.filter((route) => {
        if (this.originFilter) {
          const originName = route.name ? route.name.toLowerCase() : ''
          return route.origin === this.originFilter || originName.includes(this.originFilter.toLowerCase())
        }
        return true
      }).filter((route) => {
        if (this.asPathFilter) {
          const aspath = route.path.join(' ').toLowerCase()
          return aspath.includes(this.asPathFilter.toLowerCase())
        }
        return true
      }).filter((route) => {
        const prefixLength = parseInt(route.block.split('/')[1])
        return (this.prefixLengthRange[0] <= prefixLength) && (prefixLength <= this.prefixLengthRange[1])
      }).filter((route) => {
        if (this.validatedCIDRBlock) {
          try {
            const cidr = ipaddr.IPv4.networkAddressFromCIDR(route.block)
            return cidr.match(this.validatedCIDRBlock)
          } catch (error) {
            return false
          }
        }
        return true
      })
    }
  },
  watch: {

  },
  created () {
    if (!this.$route.query.snapshot) {
      this.$router.push({ query: { snapshot: 'latest' } })
    }
  },
  methods: {
    validCIDR (value) {
      if (!value || value.length === 0) {
        this.validatedCIDRBlock = null
        return true
      }
      try {
        this.validatedCIDRBlock = ipaddr.parseCIDR(value)
        return true
      } catch (error) {
        return 'not a valid CIDR'
      }
    }
  }
}
</script>

<style>
  .route-item {
    font-size: 12px;
    font-weight: 400;
    line-height: 16px;
    /*outline: 1px solid black;*/
    box-shadow: 0 1px 0 rgb(0 0 0 / 20%) inset;
  }
  .route-item:hover {
    background-color: #f7f7f7;
  }
</style>
