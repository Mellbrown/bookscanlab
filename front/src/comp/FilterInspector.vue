<template>
  <div class="flex grow bg-secondary card">
    <div class="border-bottom border-dark p-2 px-3 flex h-left baseline">
      <div class="btn btn-secondary btn-sm" @click="isShowSetter=false">
        <icon icon="arrow-left"/>
      </div>
      <h5 class="m-0 ml-3 p-0 mt-auto mb-1">{{ action_txt }}</h5>
      <div class="flex grow h-right">
        <div class="btn btn-primary btn-sm" @click="isShowSetter=true">
          <icon icon="plus"/>
        </div>
      </div>
    </div>
    <div class="p-2 px-3 flex grow">
      <filter-setter v-if="isShowSetter"/>
      <div v-else>
        asdf
      </div>
    </div>
  </div>
</template>

<script>
import FilterSetter from './FilterSetter'

export default {
  data () {
    return {
      action_txt: 'Root',
      isShowSetter: false
    }
  },
  methods: {

  },
  mounted () {

  },
  components: { FilterSetter }
}
</script>
