<template>
  <v-app>
    <v-app-bar
      app
      color="blue"
      flat
    >
      <v-container class="py-0 fill-height">
        <h1 class="pr-4">
          ASPATH
        </h1>
        <v-btn
          v-for="(item, i) in items"
          :key="i"
          :to="item.to"
          text
          class="mr-1"
        >
          {{ item.title }}
        </v-btn>
      </v-container>
    </v-app-bar>
    <v-main>
      <div class="header pt-2" style="background-color: #2196F3 !important; padding-bottom: 4.1rem;">
        <v-container>
          <v-row>
            <v-col class="py-0">
              <v-text-field
                dense
                flat
                hide-details
                rounded
                solo-inverted
                style="max-width: 500px;"
              />
            </v-col>
          </v-row>
          <v-row>
            <v-col>
              <v-breadcrumbs
                class="pl-1 pt-0 pb-0 breadcrumbs"
                :items="crumbs"
                divider="-"
              />
            </v-col>
          </v-row>
          <v-row no-gutters>
            <slot name="subtitle" />
          </v-row>
        </v-container>
      </div>

      <v-container style="margin-top: -4.5rem; background-color: white; border-radius: 3px;">
        <nuxt />
      </v-container>
    </v-main>
    <v-footer
      :absolute="!fixed"
      app
    >
      <span>&copy; {{ new Date().getFullYear() }}</span>
    </v-footer>
  </v-app>
</template>

<script>
export default {
  data () {
    return {
      clipped: false,
      drawer: false,
      fixed: false,
      items: [
        {
          icon: 'mdi-apps',
          title: 'Home',
          to: '/'
        },
        {
          icon: 'mdi-chart-bubble',
          title: 'Internet Exchanges',
          to: '/internet-exchanges'
        },
        {
          icon: 'mdi-chart-bubble',
          title: 'Route Collectors',
          to: '/route-collectors'
        }
      ],
      crumbs: [
        {
          disabled: false,
          text: 'Home',
          href: '/'
        }
      ],
      miniVariant: false,
      right: true,
      rightDrawer: false,
      title: 'ASPATH'
    }
  },
  created () {
    const urlParams = this.$route.fullPath.substring(1).split('/')
    let path = ''
    urlParams.forEach((param, index) => {
      path = `${path}/${param}`
      this.crumbs.push({ disabled: false, text: param, href: path })
    })
  }

}
</script>
<style>
a.v-breadcrumbs__item {
  color: black;
}
</style>
