<template>
  <div class="flex grow">
    <div class="flex bg-secondary p-1 px-3 text-light h-right">
      <div class="btn btn-primary btn-sm p-0 px-1" @click="syncListSource">
        <icon icon="sync-alt"/>
      </div>
      <div class="grow" @click="changeServer">
        <icon icon="server"/>
        {{ rHost === '' ? 'http://built-in' : rHost }}
      </div>
    </div>
    <h3 class="m-3 mb-0">
      <icon icon="folder"/>
      / 이미지 소스
    </h3>
    <div class="border border-dark  mx-3"/>
    <div class="flex grow y-scroll" @dropover.stop.prevent="$event.dataTransfer.dropEffect = 'copy'" @drop="drop">
      <div class="container">
        <div class="row">
          <div v-for="s in source" :key="s" class="col-sm-3 p-0 py-3">
            <image-card :src="`${rHost}/static/source/${s}`" class=""/>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapState, mapMutations, mapActions } from 'vuex'
import ImageCard from '@/comp/ImageCard'

export default {
  mounted () {
    window.addEventListener('keypress', this.onwindowkeypress)
  },
  beforeDestroy () {
    window.removeEventListener('keypress', this.onwindowkeypress)
  },
  methods: {
    onwindowkeypress (e) {
      switch (e.key) {
        case 'r': this.syncListSource(); break
      }
    },
    changeServer () {
      var servername = prompt('api 서버 주소를 입력')
      this.setServer(servername)
    },
    drop (e) {
      e.stopPropagation()
      e.preventDefault()
      var files = e.dataTransfer.files
      console.log(files)
    },
    ...mapMutations([
      'setServer'
    ]),
    ...mapActions([
      'syncListSource'
    ])
  },
  computed: {
    ...mapState([
      'rHost',
      'source'
    ])
  },
  components: { ImageCard }
}
</script>
