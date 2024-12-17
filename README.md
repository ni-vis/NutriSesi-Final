# Sistema de Feedbacks de Serviços

## Descrição
Este projeto é um **Sistema de Feedbacks de Serviços**, desenvolvido por um grupo de quatro alunos durante um período de três meses como parte do Trabalho de Conclusão de Curso (TCC) da primeira turma do curso Técnico em Desenvolvimento de Sistemas do SESI SENAI em 2024.

O sistema foi criado inicialmente para uma campanha contra o desperdício de alimentos, permitindo que os cardápios fossem avaliados a fim de identificar as preferências dos alunos e reduzir o desperdício. No entanto, ele é versátil e pode ser aplicado em outras áreas, como empresas que desejam coletar feedbacks de clientes para avaliar a satisfação com seus serviços.

## Funcionalidades
- Cadastro, edição e exclusão de cardápios.
- Sistema de votação para aprovação ou reprovação de itens do cardápio.
- Coleta de comentários específicos para itens reprovados.
- Relatórios de resultados com número de aprovações, reprovações, gráficos e comentários.
- Geração de relatórios em PDF.
- Interface administrativa para gerenciar cardápios e feedbacks.

## Tecnologias Utilizadas
- **Linguagem de programação**: Python
- **Framework web**: Flask
- **Banco de dados**: MySQL
- **Geração de PDF**: pdfkit
- **HTML, CSS e JavaScript** para a interface do usuário e para geração de gráficos e PDFs

## Estrutura do Projeto
- `api.py`: Contém o backend do sistema, gerenciando rotas e a lógica do servidor.
- `templates/`: Diretório com os arquivos HTML para as interfaces do sistema.
- `static/`: Arquivos CSS e JavaScript.
- `db_functions.py`: Funções auxiliares para operações no banco de dados.
- `config.py`: Configurações, incluindo variáveis sensíveis como `SECRET_KEY`.

## Como Executar
1. **Pré-requisitos**:
   - Python 3.8 ou superior.
   - MySQL.

2. **Configuração do Banco de Dados**:
   - Configure as credenciais de acesso no arquivo `config.py`.
   - Certifique-se de que o banco de dados foi inicializado com as tabelas necessárias.

3. **Executando o Projeto**:
   ```bash
   python api.py
   ```
   O sistema estará disponível em `http://localhost:5000`.

## Contribuidores
- [Geovanna Antunes](https://github.com/geovanninhaA) - **Scrum Master**: Responsável por facilitar o processo e remover impedimentos para o progresso do time.
- [Gustavo Henrique](https://github.com/GustaDev07) - **Product Owner (PO)**: Gerenciou o backlog e definiu prioridades com base nos objetivos do projeto.
- [Nicole Vidal](https://github.com/ni-vis) - **Tech Lead**: Coordenou as decisões técnicas e garantiu a qualidade do código.
- [Matheus Guimarães](https://github.com/MTheuzin) - **Desenvolvedor(a)**: Implementou funcionalidades e contribuiu para a lógica de negócio do sistema.

## Licença
Este projeto foi desenvolvido como parte de um curso técnico e não possui licença específica para uso comercial.

---

**SESI SENAI 2024** - Curso Técnico em Desenvolvimento de Sistemas
