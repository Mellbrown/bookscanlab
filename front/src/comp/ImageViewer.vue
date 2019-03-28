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
          <div class="btn-group ml-3" role="group">
            <button type="button" :class="buttonSelected[0]" @click="selectedButton=0">
              <icon icon="draw-polygon"/>
            </button>
            <button type="button" :class="buttonSelected[1]" @click="selectedButton=1">
              <icon icon="plus"/>
            </button>
            <button type="button" :class="buttonSelected[2]" @click="selectedButton=2">
              <icon icon="fist-raised"/>
            </button>
            <button type="button" :class="buttonSelected[3]" @click="selectedButton=3">
              <icon icon="minus"/>
            </button>
          </div>
        </div>
      </div>
    </div>
    <div
      ref="con"
      class="flex grow relative"
      style="overflow: hidden;"
      @mousewheel="mousewheel"
      @mousedown="mousedown">
      <div class="" :style="imgStyle" @click.ctrl="pick" v-if="src">
        <img :src="src" class="frame" ref="img" draggable="false"/>
        <svg :viewBox="viewBox" xmlns="http://www.w3.org/2000/svg" class="frame" v-if="viewBox">
          <polygon :points="txtPoints" stroke="green" fill="transparent" stroke-width="3"/>
          <polygon :points="computedPoints.txt" stroke="yellow" fill="transparent" stroke-width="3" v-if="visible3dpaper"/>
        </svg>
        <div class="frame" v-if="visible3dpaper">
          <div class="handle" :style="{
            left: p.x / scale + 'px',
            top: p.y / scale + 'px',
            border: i === pointover ? 'solid 4px green' : ''
            }" v-for="(p, i) in computedPoints.raw" :key="i">
            <div class="midcen border border-danger" style="height: 5px; width: 5px; border-width: 5pt"></div>
          </div>
        </div>
        <div class="absolute in-block border border-primary" :style="{
          height: '10px',
          width: '10px',
          borderWidth: '10pt',
          left: page3d.camerax / scale + 'px',
          top: page3d.cameray / scale + 'px'
          }" v-if="visible3dpaper">
        </div>
        <div class="frame">
          <div class="handle" :style="{
            left: p.x / scale + 'px',
            top: p.y / scale + 'px',
            border: i === pointover ? 'solid 4px green' : ''
            }" v-for="(p, i) in points" :key="i"
            @click="handleclick($event, i)"
            @mousedown.prevent.stop="handledrag($event, i)">
            <div class="midcen border border-danger" style="height: 5px; width: 5px; border-width: 5pt"></div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
function computedPoints () {
  var m = this.page3d
  var chop = m.depth.length - 1
  var w = m.width / chop

  var points = [[], []]
  // Top Line
  for (let i = 0; chop >= i; i++) {
    points[0].push({ x: m.x + w * i, y: m.y, z: m.depth[i] })
    points[1].push({ x: m.x + w * i, y: m.y + m.height, z: m.depth[i] })
  }
  points[1].reverse()
  points = points[0].concat(points[1])

  // Pojection Transformation
  points = points.map(p => {
    return {
      x: (p.x - m.camerax) / p.z + m.camerax,
      y: (p.y - m.cameray) / p.z + m.cameray
    }
  })

  return {
    raw: points,
    txt: points.map(p => p.x + ',' + p.y).join(' ')
  }
}

