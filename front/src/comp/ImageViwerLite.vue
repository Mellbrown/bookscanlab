<template>
  <div class="flex grow">
    <div class="flex">
      <div class="p-1 px-3 bg-dark flex">
        <div class="mx-auto">
          <button class="btn btn-primary mx-1" @click="rotate -= 90">
            <icon icon="undo-alt"/>
          </button>
          <button class="btn btn-primary mx-1" @click="rotate += 90">
            <icon icon="redo-alt"/>
          </button>
        </div>
      </div>
    </div>
    <div
      ref="con"
      class="flex grow relative"
      style="overflow: hidden;"
      @mousewheel="mousewheel"
      @mousedown="mousedown">
      <div class="" :style="imgStyle" v-if="src">
        <img :src="src" class="frame" ref="img" draggable="false"/>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    src: { type: String, required: true },
    init: { type: Array, default: () => [] },
    pointover: { type: Number, default: () => -1 },
  },
  data () {
    return {
      width: 100,
      rotate: 0,
      ratio: 1,
      drag: false,
      mouseprex: 0,
      mouseprey: 0,
      mousex: 0,
      mousey: 0,
      left: 0,
      top: 0,
      viewBox: '',
      points: [],
      naturalWidth: 0,
      naturalHeight: 0,
      selectedButton: 0,
      toppadd: 0,
      handledragging: null
    }
  },
  mounted () {
    var m = this
    this.$nextTick(() => {
      let width = m.$refs.img.naturalWidth
      let height = m.$refs.img.naturalHeight
      m.toppadd = m.$refs.con.getBoundingClientRect().top
      m.width = width
      m.ratio = height / width
      m.naturalWidth = width
      m.naturalHeight = height
      m.$emit('source-size', [height, width])
      m.viewBox = `0 0 ${width} ${height}`
      m.points = m.init
      m.width = 600
    })
  },
  methods: {
    mousewheel (e) {
      this.width -= e.deltaY * 1.5
    },
    mousedown (e) {
      window.addEventListener('mousemove', this.mousemove)
      window.addEventListener('mouseup', this.mouseup)
      this.mouseprex = e.clientX
      this.mouseprey = e.clientY
    },
    mouseup (e) {
      window.removeEventListener('mousemove', this.mousemove)
      window.removeEventListener('mouseup', this.mouseup)
      this.mouseprex = 0
      this.mouseprey = 0
      this.left += this.mousex
      this.top += this.mousey
      this.mousex = 0
      this.mousey = 0
    },
    mousemove (e) {
      this.mousex = e.clientX - this.mouseprex
      this.mousey = e.clientY - this.mouseprey
    }
  },
  computed: {
    computedPoints,
    scale () {
      return this.naturalWidth / this.width
    },
    imgStyle () {
      return {
        position: 'absolute',
        display: 'inline-block',
        height: `${this.height}px`,
        width: `${this.width}px`,
        filter: 'drop-shadow(0px 10px 5px rgba(0,0,0,0.5));',
        transform: `translate(${this.left + this.mousex}px, ${this.top + this.mousey}px) rotate(${this.rotate}deg)`
      }
    },
    height () {
      return this.width * this.ratio
    }
  }
}
</script>
