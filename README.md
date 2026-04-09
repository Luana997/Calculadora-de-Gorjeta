{# comentário #} — usado sempre que o comentário menciona ou explica tags Jinja2 como {% block %}, {% if %}, {% for %}, {{ }} etc. O Jinja2 ignora completamente o conteúdo desses comentários.
<!-- comentário --> — mantido para comentários que explicam apenas HTML puro, sem mencionar tags Jinja2.


GET: A rota renderiza o HTML com o formulário vazio (render_template).
POST: O usuário preenche o formulário e envia, a mesma rota recebe o POST, valida os dados e processa-os (request.form). 

Característica            GET                        POST 
Ação              Recuperar/Ler dados          Criar/Enviar dados
URL              Dados visíveis na URL         Dados ocultos (no corpo)
Segurança      Baixa (não usar para senhas)    Alta (dados privados)
Favoritável              Sim                         Não


IF ILIF ELSE



mkdir calculadora-gorjeta
cd calculadora-gorjeta

pip install flask
pip freeze > requirements.txt


from flask import Flask, render_template, request, flash, redirect, url_for

app = Flask(__name__)
app.secret_key = 'sua-chave-secreta-aqui'  # necessário para flash messages


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':

        # 1. Coleta os dados do formulário
        conta_str   = request.form.get('conta', '')
        pessoas_str = request.form.get('pessoas', '')
        gorjeta_str = request.form.get('gorjeta', '')

        # 2. Validação — verifica se os campos estão preenchidos
        erros = False

        if not conta_str:
            flash('Informe o valor da conta.', 'danger')
            erros = True

        if not pessoas_str:
            flash('Informe a quantidade de pessoas.', 'danger')
            erros = True

        if not gorjeta_str:
            flash('Informe o percentual de gorjeta.', 'danger')
            erros = True

        # 3. Conversão de tipos (tratando erros de formato)
        if not erros:
            try:
                conta = float(conta_str)
            except ValueError:
                flash('Valor da conta inválido.', 'danger')
                erros = True

            try:
                pessoas = int(pessoas_str)
            except ValueError:
                flash('Quantidade de pessoas inválida.', 'danger')
                erros = True

            try:
                gorjeta_pct = float(gorjeta_str)
            except ValueError:
                flash('Percentual de gorjeta inválido.', 'danger')
                erros = True

        # 4. Validação de regras de negócio
        if not erros:
            if conta <= 0:
                flash('O valor da conta deve ser maior que zero.', 'danger')
                erros = True

            if pessoas <= 0:
                flash('A quantidade de pessoas deve ser maior que zero.', 'danger')
                erros = True

            if gorjeta_pct < 0:
                flash('O percentual de gorjeta não pode ser negativo.', 'danger')
                erros = True

        # 5. Se tiver erros, volta pro formulário mantendo os dados digitados
        if erros:
            return render_template('index.html',
                                   conta=conta_str,
                                   pessoas=pessoas_str,
                                   gorjeta=gorjeta_str)

        # 6. Cálculos
        valor_gorjeta  = conta * (gorjeta_pct / 100)
        valor_total    = conta + valor_gorjeta
        valor_pessoa   = valor_total / pessoas

        # 7. Classificação
        if gorjeta_pct < 5:
            classificacao = 'Mão de vaca'
        elif gorjeta_pct <= 15:
            classificacao = 'Legal'
        else:
            classificacao = 'Generoso'

        # 8. Envia os resultados para a página de resultado
        return render_template('resultado.html',
                               valor_gorjeta=valor_gorjeta,
                               valor_total=valor_total,
                               valor_pessoa=valor_pessoa,
                               classificacao=classificacao,
                               gorjeta_pct=gorjeta_pct)

    # Se for GET, só mostra o formulário vazio
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)


request.method == 'POST' — diferencia quando o usuário enviou o formulário ou só entrou na página
flash('mensagem', 'categoria') — guarda uma mensagem temporária pra mostrar pro usuário
Fazemos a validação em camadas: primeiro vazio, depois formato, depois regras de negócio



Por que url_for('static', filename='...')? O Flask gera o caminho correto automaticamente. Nunca use caminhos "na mão" como ../static/css/style.css — isso quebra dependendo de onde a rota está.




Usuário acessa /  →  Flask chama index()  →  método GET  →  mostra formulário

Usuário preenche e clica Calcular  →  POST para /
  └── Validação falhou?  →  flash de erro + volta pro form com dados
  └── Validação ok?      →  calcula  →  render resultado.html



  GET
Usado para buscar informações. Quando você digita uma URL e aperta Enter, está fazendo um GET. Não envia dados secretos — tudo fica visível na URL.

Exemplo: acessar a página de login.

POST
Usado para enviar dados ao servidor. Quando você preenche um formulário e clica em "Enviar", está fazendo um POST. Os dados vão no corpo da requisição, não na URL.

Exemplo: enviar o formulário de login com e-mail e senha.



