import Vue from 'vue'
import Router from 'vue-router'

import MakeFilter from '@/pages/MakeFilter'
import ListSource from '@/pages/ListSource'
import ModifyPoly from '@/pages/ModifyPoly'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      component: ListSource
    },
    {
      path: '/makefilter',
      component: MakeFilter
    },
    {
      path: '/modify-poly',
      component: ModifyPoly
    }
  ]
})
