# Gerenciador de Processo Linux


Esse projeto visa aplicar e expandir meus conhecimentos em Python e Linux, nele tive o objetivo de fazer
um projeto mais baixo nível, utilizando o menor numero de funções do Python e utilitários do Linux
para obter as informações dos processos, focando em obter as informações diretamente do sistema de 
arquivos do sistema.

Dessa forma esse projeto funciona mapeando informações do diretório /proc do Linux para obter os processos
em execução e depois passa um a um lendo arquivos gerados pelo próprio sistema para pegar informações 
de cada processo, as informações coletadas dos processos são as seguintes:
- PID;
- Usuário que iniciou o processo;
- Nome do processo;
- Prioridade;
- Uso de memória(em KB);
- Uso de leitura de disco(em KB);
- Uso de escrita de disco(em KB);
- Status do processo;

Essas informações ficam sendo atualizadas de forma dinâmica na tela a cada 5 segundos, e para manter a 
fluidez da interface optei por utilizar algumas técnicas para atualizar somente os campos necessários
em tela, usando a seguinte estratégia:

- Quando o processo não estiver ainda na lista, inseri-lô ao fim para causar um menor impacto visual;
- Quando um processo for encerrado, retirar somente a linha referente ao processo e não reconstruir
toda a lista;
- Quando um processo tiver algum dado atualizado, pegar somente o campo que está diferente e atualizá-lo
para evitar apagar e inserir novamente em outra posição da lista;

Durante o desenvolvimento do projeto tive algumas difilculdades, mas sem dúvidas consegui por em prática,
relembrar e aprender vários conceitos que são tão importantes no Linux e no desenvolvimento de software
em geral.

Abaixo segue um video demonstrativo da execução do projeto:


E caso queira executá-lo é bem simples, basta seguir os seguintes passos:
- Clonar esse repositório(`git clone https://github.com/marcoswb/process-manager.git`);
- Instalar as dependências(`pip install -r requirements.txt`)
- Executar o projeto como administrador(`sudo python main.py`)