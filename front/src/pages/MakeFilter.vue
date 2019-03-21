<template>
  <div class="flex grow container-fluid">
    <div class="row grow">
      <div class="col-md-6 bg-danger flex grow m-1 card">

      </div>
      <div class="col-md-3 bg-info flex grow m-1 card">

      </div>
      <div class="col-md-3 flex grow m-1 p-0">
        <filter-inspector />
      </div>
    </div>
  </div>
</template>

<script>
import FilterInspector from '@/comp/FilterInspector'

export default {
  components: { FilterInspector }
}
</script>
