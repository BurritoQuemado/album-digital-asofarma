import { TweenMax, Power2 } from 'gsap'

$(() => {
    let menuIsOpened = false
    $('.Card-Footer').hide()
    function onClickQuantity() {
        const id = $(this).attr('data-id')
        const visible = $(this).attr('show') || false
        const isVisible = (visible === 'true')
        $(this).attr('show', !isVisible)
        !isVisible ? $(`.Card-Footer-${id}`).show() : $(`.Card-Footer-${id}`).hide()
    }
    function onClickMenu() {
        TweenMax.to('#Sidebar', 0.45, {
            x: !menuIsOpened ? 0 : -$('#Sidebar').outerWidth() + $('#Menu--Toggler').outerWidth(),
            onComplete: () => menuIsOpened = !menuIsOpened,
            ease: Power2.easeOut,
        })
        $('#Menu--Toggler span').text(() => {
            return !menuIsOpened ? 'Cerrar menú' : 'Ver secciones de álbum'
        })
    }
    $(window).resize(() => {
        menuIsOpened = false
        $('#Menu--Toggler span').text(() => {
            return 'Ver secciones de álbum'
        })
        TweenMax.set('#Sidebar', {
            x: -$('#Sidebar').outerWidth() + $('#Menu--Toggler').outerWidth(),
        })
    })
    const closeMenuOutside = (e) => {
        const container = $('#Sidebar')
        if (!container.is(e.target) && container.has(e.target).length === 0) {
            if (menuIsOpened) {
                TweenMax.to('#Sidebar', 0.45, {
                    x: -$('#Sidebar').outerWidth() + $('#Menu--Toggler').outerWidth(),
                    onComplete: () => menuIsOpened = false,
                    ease: Power2.easeOut,
                })
                $('#Menu--Toggler span').text(() => {
                    return 'Ver secciones de álbum'
                })
            }
        }
    }
    TweenMax.set('#Sidebar', {
        x: -$('#Sidebar').outerWidth() + $('#Menu--Toggler').outerWidth(),
    })
    $('#Menu--Toggler').click(onClickMenu)
    $('.Card-Quantity').click(onClickQuantity)
    $(document).mouseup(closeMenuOutside)
    if (window.location.hash) {
        setTimeout(() => {
            const hash = window.location.hash.substring(1)
            const $anchor = $(`#Card-${hash}`).offset()
            $(`#Card-${hash}`).addClass('NewCard')
            // console.log($anchor)
            $('html, body').animate({
                scrollTop: $anchor.top - (window.innerHeight / 4),
            }, 500)
            const uri = window.location.toString()
            if (uri.indexOf('#') > 0) {
                const cleanUri = uri.substring(0, uri.indexOf('#'))
                window.history.replaceState({}, document.title, cleanUri)
            }
        }, 500)
    }
})
