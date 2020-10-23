function ultimoCPO() {
    const lastCpo = JSON.parse($('#cpo_ultimo').attr('value'));
    for (let i = 0; i < lastCpo.cariados.length; i++) {
        console.log(lastCpo.cariados[i])
        $(`#${lastCpo.cariados[i]}`).addClass('decayed-tooth');
    }
    for (let i = 0; i < lastCpo.obturados.length; i++) {
        $(`#${lastCpo.obturados[i]}`).addClass('filled-tooth');
    }
    for (let i = 0; i < lastCpo.perdidos.length; i++) {
        $(`#${lastCpo.perdidos[i]}`).addClass('missing-tooth');
    }
    for (let i = 0; i < lastCpo.ausentes.length; i++) {
        $(`#${lastCpo.ausentes[i]}`).addClass('lacking-tooth');
    }


}

$(document).ready(function () {
    ultimoCPO()
});