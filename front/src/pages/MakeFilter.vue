<template>
  <div class="flex grow container-fluid h-left p-0">
      <image-viewer-lite
        class="col-md-8 flex grow bg-secondary p-0 m-0"
        :images="images" />
      <filteres class="col-md-4 flex grow m-0 p-0" @loaded="loaded = $event" />
  </div>
</template>

<script>
import ImageViewerLite from '@/comp/ImageViewerLite'
import Filteres from '@/comp/Filteres'
import { mapState } from 'vuex'

export default {
  data () {
    return {
      loaded: null
    }
  },
  computed: {
    images () {
      console.log(this.loaded)
      return [
        'source/' + this.selectedSource,
        ...(
          this.loaded === null ? [] : 
          this.loaded.images.map(img => 'filter/' + img)
        )
      ].reverse()
    },
    ...mapState([
      'selectedSource'
    ])
  },
  components: { ImageViewerLite, Filteres }
}
</script>