Python + Flask	É o "cérebro" do sistema. Recebe as requisições do navegador, processa os dados e decide qual página mostrar.
Jinja2	É a linguagem de templates. Permite misturar HTML com lógica Python (loops, condições, variáveis) dentro dos arquivos .html.
Bootstrap	É uma biblioteca de CSS pronta. Fornece botões, tabelas, formulários e grids já estilizados para não precisar escrever tudo do zero.





Importação	Para que serve
Flask	A classe principal que cria a aplicação.
render_template	Abre um arquivo HTML da pasta templates e o devolve como resposta.
request	Permite acessar os dados enviados pelo formulário (request.form).
redirect	Redireciona o usuário para outra página.
url_for	Gera automaticamente a URL de uma rota pelo nome da função.
flash	Envia mensagens temporárias para o usuário (ex: "Login realizado!").
session	Armazena dados do usuário entre requisições (como o e-mail de quem está logado).



JINJA2
{{ variavel }}	Expressão	Exibe o valor de uma variável na página.
{% comando %}	Instrução	Executa lógica: if, for, block, extends, etc.
{# comentário #}	Comentário	Comentário que o Jinja2 ignora completamente. Não aparece no HTML final.


Jinja2 — exibindo variáveis
<!-- Exibe o nome do usuário logado, guardado na sessão -->
{{ session.get('usuario', 'Usuário') }}

<!-- Exibe o nome de um livro -->
{{ l.titulo }}

<!-- Gera a URL da rota 'login' automaticamente -->
{{ url_for('login') }}


Jinja2 — condição if (usada na navbar para destacar o item ativo)
<a class="nav-link {% if request.path.startswith('/livros') %}active{% endif %}">
  Livros
</a>

{# Se a URL atual começa com /livros, adiciona a classe "active" ao link,
   deixando o item do menu destacado visualmente. #}



      Jinja2 — loop for (usado para montar as tabelas)
{% for l in livros %}
<tr>
  <td>{{ l.id }}</td>
  <td>{{ l.titulo }}</td>
  <td>{{ l.autor }}</td>
</tr>
{% endfor %}




Template base (base.html)
Define a estrutura comum: navbar, rodapé, links de CSS e JS. Tem um bloco vazio onde cada página vai colocar seu conteúdo.

{% block conteudo %}
{% endblock %}



Página filha (listar_livros.html)
Herda o base.html e preenche apenas o bloco de conteúdo, sem repetir navbar ou rodapé.

{% extends 'base.html' %}
{% block conteudo %}
  <!-- conteúdo aqui -->
{% endblock %}



base_publica.html	index, login, cadastro	Navbar simples com botões de "Entrar" e "Cadastrar". Fundo claro. Sem menu do sistema.
base.html	usuários, livros, autores	Navbar completa com menu de navegação entre seções, nome do usuário logado e botão de sair.




base.html — exibindo flash messages
{% with messages = get_flashed_messages(with_categories=true) %}
  {% if messages %}
    {% for category, message in messages %}

      <div class="alert alert-{{ category }}">
        {{ message }}
      </div>

    {% endfor %}
  {% endif %}
{% endwith %}



container / container-fluid	Limita e centraliza o conteúdo na página.
row / col-md-6	Sistema de grid. Divide a linha em colunas (12 no total). col-md-6 ocupa metade.
btn btn-amber	Estilo de botão. btn é Bootstrap, btn-amber é classe personalizada do projeto.
form-control / form-select	Estiliza inputs e selects com bordas, padding e foco animado.
table table-hover table-bordered	Tabela com bordas e destaque ao passar o mouse.
d-flex / gap-3 / justify-content-end	Flexbox utilitário para alinhar elementos lado a lado.
alert alert-success / alert-danger	Caixas de mensagem coloridas (verde = sucesso, vermelho = erro).
navbar navbar-expand-lg	Barra de navegação responsiva que vira menu hambúrguer em telas pequenas.
mb-3 / mt-4 / px-4 / py-2	Utilitários de espaçamento. m=margin, p=padding, b=bottom, t=top, x=horizontal, y=vertical.
text-center / w-100	Centraliza texto / faz elemento ocupar 100% da largura.



1	Usuário acessa /login no navegador → requisição GET chega ao Flask.
2	Flask chama a função login(). Como é GET, retorna render_template('login.html').
3	Jinja2 processa o login.html, preenche as tags {{ }} e {% %}, e gera o HTML final.
4	Navegador recebe o HTML e exibe a página de login para o usuário.
5	Usuário preenche e-mail e senha e clica em "Entrar" → requisição POST é enviada.
6	Flask chama login() novamente. Agora é POST, então entra no bloco if request.method == 'POST'.
7	Flask pega os dados: request.form.get('email') e request.form.get('senha').
8	Valida os campos. Se estiverem preenchidos, salva na sessão: session['usuario'] = email.
9	Envia mensagem de sucesso: flash('Login realizado!', 'success').
10	Redireciona para a lista de usuários: redirect(url_for('listar_usuarios')).
11	Na nova página, o base.html exibe a flash message de sucesso e o nome do usuário logado na navbar.



<!-- Comentário HTML -->

{# Comentário Jinja2 #}
