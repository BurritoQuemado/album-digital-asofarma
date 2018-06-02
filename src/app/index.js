$(() => {
    $('.Card-Footer').hide()
    function onClickQuantity() {
        const id = $(this).attr('data-id')
        const visible = $(this).attr('show') || false
        const isVisible = (visible === 'true')
        $(this).attr('show', !isVisible)
        !isVisible ? $(`.Card-Footer-${id}`).show() : $(`.Card-Footer-${id}`).hide()
    }
    $('.Card-Quantity').click(onClickQuantity)
    if (window.location.hash) {
        setTimeout(() => {
            const hash = window.location.hash.substring(1)
            const $anchor = $(`#Card-${hash}`).offset()
            console.log($anchor)
            $('html, body').animate({
                scrollTop: $anchor.top - (window.innerHeight / 2),
            }, 500)
            const uri = window.location.toString()
            if (uri.indexOf('#') > 0) {
                const cleanUri = uri.substring(0, uri.indexOf('#'))
                window.history.replaceState({}, document.title, cleanUri)
            }
        }, 500)
    }
})
