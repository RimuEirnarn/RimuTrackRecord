import { Notification } from "../vendor/enigmarimu.js/notification.mjs"
import { Template } from "../vendor/enigmarimu.js/template.mjs"
import { config } from "../vendor/enigmarimu.js/config.mjs"

config.target.notification = "#alert"
const notification = new Notification()
notification.setTemplate(await Template.with_url("toast-notify", "template/notification.html", 100))
notification.setInitiator((notification_id) => {
  const toast = document.querySelector(`[data-id="${notification_id}"]`)

  const toastBootstrap = bootstrap.Toast.getOrCreateInstance(toast, {delay: 1500})
  toastBootstrap.show()
})

export { notification }