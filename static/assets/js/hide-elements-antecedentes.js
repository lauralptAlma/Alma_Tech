/* En el caso de los Antecedentes clínicos los campos de descripción serán visibles
* según la opción seleccionada por el usuario */
$('label[for=id_desc_aparato_digestivo]').hide();
$('#id_desc_aparato_digestivo').hide();
$("#id_aparato_digestivo").change(function () {
    if ($(this).val() == "SI") {
        $('label[for=id_desc_aparato_digestivo]').show();
        $('#id_desc_aparato_digestivo').show();
        $('#id_desc_aparato_digestivo').attr('required', '');
        $('#id_desc_aparato_digestivo').attr('data-error', 'Este campo es requerido.');
    } else {
        $('label[for=id_desc_aparato_digestivo]').hide();
        $('#id_desc_aparato_digestivo').hide();
        $('#id_desc_aparato_digestivo').removeAttr('required');
        $('#id_desc_aparato_digestivo').removeAttr('data-error');
    }
});
$('label[for=id_desc_alergias]').hide();
$('#id_desc_alergias').hide();
$("#id_alergias").change(function () {
    if ($(this).val() == "SI") {
        $('label[for=id_desc_alergias]').show();
        $('#id_desc_alergias').show();
        $('#id_desc_alergias').attr('required', '');
        $('#id_desc_alergias').attr('data-error', 'Este campo es requerido.');
    } else {
        $('label[for=id_desc_alergias]').hide();
        $('#id_desc_alergias').hide();
        $('#id_desc_alergias').removeAttr('required');
        $('#id_desc_alergias').removeAttr('data-error');
    }
});
$('label[for=id_desc_autoinmnunes]').hide();
$('#id_desc_autoinmnunes').hide();
$("#id_autoinmnunes").change(function () {
    if ($(this).val() == "SI") {
        $('label[for=id_desc_autoinmnunes]').show();
        $('#id_desc_autoinmnunes').show();
        $('#id_desc_autoinmnunes').attr('required', '');
        $('#id_desc_autoinmnunes').attr('data-error', 'Este campo es requerido.');
    } else {
        $('label[for=id_desc_autoinmnunes]').hide();
        $('#id_desc_autoinmnunes').hide();
        $('#id_desc_autoinmnunes').removeAttr('required');
        $('#id_desc_autoinmnunes').removeAttr('data-error');
    }
});
$('label[for=id_desc_oncologicas]').hide();
$('#id_desc_oncologicas').hide();
$("#id_oncologicas").change(function () {
    if ($(this).val() == "SI") {
        $('label[for=id_desc_oncologicas]').show();
        $('#id_desc_oncologicas').show();
        $('#id_desc_oncologicas').attr('required', '');
        $('#id_desc_oncologicas').attr('data-error', 'Este campo es requerido.');
    } else {
        $('label[for=id_desc_oncologicas]').hide();
        $('#id_desc_oncologicas').hide();
        $('#id_desc_oncologicas').removeAttr('required');
        $('#id_desc_oncologicas').removeAttr('data-error');
    }
});
$('label[for=id_desc_hematologicas]').hide();
$('#id_desc_hematologicas').hide();
$("#id_hematologicas").change(function () {
    if ($(this).val() == "SI") {
        $('label[for=id_desc_hematologicas]').show();
        $('#id_desc_hematologicas').show();
        $('#id_desc_hematologicas').attr('required', '');
        $('#id_desc_hematologicas').attr('data-error', 'Este campo es requerido.');
    } else {
        $('label[for=id_desc_hematologicas]').hide();
        $('#id_desc_hematologicas').hide();
        $('#id_desc_hematologicas').removeAttr('required');
        $('#id_desc_hematologicas').removeAttr('data-error');
    }
});
$('label[for=id_desc_intervenciones]').hide();
$('#id_desc_intervenciones').hide();
$("#id_intervenciones").change(function () {
    if ($(this).val() == "SI") {
        $('label[for=id_desc_intervenciones]').show();
        $('#id_desc_intervenciones').show();
        $('#id_desc_intervenciones').attr('required', '');
        $('#id_desc_intervenciones').attr('data-error', 'Este campo es requerido.');
    } else {
        $('label[for=id_desc_intervenciones]').hide();
        $('#id_desc_intervenciones').hide();
        $('#id_desc_intervenciones').removeAttr('required');
        $('#id_desc_intervenciones').removeAttr('data-error');
    }
});
$('label[for=id_desc_medicacion]').hide();
$('#id_desc_medicacion').hide();
$("#id_toma_medicacion").change(function () {
    if ($(this).val() == "SI") {
        $('label[for=id_desc_medicacion]').show();
        $('#id_desc_medicacion').show();
        $('#id_desc_medicacion').attr('required', '');
        $('#id_desc_medicacion').attr('data-error', 'Este campo es requerido.');
    } else {
        $('label[for=id_desc_medicacion]').hide();
        $('#id_desc_medicacion').hide();
        $('#id_desc_medicacion').removeAttr('required');
        $('#id_desc_medicacion').removeAttr('data-error');
    }
});
$('label[for=id_desc_endocrinometabolico]').hide();
$('#id_desc_endocrinometabolico').hide();
$("#id_endocrinometabolico").change(function () {
    if ($(this).val() == "OTROS") {
        $('label[for=id_desc_endocrinometabolico]').show();
        $('#id_desc_endocrinometabolico').show();
        $('#id_desc_endocrinometabolico').attr('required', '');
        $('#id_desc_endocrinometabolico').attr('data-error', 'Este campo es requerido.');
    } else {
        $('label[for=id_desc_endocrinometabolicos]').hide();
        $('#id_desc_endocrinometabolico').hide();
        $('#id_desc_endocrinometabolico').removeAttr('required');
        $('#id_desc_endocrinometabolico').removeAttr('data-error');
    }
});
$('label[for=id_desc_cardiovascular]').hide();
$('#id_desc_cardiovascular').hide();
$("#id_cardiovascular").change(function () {
    if ($(this).val() == "OTROS") {
        $('label[for=id_desc_cardiovascular]').show();
        $('#id_desc_cardiovascular').show();
        $('#id_desc_cardiovascular').attr('required', '');
        $('#id_desc_cardiovascular').attr('data-error', 'Este campo es requerido.');
    } else {
        $('label[for=id_desc_cardiovascular]').hide();
        $('#id_desc_cardiovascular').hide();
        $('#id_desc_cardiovascular').removeAttr('required');
        $('#id_desc_cardiovascular').removeAttr('data-error');
    }
});
$('label[for=id_desc_nefrourologicos]').hide();
$('#id_desc_nefrourologicos').hide();
$("#id_nefrourologicos").change(function () {
    if ($(this).val() == "SI") {
        $('label[for=id_desc_nefrourologicos]').show();
        $('#id_desc_nefrourologicos').show();
        $('#id_desc_nefrourologicos').attr('required', '');
        $('#id_desc_nefrourologicos').attr('data-error', 'Este campo es requerido.');
    } else {
        $('label[for=id_desc_nefrourologicos]').hide();
        $('#id_desc_nefrourologicos').hide();
        $('#id_desc_nefrourologicos').removeAttr('required');
        $('#id_desc_nefrourologicos').removeAttr('data-error');
    }
});
$('label[for=id_desc_dermatologicos]').hide();
$('#id_desc_dermatologicos').hide();
$("#id_dermatologicos").change(function () {
    if ($(this).val() == "SI") {
        $('label[for=id_desc_dermatologicos]').show();
        $('#id_desc_dermatologicos').show();
        $('#id_desc_dermatologicos').attr('required', '');
        $('#id_desc_dermatologicos').attr('data-error', 'Este campo es requerido.');
    } else {
        $('label[for=id_desc_dermatologicos]').hide();
        $('#id_desc_dermatologicos').hide();
        $('#id_desc_dermatologicos').removeAttr('required');
        $('#id_desc_dermatologicos').removeAttr('data-error');
    }
});