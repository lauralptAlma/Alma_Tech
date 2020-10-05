function replaceAll(find, replace, str) {
    return str.replace(new RegExp(find, 'g'), replace);
}

/*Crea la estructura del odontograma*/
function createOdontogram() {
    var htmlLecheLeft = "",
        htmlLecheRight = "",
        htmlLeft = "",
        htmlRight = "",
        a = 1;
    for (var i = 9 - 1; i >= 1; i--) {
        //Dientes Definitivos Cuandrante Derecho (Superior/Inferior)
        let claseDiente = "diente";
        if (i == 8 || i == 1) {
            claseDiente = "primer-diente";
        }
        htmlRight += '<div data-name="value" id="dienteindex' + i + '" class=' + claseDiente + '>' +
            '<span style="margin-left: 45px; margin-bottom:5px; display: inline-block !important; border-radius: 10px !important;" class="badge badge-pill badge-info">index' + i + '</span>' +
            '<div id="tindex' + i + '" class="cuadro click">' +
            '</div>' +
            '<div id="lindex' + i + '" class="cuadro izquierdo click">' +
            '</div>' +
            '<div id="bindex' + i + '" class="cuadro debajo click">' +
            '</div>' +
            '<div id="rindex' + i + '" class="cuadro derecha click click">' +
            '</div>' +
            '<div id="cindex' + i + '" class="centro click">' +
            '</div>' +
            '</div>';
        //Dientes Definitivos Cuandrante Izquierdo (Superior/Inferior)
        htmlLeft += '<div id="dienteindex' + a + '" class=' + claseDiente + '>' +
            '<span style="margin-left: 45px; margin-bottom:5px; display: inline-block !important; border-radius: 10px !important;" class="badge badge-pill badge-info">index' + a + '</span>' +
            '<div id="tindex' + a + '" class="cuadro click">' +
            '</div>' +
            '<div id="lindex' + a + '" class="cuadro izquierdo click">' +
            '</div>' +
            '<div id="bindex' + a + '" class="cuadro debajo click">' +
            '</div>' +
            '<div id="rindex' + a + '" class="cuadro derecha click click">' +
            '</div>' +
            '<div id="cindex' + a + '" class="centro click">' +
            '</div>' +
            '</div>';
        if (i <= 5) {
            //Dientes Temporales Cuandrante Derecho (Superior/Inferior)
            htmlLecheRight += '<div id="dienteLindex' + i + '" style="left: -25%;" class="diente-leche">' +
                '<span style="margin-left: 45px; margin-bottom:5px; display: inline-block !important; border-radius: 10px !important;" class="badge badge-pill label-alma">index' + i + '</span>' +
                '<div id="tlecheindex' + i + '" class="cuadro-leche top-leche click">' +
                '</div>' +
                '<div id="llecheindex' + i + '" class="cuadro-leche izquierdo-leche click">' +
                '</div>' +
                '<div id="blecheindex' + i + '" class="cuadro-leche debajo-leche click">' +
                '</div>' +
                '<div id="rlecheindex' + i + '" class="cuadro-leche derecha-leche click click">' +
                '</div>' +
                '<div id="clecheindex' + i + '" class="centro-leche click">' +
                '</div>' +
                '</div>';
        }
        if (a < 6) {
            let claseDienteLeche = "diente-leche";
            if (a == 1) {
                claseDienteLeche = "primer-diente-leche";
            }
            //Dientes Temporales Cuandrante Izquierdo (Superior/Inferior)
            htmlLecheLeft += '<div id="dienteLindex' + a + '" class=' + claseDienteLeche + '>' +
                '<span style="margin-left: 45px; margin-bottom:5px; display: inline-block !important; border-radius: 10px !important;" class="badge badge-pill label-alma">index' + a + '</span>' +
                '<div id="tlecheindex' + a + '" class="cuadro-leche top-leche click">' +
                '</div>' +
                '<div id="llecheindex' + a + '" class="cuadro-leche izquierdo-leche click">' +
                '</div>' +
                '<div id="blecheindex' + a + '" class="cuadro-leche debajo-leche click">' +
                '</div>' +
                '<div id="rlecheindex' + a + '" class="cuadro-leche derecha-leche click click">' +
                '</div>' +
                '<div id="clecheindex' + a + '" class="centro-leche click">' +
                '</div>' +
                '</div>';
        }
        a++;
    }
    $("#tr").append(replaceAll('index', '1', htmlRight));
    $("#tl").append(replaceAll('index', '2', htmlLeft));
    $("#tlr").append(replaceAll('index', '5', htmlLecheRight));
    $("#tll").append(replaceAll('index', '6', htmlLecheLeft));


    $("#bl").append(replaceAll('index', '3', htmlLeft));
    $("#br").append(replaceAll('index', '4', htmlRight));
    $("#bll").append(replaceAll('index', '7', htmlLecheLeft));
    $("#blr").append(replaceAll('index', '8', htmlLecheRight));
}

