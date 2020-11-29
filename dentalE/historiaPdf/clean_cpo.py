from dentalE.models import CPO
import ast
# Limpieza de cpo


def build_clean_teeth_dic(teeth_list, status):
    list_clean = {}
    maxilla = ['1', '2', '5', '6']
    lower_jaw = ['3', '4', '7', '8']
    if teeth_list:
        for teeth in teeth_list:
            cara_list = cara(teeth[0])
            pieza_list = teeth[-2] + teeth[-1]
            if pieza_list[0] in maxilla and cara_list == 'Lingual/Paladino':
                cara_list = 'Paladino'
            if pieza_list[0] in lower_jaw and cara_list == 'Lingual/Paladino':
                cara_list = 'Lingual'
            list_dic = dict(cara=[cara_list], pieza=pieza_list)
            if pieza_list in list_clean:
                existing_list_caras = list_clean[pieza_list][status].get(
                    'cara')
                existing_list_caras.append(cara_list)
                list_clean[pieza_list][status] = dict(cara=existing_list_caras,
                                                      pieza=pieza_list)
            else:
                list_clean[pieza_list] = {status: list_dic}
    return list_clean


def cara(argument):
    switcher = {
        't': "Vestibular",
        'l': "Distal",
        'b': "Lingual/Palatino",
        'r': "Mesial",
        'c': "Oclusal",
    }
    return switcher.get(argument, "Cara de diente no válida")


def clean_tooth(teeth):
    list_clean = []
    if teeth:
        for t in teeth:
            tooth = t[-2] + t[-1]
            if tooth in list_clean:
                pass
            else:
                list_clean.append(tooth)
    return list_clean


def clean_decayed_filled(decayed_filled_teeth):
    decayed_filled_list = []
    for id, info in decayed_filled_teeth.items():
        pieza = id
        for key in info:
            caras = info[key]['cara']
        decayed_filled_list.append([pieza, caras])
    return decayed_filled_list


def get_cpo(patient):
    cpos = CPO.objects.filter(paciente_id=patient).order_by('-cpo_id')
    if cpos:
        for c in cpos:
            c.contenido_cpo = ast.literal_eval(c.contenido_cpo)
            caries = c.contenido_cpo['cariados']
            caries_dic = build_clean_teeth_dic(caries, 'cariados')
            caries_clean = clean_decayed_filled(caries_dic)
            obturaciones = c.contenido_cpo['obturados']
            obturaciones_dic = build_clean_teeth_dic(obturaciones, 'obturados')
            obturaciones_clean = clean_decayed_filled(obturaciones_dic)
            perdidos = c.contenido_cpo['perdidos']
            perdidos_clean = clean_tooth(perdidos)
            ausentes = c.contenido_cpo['ausentes']
            ausentes_clean = clean_tooth(ausentes)

            c.caries = caries_clean
            c.obturaciones = obturaciones_clean
            c.perdidos = perdidos_clean
            c.ausentes = ausentes_clean
    return cpos
