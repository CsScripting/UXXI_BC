from PackLibrary.librarys import(
DataFrame
)
from mod_variables import *


def parse_week_loads_df_from_json (w_loads : list):

    # w_loads UMA LISTA, com DADOS PARA CADA UMA DAS DISCIPLINAS A QUAL FOI APLICADO O PADRÂO DE WEEKLOAD!!!
    # CADA ELEMENTO DA LISTA TEM AS CARACTERISTICAS DE W_LOAD PARA DISCIPLINA/TIPO
    # NO CASO DE TER SIDO APLICADO A QUATRO DISCIPLINAS APRESENTA 4 LINHAS O DF FINAL...


    df = DataFrame(w_loads)


    columns_used_from_json = [v_id_dto,
                              v_name_dto,
                              v_module_w_load_dto,
                              v_w_load_session_dto,
                              v_w_load_typologie_dto
                              ]

     #Filter DataFrame Values
    df = df [columns_used_from_json].copy()

    df[v_mod_code] =  df[v_module_w_load_dto].apply(lambda x: x.get(v_code_dto)) # UMA DISCIPLINA POR LINHA ... GET SIMPLES
    df['Datos_Tipologia_Temp'] = df[v_w_load_typologie_dto].apply(lambda x: [ d[v_typologie_data_dto]  for d in x]) ## TIPOLOGIAS É UMA LISTA 
    df[v_mod_typologie] = df['Datos_Tipologia_Temp'].apply(lambda x: [ d[v_name_dto]  for d in x]) ## PROCURAR NA LISTA DE TIPOLOGIAS NOME DE TIPOLOGIA --> TIPOLOGIAS RETORNA LISTA D1 (Dimensão 1)

    # wlSessions LISTA PODE TER 1, 2, ou 3 elementos conforme Repetição 1, 2 ou 3 ...
    # APENAS CONSIDERADOS VALORES DE SESSION 1...Ou SEJA O PRIMEIRO ELEMENTO DE LISTA
    # O QUE NECESITAMOS DE SESSION É SEMPRE IGUAL PARA AS DIFERENTES REPETIÇÔES: CODIGO WEEKLOAD, TIPOLOGIA e TURMAS QUE NECESITAMOS DE GERIR.
    # .
    # .
    df['Datos_Sections_Temp'] = df[v_w_load_session_dto].apply(lambda x: [value['wlsSections'] for index_value, value in enumerate(x) if index_value == 0] ) # PROCURAR EM LISTA SESSIONES --> Lista SECTIONES

    # df['Name_Section'] = df['Datos_Sections_Temp'].apply(lambda x: [ ([v[v_name_dto] for v in d]) for d in x]) # EM LISTA SECTIONES NOME SECTIONES  --> RETORNA LISTA D2
    df[v_id_w_load_section] = df['Datos_Sections_Temp'].apply(lambda x: [ ([v[v_id_dto] for v in d]) for d in x]) # EM LISTA SECTIONES CODIGO SECTIONES  --> RETORNA LISTA D2
    df['Student_Groups_Temp'] = df['Datos_Sections_Temp'].apply(lambda x: [ ([v['studentGroups'] for v in d]) for d in x]) # EM LISTA DE SESSIONES --> LISTAS SECTIONES ---> LISTA STUDENTGROUPS RETORNA LISTA D3
    df['Name_Student_Groups_Temp'] = df['Student_Groups_Temp'].apply(lambda x: [ ([([n[v_name_dto] for n in v]) for v in d]) for d in x]) # --> D3
                                                    
    

    df.rename(columns = {v_id_dto : v_id_w_load,
                         v_name_dto : v_name_wload,
                         }, inplace=True)
    
    df = df[[v_id_w_load,
             v_name_wload,
             v_mod_typologie,
             v_mod_code,
             v_id_w_load_section,
             'Name_Student_Groups_Temp']].copy()
    
    # AJUSTE DE DADOS EM DATAFRAME


    #CRIOU LISTA DE DIMENSÂO 2 (CRIOU ESTE TIPO DE LISTA VALOR ANINHADO NO JSON)PASSAR COM DIMENSÂO 1
    df[v_id_w_load_section] = df[v_id_w_load_section].apply(lambda x: [elem for d1 in x for elem in d1])
    #CRIOU LISTA DE DIMENSÂO 3 (CRIOU ESTE TIPO DE LISTA VALOR ANINHADO NO JSON)PASSAR COM DIMENSÂO 2 ---> NECESSARIO FICAR LISTA DE LISTA !!! PARA SABER OS GRUPOS DE CADA SECCION
    df['Name_Student_Groups_Temp'] = df['Name_Student_Groups_Temp'].apply(lambda x: [elem for d2 in x for elem in d2])
    

    return(df)


