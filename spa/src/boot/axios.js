import axios from 'axios'
axios.defaults.withCredentials = true
axios.defaults.xsrfCookieName = 'csrftoken'
axios.defaults.xsrfHeaderName = 'X-CSRFToken'
const axiosInstance = axios.create({
  baseURL: '/' //  'http://submission.ucdavis.edu'// ,
})
export default async ({ Vue }) => {
  Vue.prototype.$axios = axiosInstance
}

export { axiosInstance }
