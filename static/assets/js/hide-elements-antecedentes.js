/* En el caso de los Antecedentes clínicos los campos de descripción serán
visibles según la opción seleccionada por el usuario */

const radios = document.querySelectorAll('input[type=radio]');
const checks = document.querySelectorAll('input[value=\'OTROS\']');

function changeRadioHandler(event) {
    if (this.value === 'SI') {
        $(this).closest('ul').nextUntil('.col').show();
    } else if (this.value === 'NO') {
        $(this).closest('ul').nextUntil('.col').hide();
    } else {
        $(this).closest('ul').nextUntil('.col').hide();
    }
}

function changeCheckHandler(event) {
    if (this.checked) {
        $(this).closest('ul').nextUntil('.col').show();
    } else if (this.value === 'NO') {
        $(this).closest('ul').nextUntil('.col').hide();
    } else {
        $(this).closest('ul').nextUntil('.col').hide();
    }
}

Array.prototype.forEach.call(radios, function (radio) {
    radio.addEventListener('change', changeRadioHandler);
})
Array.prototype.forEach.call(checks, function (check) {
    check.addEventListener('change', changeCheckHandler);
})

$(document).ready(function () {
    radios.forEach(function (radio) {
        $(radio).closest('ul').nextUntil('.col').hide();
    })
    checks.forEach(function (check) {
        $(check).closest('ul').nextUntil('.col').hide();
    })
});
