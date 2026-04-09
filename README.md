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