/* Cuando se carga la página, crea el odontograma y según el botón seleccionado y la pieza en que se hizo click
* se le agrega la clase correspondiente a dicha pieza */
$(document).ready(function () {
    createOdontogram();
    $(".click").click(function (event) {
        var control = $("#controls").children().find('.active').attr('id');
        var cuadro = $(this).find("input[name=cuadro]:hidden").val();
        switch (control) {
            case "cariado":
                if ($(this).hasClass("filled-tooth")) {
                    $(this).removeClass('filled-tooth');
                    $(this).addClass('decayed-tooth');
                } else if ($(this).hasClass("missing-tooth")) {
                    $(this).parent().children().each(function (index, el) {
                        $(el).removeClass("missing-tooth");
                    });
                    $(this).addClass('decayed-tooth');
                } else if ($(this).hasClass("lacking-tooth")) {
                    $(this).parent().children().each(function (index, el) {
                        $(el).removeClass("lacking-tooth");
                    });
                    $(this).addClass('decayed-tooth');
                } else {
                    if ($(this).hasClass("decayed-tooth")) {
                        $(this).removeClass('decayed-tooth');
                    } else {
                        $(this).addClass('decayed-tooth');
                    }
                }
                break;
            case "obturado":
                if ($(this).hasClass("decayed-tooth")) {
                    $(this).removeClass('decayed-tooth');
                    $(this).addClass('filled-tooth');
                } else if ($(this).hasClass("missing-tooth")) {
                    $(this).parent().children().each(function (index, el) {
                        $(el).removeClass("missing-tooth");
                    });
                    $(this).addClass('filled-tooth');
                } else if ($(this).hasClass("lacking-tooth")) {
                    $(this).parent().children().each(function (index, el) {
                        $(el).removeClass("lacking-tooth");
                    });
                    $(this).addClass('filled-tooth');
                } else {
                    if ($(this).hasClass("filled-tooth")) {
                        $(this).removeClass('filled-tooth');
                    } else {
                        $(this).addClass('filled-tooth');
                    }
                }
                break;
            case "perdido":
                var dientePosition = $(this).position();
                $(this).parent().children().each(function (index, el) {
                    if ($(el).hasClass("click")) {
                        if ($(el).hasClass("missing-tooth")) {
                            $(el).removeClass("missing-tooth");
                        } else if ($(el).hasClass("filled-tooth")) {
                            $(el).removeClass("filled-tooth");
                            $(el).addClass('missing-tooth');
                        } else if ($(el).hasClass("decayed-tooth")) {
                            $(el).removeClass("decayed-tooth");
                            $(el).addClass('missing-tooth');
                        } else if ($(el).hasClass("lacking-tooth")) {
                            $(el).removeClass("lacking-tooth");
                            $(el).addClass('missing-tooth');
                        } else {
                            $(el).addClass('missing-tooth');
                        }
                    }
                });
                break;
            case "ausente":
                var dientePosition = $(this).position();
                $(this).parent().children().each(function (index, el) {
                    if ($(el).hasClass("click")) {
                        if ($(el).hasClass("lacking-tooth")) {
                            $(el).removeClass("lacking-tooth");
                        } else if ($(el).hasClass("filled-tooth")) {
                            $(el).removeClass("filled-tooth");
                            $(el).addClass('lacking-tooth');
                        } else if ($(el).hasClass("decayed-tooth")) {
                            $(el).removeClass("decayed-tooth");
                            $(el).addClass('lacking-tooth');
                        } else if ($(el).hasClass("missing-tooth")) {
                            $(el).removeClass("missing-tooth")
                            $(el).addClass('lacking-tooth');
                        } else {
                            $(el).addClass('lacking-tooth');
                        }
                    }
                });
                break
            default:
                console.log("borrar case");
        }
        return false;
    });
    return false;
});

/* Al presionar Guardar obtiene el id de los elementos que tienen como atributo las clases correspondientes
* a cariado, obturado, perdido o ausente y los almacena en un string con formato JSON. Al finalizar quita
* la última coma y le asigna el valor del CPO al elemento correspondiente para ser almacenado. */
function obtenerCPO() {
    //let dientes = '{"cariados":[';
    const caries = [];
    const cariados = $('.decayed-tooth');
    cariados.each(function (index, element) {
        let idCarie = `"${$(element).attr('id')}"`;
        caries.push(idCarie);
        //dientes += '"' + idCarie + '"' + ','
    });
    //dientes += '],"obturados":[';
    const obturaciones = [];
    const obturados = $('.filled-tooth');
    obturados.each(function (index, element) {
        let idObturado = `"${$(element).attr('id')}"`;
        //dientes += '"' + idObturado + '"' + ','
        obturaciones.push(idObturado)
    });
    //dientes += '],"perdidos":[';
    const perdidas = [];
    const perdidos = $('.missing-tooth');
    perdidos.each(function (index, element) {
        let idPerdido = `"${$(element).attr('id')}"`;
        //dientes += '"' + idPerdido + '"' + ','
        perdidas.push(idPerdido)
    });
    //dientes += '],"ausentes":[';
    const ausente = [];
    const ausentes = $('.lacking-tooth');
    ausentes.each(function (index, element) {
        let idAusente = `"${$(element).attr('id')}"`;
        //dientes += '"' + idAusente + '"' + ','
        ausente.push(idAusente)
    });
    //dientes = dientes.substring(0, dientes.length - 1);
    //dientes += ']}'
    let dientes = `{"cariados":[${caries}],"obturados":[${obturaciones}],"perdidos":[${perdidas}],"ausentes":[${ausente}]}`;
    $("#id_contenido_cpo").val(dientes)
    console.log(dientes)
}
