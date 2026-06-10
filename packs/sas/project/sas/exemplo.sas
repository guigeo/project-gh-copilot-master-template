/* Exemplo de programa SAS seguindo as convenções do template.
   Objetivo: ler vendas, filtrar período e resumir por região. */

options nodate nonumber mprint;

/* Caminho via macro variável, nunca path local fixo */
%let raiz = %sysget(SAS_PROJECT_ROOT);
libname dados "&raiz/dados";

/* Filtra cedo para reduzir volume antes de agregar */
proc sql;
    create table work.vendas_2024 as
    select regiao,
           produto,
           sum(valor) as total_valor format=comma12.2,
           count(*)   as qtd
    from dados.vendas
    where ano = 2024
    group by regiao, produto;
quit;

/* Limpa temporários ao final */
proc datasets library=work nolist;
    delete vendas_2024;
quit;
