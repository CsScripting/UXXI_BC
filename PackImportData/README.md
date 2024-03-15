## main_import_data

[x] import_data_steps():

    [] - Inserir as salas em Falta de de Ficheiro Curriculim New
         TALVEZ MELHOR OPÇÂO PARA PROCESSO: Utilizador terá de usar Formato de Dados Gerado para Importar Salas
         Isto para não se ter de validar se Edificio ou Caracteristicas Existem ....


[x] import_data_steps():

    * Mais Tarde Subdividir em general_import_data_steps:

        [x] planning_import_data_steps ---> Em Elaboração

        [] schedules_import_data_steps


[x] match_id_entities_events.py

    [] Nas diferentes entidades/metodos verificar o ficheiro que cria df_invalid ...será necessario fazer drop columns [valor que buscava, _merge]
        A implementação será na tal como em match_id_entities_planning.py para as diferentes entidades !!!
        Pode-se testar alterando valores enquanto executa:
        df.loc[df[v_code_best] == 'G12341', v_code_best ] = 'AV' ##ONLY TO TEST