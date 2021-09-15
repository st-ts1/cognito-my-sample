import Vue from 'vue'
import Element from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
import locale from 'element-ui/lib/locale/lang/ja'

// 参考: https://element-plus.org/#/jp/component/i18n
// あってそうだが、上手く日本語になっていない。。。
Vue.use(Element, { locale })
