# app.py — Arquivo principal da aplicação Flask
# Aqui ficam as rotas e a lógica de negócio (back-end)

from flask import Flask, render_template, request, redirect, url_for, flash

# Cria a instância da aplicação Flask
# __name__ indica o módulo atual, usado pelo Flask para localizar templates e estáticos
app = Flask(__name__)

# Chave secreta necessária para o sistema de flash messages (sessão segura)
# Em produção, use uma chave longa e aleatória, nunca deixe em texto puro no código
app.secret_key = "sua_chave_secreta_aqui"


# ─────────────────────────────────────────────
# Função auxiliar: classifica o percentual de gorjeta
# ─────────────────────────────────────────────
def classificar_gorjeta(percentual):
    """
    Retorna a classificação do pagador com base no percentual de gorjeta informado.
    - Abaixo de 5%  → "Mão de vaca"
    - De 5% a 15%   → "Legal"   (inclusive nos dois extremos)
    - Acima de 15%  → "Generoso"
    """
    if percentual < 5:
        return "Mão de vaca"
    elif percentual <= 15:
        return "Legal"
    else:
        return "Generoso"


# ─────────────────────────────────────────────
# Rota principal — exibe o formulário (GET) e processa os dados (POST)
# ─────────────────────────────────────────────
@app.route("/", methods=["GET", "POST"])
def index():
    """
    GET  → apenas renderiza o formulário vazio.
    POST → valida os dados, calcula os resultados e renderiza a página de resultados
           (ou re-exibe o formulário com erros, mantendo os valores já digitados).
    """

    # Dicionário que armazena os valores digitados pelo usuário para re-popular
    # o formulário em caso de erro (evita que o usuário precise redigitar tudo)
    dados_formulario = {
        "valor_conta": "",
        "quantidade_pessoas": "",
        "percentual_gorjeta": "",
    }

    # ── Processamento do POST ──────────────────────────────────────────────
    if request.method == "POST":

        # Coleta os valores enviados pelo formulário como strings brutas
        valor_conta_str = request.form.get("valor_conta", "").strip()
        qtd_pessoas_str = request.form.get("quantidade_pessoas", "").strip()
        perc_gorjeta_str = request.form.get("percentual_gorjeta", "").strip()

        # Guarda os valores para re-popular o formulário (sempre, mesmo com erro)
        dados_formulario["valor_conta"] = valor_conta_str
        dados_formulario["quantidade_pessoas"] = qtd_pessoas_str
        dados_formulario["percentual_gorjeta"] = perc_gorjeta_str

        # ── Validação campo a campo ────────────────────────────────────────
        erros = []  # Lista de mensagens de erro encontradas

        # 1. Verificar se os campos estão preenchidos
        if not valor_conta_str:
            erros.append("O valor total da conta é obrigatório.")
        if not qtd_pessoas_str:
            erros.append("A quantidade de pessoas é obrigatória.")
        if not perc_gorjeta_str:
            erros.append("O percentual de gorjeta é obrigatório.")

        # 2. Se os campos estiverem preenchidos, tentar converter para números
        valor_conta = None
        qtd_pessoas = None
        perc_gorjeta = None

        if valor_conta_str:
            try:
                # Substitui vírgula por ponto (suporte ao formato brasileiro)
                valor_conta = float(valor_conta_str.replace(",", "."))
            except ValueError:
                erros.append("O valor da conta deve ser um número válido.")

        if qtd_pessoas_str:
            try:
                # Garante que seja inteiro (não aceitamos 2.5 pessoas)
                qtd_pessoas = int(qtd_pessoas_str)
            except ValueError:
                erros.append("A quantidade de pessoas deve ser um número inteiro.")

        if perc_gorjeta_str:
            try:
                perc_gorjeta = float(perc_gorjeta_str.replace(",", "."))
            except ValueError:
                erros.append("O percentual de gorjeta deve ser um número válido.")

        # 3. Validações de regras de negócio (só se a conversão foi bem-sucedida)
        if valor_conta is not None and valor_conta <= 0:
            erros.append("O valor da conta deve ser maior que zero.")

        if qtd_pessoas is not None and qtd_pessoas <= 0:
            erros.append("A quantidade de pessoas deve ser maior que zero.")

        if perc_gorjeta is not None and perc_gorjeta < 0:
            erros.append("O percentual de gorjeta não pode ser negativo.")

        # ── Se houver erros, exibe as mensagens e re-renderiza o formulário ──
        if erros:
            for erro in erros:
                # flash(mensagem, categoria) — a categoria é usada no template
                # para definir a cor do alerta (danger = vermelho no Bootstrap)
                flash(erro, "danger")
            # Passa os dados de volta para re-popular o formulário
            return render_template("index.html", dados=dados_formulario)

        # ── Cálculos (só chegamos aqui se todos os dados são válidos) ─────
        valor_gorjeta = valor_conta * (perc_gorjeta / 100)
        valor_total = valor_conta + valor_gorjeta
        valor_por_pessoa = valor_total / qtd_pessoas
        classificacao = classificar_gorjeta(perc_gorjeta)

        # Agrupa os resultados em um dicionário para passar ao template
        resultados = {
            "valor_conta": valor_conta,
            "qtd_pessoas": qtd_pessoas,
            "perc_gorjeta": perc_gorjeta,
            "valor_gorjeta": valor_gorjeta,
            "valor_total": valor_total,
            "valor_por_pessoa": valor_por_pessoa,
            "classificacao": classificacao,
        }

        # Renderiza a página de resultados passando os dados calculados
        return render_template("resultado.html", resultados=resultados)

    # ── GET: apenas exibe o formulário vazio ──────────────────────────────
    return render_template("index.html", dados=dados_formulario)


# ─────────────────────────────────────────────
# Ponto de entrada da aplicação
# ─────────────────────────────────────────────
if __name__ == "__main__":
    # debug=True → reinicia o servidor automaticamente ao salvar e exibe erros no navegador
    # Nunca use debug=True em produção!
    app.run(debug=True)
