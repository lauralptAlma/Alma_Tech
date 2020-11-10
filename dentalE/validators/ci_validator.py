# Validación de Cédula
# Adaptado de https://github.com/francocorreasosa/ci_py
# [Arreglos de validación de cédula con 7 dígitos o menos]
# The MIT License (MIT)
#
# Copyright (c) 2014 Franco Correa
#
# Permission is hereby granted, free of charge, #to any person obtaining a
# copy of this software and associated documentation files
# (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, #distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following #conditions:
#
# The above copyright notice and this #permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


def get_validation_digit(ci):
    a = 0
    i = 0
    str_ci = (str(ci))
    if len(str_ci) <= 7:
        for i in range(len(str_ci), 8):
            str_ci = '0' + str_ci
            i = i + 1
    for i in range(0, 7):
        a += (int("2987634"[i]) * int(str_ci[i])) % 10
        i = i + 1
    if a % 10 == 0:
        return 0
    else:
        return 10 - a % 10


def clean_ci(ci):
    return int(str(ci).replace("-", "").replace('.', ''))


def validate_ci(ci):
    ci = clean_ci(ci)
    dig = int(str(ci)[int(len(str(ci))) - 1])
    return dig == get_validation_digit(ci)
