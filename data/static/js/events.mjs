document.addEventListener("page.transitioned", (event) => {
    console.debug("Path transitioned to: ", event.detail)
})