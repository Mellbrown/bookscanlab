<template>
  <div id="app">
    <nav class="navbar navbar-expand-sm navbar-light bg-info">
      <router-link class="navbar-brand" to="/">
        북스캐너 LAB 
        <icon icon="flask" class="ml-1"/>
      </router-link>
      <ul class="navbar-nav mr-auto">
        <li class="nav-item">
          <router-link class="nav-link" to="/makefilter">필터</router-link>
        </li>
        <li class="nav-item">
          <router-link class="nav-link" to="/modify-poly">폴리 수정</router-link>
        </li>
      </ul>
    </nav>
    <router-view />
    <div class="bg-dark text-light px-2">
      selected source : "{{ selectedSource }}"
    </div>
  </div>
</template>

<script>
import { mapState, mapMutations } from 'vuex'
export default {
  methods: {
    ...mapMutations([
      'selectSource'
    ])
  },
  computed: {
    ...mapState([
      'selectedSource'
    ])
  }
}
</script>


<style lang="scss" scoped>
.navbar-brand{
  font-weight: bold;
}
</style>
