Release Folder:
C:\Users\Paulo Fernandes\Desktop\LocalRepositories\Release_Environment\Deploy_UXXI_BC

Release Options:
pyinstaller --noconsole --onefile --icon="log.ico" --add-data="log.ico;." UXXI_To_BC.py --version-file version_info_UXXI_to_BC.txt


                                         -------------------- // ------------------------ 


== PackValidationsFiles ==

# [x] settings_validation

    * validation_settings_steps

       [x]  1º - present_on_ui_opciones_process() -- > Opções relativas a Processo
       [x]  2º - Se pasta de dados UXXI existe
       [x]  2º - Extensão de Ficheiro

       --> No caso de Update ou Importação:
       [x]  1º - Se pasta de config.txt existe
       [x]  2º - Se config.tx existe na Pasta
       [x]  2º - Se Formato de config.txt está correto

== PackManageData ==  

[] bussiness_rules_uxxi

    Aplicar a causuistica a AD (Atividades Dirigidas...subDivisão ed EPD's)

    * relacion_group_EPD_by_section_module_EB

    As turmas de referencia para os eventos são sempre relativos ao maximo de divisões de Turnos em relação a PLANO/DISCIPLINA:

    Plano A:
    --> A Disciplina de MAT tem um EB e duas EPD's, a EB fica com duas EPD's
    --> A Disciplina de ALG tem uma EB e tres EPD´s, a EB fica com tres EPS´s.
    --> No Plano serão Inseridas 3 Turmas 
    --> Como por vezes temos turnos compartidos por diferentes Planos, numa EB posso ter:
        Dois turnos de EDP de Grado A
        Tres tursnos de EDP de Grado B

        Caso de Disciplina de Fundamentos De Derecho (103002)
    --> No caso de Disciplina só ter EB fica com o grupo reduzido EPD , so tem EB1 o Grupo será o EDP1
        Irá facilitar no caso de se querer criar mais Grupos.
       
* Nota em relação a Sobreposição não verificada ---> ver Back Up de UPO Idioma Moderno I: Isto em processo de Geração de Salas --> Muitas turmas associadas.

Duración en slots: 6 (3:00)
Carga semanal: EB4
Tipología: EB
Asignatura: IDIOMA MODERNO I: ITALIANO; 106008; 106008
Sección: EB 1
Semanas: 07/11/2022

Ver dados importados Ultimos de alunos reais na UPO

* Verificar a Agregação de Semanas...o group_entities...poderei alterar com o Codigo de Evento que Fernando vai Enviar

* Algumas das validações a fazer:

- Formato de data;
- Int (alunos);
- Formato de Horas;

* Notas em relação a Possibilidade de Criar Nome de Grupo Bullet com Sigla de Titulacion e não com o Nome.
     
