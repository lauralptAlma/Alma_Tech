/* En el caso de los Antecedentes clínicos los campos de descripción serán visibles
* según la opción seleccionada por el usuario */
// Aparato digestivo
$('label[for=id_desc_aparato_digestivo]').hide();
$('#id_desc_aparato_digestivo').hide();
const hideElementApDigestivo = document.querySelector('#id_aparato_digestivo_0');
hideElementApDigestivo.addEventListener('change', function (e) {
    if (hideElementApDigestivo.checked) {
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

// Dermatologicos
$('label[for=id_desc_dermatologicos]').hide();
$('#id_desc_dermatologicos').hide();
const hideElementDermatologicos = document.querySelector('#id_dermatologicos_0');
hideElementDermatologicos.addEventListener('change', function (e) {
    if (hideElementDermatologicos.checked) {
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

// Alergias
$('label[for=id_desc_alergias]').hide();
$('#id_desc_alergias').hide();
const hideElementAlergias = document.querySelector('#id_alergias_0');
hideElementAlergias.addEventListener('change', function (e) {
    if (hideElementAlergias.checked) {
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

// Autoinmnunes
$('label[for=id_desc_autoinmunes]').hide();
$('#id_desc_autoinmunes').hide();
const hideElementAutoinmune = document.querySelector('#id_autoinmunes_0');
hideElementAutoinmune.addEventListener('change', function (e) {
    if (hideElementAutoinmune.checked) {
        $('label[for=id_desc_autoinmunes]').show();
        $('#id_desc_autoinmunes').show();
        $('#id_desc_autoinmunes').attr('required', '');
        $('#id_desc_autoinmunes').attr('data-error', 'Este campo es requerido.');
    } else {
        $('label[for=id_desc_autoinmunes]').hide();
        $('#id_desc_autoinmunes').hide();
        $('#id_desc_autoinmunes').removeAttr('required');
        $('#id_desc_autoinmunes').removeAttr('data-error');
    }
});

// Oncologicas
$('label[for=id_desc_oncologicas]').hide();
$('#id_desc_oncologicas').hide();
const hideElementOncologicas = document.querySelector('#id_oncologicas_0');
hideElementOncologicas.addEventListener('change', function (e) {
    if (hideElementOncologicas.checked) {
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

// Hematologicas
$('label[for=id_desc_hematologicas]').hide();
$('#id_desc_hematologicas').hide();
const hideElementHematologicas = document.querySelector('#id_hematologicas_0');
hideElementHematologicas.addEventListener('change', function (e) {
    if (hideElementHematologicas.checked) {
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

// Intervenciones
$('label[for=id_desc_intervenciones]').hide();
$('#id_desc_intervenciones').hide();
const hideElementIntervenciones = document.querySelector('#id_intervenciones_0');
hideElementIntervenciones.addEventListener('change', function (e) {
    if (hideElementIntervenciones.checked) {
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

// Medicacion
$('label[for=id_desc_medicacion]').hide();
$('#id_desc_medicacion').hide();
const hideElementMedicacion = document.querySelector('#id_toma_medicacion_0');
hideElementMedicacion.addEventListener('change', function (e) {
    if (hideElementMedicacion.checked) {
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

// Endocrinometabolico
$('label[for=id_desc_endocrinometabolico]').hide();
$('#id_desc_endocrinometabolico').hide();
const hideElementEndocrinometabolico = document.querySelector('#id_endocrinometabolico_4');
hideElementEndocrinometabolico.addEventListener('change', function (e) {
    if (hideElementEndocrinometabolico.checked) {
        $('label[for=id_desc_endocrinometabolico]').show();
        $('#id_desc_endocrinometabolico').show();
        $('#id_desc_endocrinometabolico').attr('required', '');
        $('#id_desc_endocrinometabolico').attr('data-error', 'Este campo es requerido.');
    } else {
        $('label[for=id_desc_endocrinometabolico]').hide();
        $('#id_desc_endocrinometabolico').hide();
        $('#id_desc_endocrinometabolico').removeAttr('required');
        $('#id_desc_endocrinometabolico').removeAttr('data-error');
    }
});

// Cardiovascular
$('label[for=id_desc_cardiovascular]').hide();
$('#id_desc_cardiovascular').hide();
const hideElementCardiovascular = document.querySelector('#id_cardiovascular_4');
hideElementCardiovascular.addEventListener('change', function (e) {
    if (hideElementCardiovascular.checked) {
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

// Nefrourologicos
$('label[for=id_desc_nefrourologicos]').hide();
$('#id_desc_nefrourologicos').hide();
const hideElementNefrourologicos = document.querySelector('#id_nefrourologicos_4');
hideElementNefrourologicos.addEventListener('change', function (e) {
    if (hideElementNefrourologicos.checked) {
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

// Osteoarticulares
$('label[for=id_desc_osteoarticulares]').hide();
$('#id_desc_osteoarticulares').hide();
const hideElementOsteoarticulares = document.querySelector('#id_osteoarticulares_3');
hideElementOsteoarticulares.addEventListener('change', function (e) {
    if (hideElementOsteoarticulares.checked) {
        $('label[for=id_desc_osteoarticulares]').show();
        $('#id_desc_osteoarticulares').show();
        $('#id_desc_osteoarticulares').attr('required', '');
        $('#id_desc_osteoarticulares').attr('data-error', 'Este campo es requerido.');
    } else {
        $('label[for=id_desc_osteoarticulares]').hide();
        $('#id_desc_osteoarticulares').hide();
        $('#id_desc_osteoarticulares').removeAttr('required');
        $('#id_desc_osteoarticulares').removeAttr('data-error');
    }
});

