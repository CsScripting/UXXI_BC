## main_manage_data_planning_uxxi 

* NOTA IMPORTANTE: Em UXXI para envio de horarios apenas é necessario enviar uma das disciplinas. Proprio Sistema irá fazer a relação à Posteriori
* Cria na pasta de planificação pasta de ManageData.
* Em pasta de Manage Data apresenta os Dados de Curriculo que serão considerados na Geração de BTT

    - Cursos --> Todos os cursos Importados;
    - Planos --> Todos os Planos Importados;
    - Turmas --> Todas as Turmas Importados;
    - Disciplinas --> Apenas as dominantes Importadas --> Se disciplina de Grado Dominante de Disciplina de DG. Disciplina Dominante Fica Inserida em Plano de DG;
    - Disciplinas por Plano/Linea --> ;
    - Disciplinas Dominantes e Dominadas;

* Algumas especificações de processos implementados:

[x] group_mutual_modules_plannificacion()

    *   Para Selecionar as Dominantes:
        1º Ordenado por GRADO (G), DOBLE GRADO (DG), MASTERES (M), CURSOS EXTERNOS (F)
        Ou seja, a prioridade da disciplina para ficar como dominante é segundo a ordem indicada acima !
        Isto porque no sistema UXXI só é necessario enviar uma disciplina, o sistema UXXI irá fazer a associação a outros horarios.
        2º Ordena depois por Curso, no caso de duas Discipplinas Dois Grados Com Codigos Diferentes
        3º Por Codigo de Disciplina

[x] check_typologies_uxxi_from_file_conector

    * EB - len(codigo_grupo) = 1
    * EPD - len(codigo_grupo) = 2 
    * AD - len(codigo_grupo) > 2


[] Validações a Considerar:

    [x] genFiles.filter_file_not_null_values

        * Neste caso apenas considera valores que não são nulos...possibilidade de Guardar esta informação !!!
        * Verificar se não existem mesmos conectores de Grupos Diferentes (1,111)
        * Em principio nunca teremos (1,2) --> Só abrem o grupos Grande 2 depois de estar completo o Grupo 1 

        * Validar em conectores o Periodo academico, é unico?

    [x] dataCredUxxi.hours_weeks_section

        *Distribuição de horas nem sempre equitativa --> ver valores de variaveis Nr_Slots_To_Asign

[] Em falta:


    [] - Neste momento cria conjunto de df com validações, será necessario apresentar estes ficheiros

    [] - Validações antes de Gerar

    [] - verificar mesmo grupo de actividad e nomenclautra diferente grupo (ex: 21, 11)
