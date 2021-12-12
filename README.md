# Projeto de filtros ativos utilizando algoritmo evolucionário

Trabalho de conclusão do curso para obtenção de certificado no Curso de Especialização – Latu Sensu em
Engenharia de Desenvolvimento de Projetos Eletrônicos da União Brasileira de Faculdades, UniBF.

O trabalho consiste em aplicar algoritmo evolucionário para o projeto de filtros ativos, buscando obter a melhor
relação de valores de componentes eletrônicos (resistores e capacitores) disponíveis comercialmente a fim
de atender os requisitos de projeto do filtro ativo.

# 1. Funcionamento

Todo o projeto é baseado na otimização de um circuito de filtro ativo passa-baixas com resposta do tipo Butterworth. A
otimização irá buscar a melhor seleção de componentes eletrônicos (resistores e capacitores) com valor comercial a fim
de satisfazer os critérios de resposta do filtro.

## 1.1 Otimização
## 1.2 Equações dos filtros ativos
## 1.3 Resultados

# 2. Execução do código

O projeto foi todo feito na linguagem [Python](https://www.python.org), com o auxílio das bibliotecas 
[Numpy](https://numpy.org) e [DEAP](https://github.com/DEAP/deap). O software 
[LTspice](https://www.analog.com/en/design-center/design-tools-and-calculators/ltspice-simulator.html) foi utilizado 
como software de simulação para a análise dos resultados.

Requisitos:

* Python 3.9+ (Pode funcionar em versões mais antigas, mas não foi testado)
* Bibliotecas do arquivo ```./Python/requirements.txt```

O código de otimização para cada série está nos scripts ```./Python/e12_series.py```, ```./Python/e24_series.py``` e
```./Python/e48_series.py```. Cada script possui suas próprias configurações de otimização e das características do
filtro e após a execução o resultado é salvo em um arquivo no formato json na pasta ```./Python/results```.

O script ```./Python/ltspice_generator.py``` utiliza dos arquivos json de resultados para criar um filtro com os 
componentes obtidos da otimização no formato .asc que é utilizado pelo LTSpice para simulações.

# 3. Referências bibliográficas

Aqui estão algumas das principais referências utilizadas no TCC:

CARTER, Bruce; MANCINI, Ron. **Op Amps for everyone**. Newnes, 2017.

DE RAINVILLE, François-Michel et al. **DEAP: A python framework for evolutionary algorithms**. Proceedings of the 14th
annual conference companion on Genetic and evolutionary computation. 2012. p. 85-92.

DE, Bishnu Prasad et al. **Optimal selection of components value for analog active filter design using simplex particle 
swarm optimization**. International Journal of Machine Learning and Cybernetics, v. 6, n. 4, p. 621-636, 2015.

GOLDBERG, D. E. **Genetic Algorithms in Search, Optimization, and Machine Learning**. 1. ed. Boston, Massachusetts:
Addison-Wesley Publishing Company, 1989. 432 p.

RAO, S. S. **Engineering optimization: theory and practice**. 4. ed. Hoboken, New Jersey: John Wiley & Sons, 2009. 830
p.

WIKIPÉDIA. **E series of preferred numbers**. Disponível em: 
<http://en.wikipedia.org/wiki/E_series_of_preferred_numbers>. Acesso em: 25 nov. 2021.