export default {
  props: {
    src: { type: String, required: true },
    init: { type: Array, default: () => [] },
    pointover: { type: Number, default: () => -1 },
    page3d: { type: Object, required: true },
    visible3dpaper: { type: Boolean, default: () => false }
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
      leftpadd: 0,
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
      m.leftpadd = m.$refs.con.getBoundingClientRect().left
      m.width = width
      m.ratio = height / width
      m.naturalWidth = width
      m.naturalHeight = height
      m.$emit('source-size', [height, width])
      m.viewBox = `0 0 ${width} ${height}`
      window.addEventListener('keypress', this.onwindowkeypress)
      m.points = m.init
      m.width = 600
    })
  },
  beforeDestroy () {
    window.removeEventListener('keypress', this.onwindowkeypress)
  },
  methods: {
    mouse2imgScale (x, y) {
      x -= this.left + this.leftpadd
      y -= this.top + this.toppadd
      return { x: x * this.scale, y: y * this.scale }
    },
    handledrag (e, i) {
      if (this.selectedButton === 2) {
        this.handledragging = {
          target: i,
          ...this.mouse2imgScale(e.clientX, e.clientY)
        }
        window.addEventListener('mousemove', this.handlemove)
        window.addEventListener('mouseup', this.handleup)
      } else if (this.selectedButton === 1) {
        this.points.splice(i, 0, { ...this.points[i] })
        this.points = this.points.filter(() => true)
        this.handledragging = {
          target: i,
          ...this.mouse2imgScale(e.clientX, e.clientY)
        }
        window.addEventListener('mousemove', this.handlemove)
        window.addEventListener('mouseup', this.handleup)
      }
    },
    handlemove (e) {
      this.handledragging = {
        ...this.handledragging,
        ...this.mouse2imgScale(e.clientX, e.clientY)
      }
    },
    handleup (e) {
      window.removeEventListener('mousemove', this.handlemove)
      window.removeEventListener('mouseup', this.handleup)
      this.points[this.handledragging.target] = {
        x: parseInt(this.handledragging.x),
        y: parseInt(this.handledragging.y)
      }
      this.handledragging = null
      this.points = this.points.filter(() => true)
      console.log('end')
    },
    handleclick (e, i) {
      if (this.selectedButton === 3) {
        console.log(i + 'delete')
        this.points = this.points.filter((p, idx) => {
          if (idx !== i) return true
        })
      }
    },
    pick (e) {
      var mousex = e.clientX
      var mousey = e.clientY
      mousex -= this.left + this.leftpadd
      mousey -= this.top + this.toppadd
      mousex *= this.scale
      mousey *= this.scale
      mousex = parseInt(mousex)
      mousey = parseInt(mousey)
      function dist (x2, y2) {
        var x1 = mousex
        var y1 = mousey
        return Math.pow(x2 - x1, 2) + Math.pow(y2 - y1, 2)
      }
      if (this.points.length !== 0) {
        var closer = { target: 0, dist: dist(this.points[0].x, this.points[0].y) }
        for (var i = 1; this.points.length > i; i++) {
          var d = dist(this.points[0].x, this.points[0].y)
          if (closer.dist > d) {
            closer = {
              target: i,
              dist: d
            }
          }
        }

        var prevIdx = closer.target - 1 < 0 ? this.points.length - 1 : closer.target - 1
        var nextIdx = closer.target + 1 < this.points.length ? closer.target + 1 : 0
        var prevDist = dist(this.points[prevIdx].x, this.points[prevIdx].y)
        var nextDist = dist(this.points[nextIdx].x, this.points[nextIdx].y)

        this.points.splice(prevDist < nextDist ? closer.target : closer.target + 1, 0, { x: mousex, y: mousey })
        this.points = this.points.filter(() => true)
      } else {
        this.points = [{ x: mousex, y: mousey }]
      }
    },
    mousewheel (e) {
      this.width -= e.deltaY * 1.5
    },
    onwindowkeypress (e) {
      switch (e.keyCode) {
        case 113: this.selectedButton = 0; break
        case 119: this.selectedButton = 1; break
        case 101: this.selectedButton = 2; break
        case 114: this.selectedButton = 3; break
      }
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
  watch: {
    points () {
      this.$emit('points-changed', this.points)
    }
  },
  computed: {
    computedPoints,
    scale () {
      return this.naturalWidth / this.width
    },
    buttonSelected () {
      return [
        ['btn', (this.selectedButton !== 0 ? 'btn-secondary' : 'btn-light')],
        ['btn', (this.selectedButton !== 1 ? 'btn-secondary' : 'btn-light')],
        ['btn', (this.selectedButton !== 2 ? 'btn-secondary' : 'btn-light')],
        ['btn', (this.selectedButton !== 3 ? 'btn-secondary' : 'btn-light')]
      ]
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
    },
    txtPoints () {
      var dr = this.handledragging
      return this.points.map((p, i) => {
        if (dr !== null && dr.target === i) {
          return dr.x + ',' + dr.y
        }
        return p.x + ',' + p.y
      }).join(' ')
    }
  }
}
</script>

<style lang="scss" scoped>
.handle {
  position: absolute;
  height: 30px;
  width: 30px;
  border-radius: 15px;
  transform: translate(-50%, -50%);
  cursor: pointer;

  &:hover {
    border: solid 4px green;
  }
}
</style>
