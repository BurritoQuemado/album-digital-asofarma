$(() => {
    $('.Card-Footer').hide()
    function onClickQuantity() {
        const id = $(this).attr('data-id')
        const visible = $(this).attr('show') || false
        const isVisible = (visible === 'true')
        $(this).attr('show', !isVisible)
        !isVisible ? $(`.Card-Footer-${id}`).show() : $(`.Card-Footer-${id}`).hide()
    }
    console.info('>> init')
    $('.Card-Quantity').click(onClickQuantity)
})
