
### 🔒 Minicurso Prático: Segurança no Desenvolvimento Web com Python e Flask

Este documento contém o planejamento pedagógico completo, códigos-fonte, guia de laboratório e material para slides voltado para alunos de Sistemas de Informação. 

### 🗺️ 1. Roadmap e Cronograma Consolidado (4 Horas)

[00:00 - 01:00] ───► MÓDULO 1: SQL INJECTION (SQLi)
                       ├── Teoria: O que é OWASP Top 10 e Árvores de Parsing SQL
                       ├── Prática: Burlar tela de login Flask com ' OR '1'='1
                       └── Correção: Implementação de Consultas Parametrizadas (?)
                       
[01:00 - 02:00] ───► MÓDULO 2: LÓGICA DE NEGÓCIO E IDOR
                       ├── Teoria: Falhas no Controle de Acesso e manipulação de requisições HTTP
                       ├── Prática: Alterar parâmetros de URL para acessar dados de terceiros
                       └── Correção: Validação de escopo baseada em contexto (ABAC) no Backend
                       
[02:00 - 03:00] ───► MÓDULO 3: CROSS-SITE SCRIPTING (XSS)
                       ├── Teoria: Diferença entre Texto Puro e Execução de Scripts no Navegador
                       ├── Prática: Roubo de cookies desativando o auto-escaping do Jinja2 (| safe)
                       └── Correção: Sanitização seletiva com Allowlist usando a biblioteca Bleach
                       
[03:00 - 04:00] ───► MÓDULO 4: AVALIAÇÃO DINÂMICA (Tomada de Decisão)
                       ├── SE TURMA AVANÇADA: Mini-Desafio CTF Prático com UNION SELECT
                       └── SE POUCO TEMPO: Quiz Teórico de Fixação com 4 Questões de SI

### 🐙 2. Guia de Configuração do Ambiente (Git/GitHub)

### Configuração do Arquivo requirements.txt

Crie um arquivo com este nome exato na raiz do seu repositório: 

text

Flask==3.0.3
SQLAlchemy==2.0.31
bleach==6.1.0
Werkzeug==3.0.3

Use code with caution.

### Comandos para os Alunos (Terminal)

bash

# 1. Clonar o repositório do professor
git clone https://github.com/SEU_USUARIO_GITHUB/minicurso-devsecops-python.git

# 2. Entrar na pasta do projeto
cd minicurso-devsecops-python

# 3. Criar um ambiente virtual
python -m venv venv

# 4. Ativar o ambiente virtual
# No Windows (PowerShell):
.\venv\Scripts\Activate.ps1
# No Linux/Mac:
source venv/bin/activate

# 5. Instalar todas as dependências
pip install -r requirements.txt

Use code with caution.

### 💻 3. Códigos de Exemplo e Explicações Técnicas

### 🏛️ Módulo 1: SQL Injection (SQLi)

### Código Vulnerável (app_vulnerable.py)

python

from flask import Flask, request
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect(":memory:", check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)")
    cursor.execute("INSERT INTO users (username, password) VALUES ('admin', 'SenhaSuperSecreta123')")
    conn.commit()
    return conn

db = init_db()

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    
    cursor = db.cursor()
    # O ERRO: Concatenação direta de strings cria a vulnerabilidade
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    cursor.execute(query)
    user = cursor.fetchone()
    
    if user:
        return f"<h1>Bem-vindo, {user}! Login efetuado com sucesso.</h1>"
    return "<h1>Usuário ou senha incorretos.</h1>", 401

Use code with caution.

### Código Corrigido (app_secure.py)

python

@app.route('/login', methods=['POST'])
def login_secure():
    username = request.form.get('username')
    password = request.form.get('password')
    
    cursor = db.cursor()
    # A CORREÇÃO: Uso de consultas parametrizadas (Placeholders)
    query = "SELECT * FROM users WHERE username = ? AND password = ?"
    cursor.execute(query, (username, password))
    user = cursor.fetchone()
    
    if user:
        return f"<h1>Bem-vindo, {user}!</h1>"
    return "<h1>Falha na autenticação.</h1>", 401

Use code with caution.

**Explicação Técnica:** Ao utilizar o caractere ?, o driver do banco de dados pré-compila a estrutura rígida da query. O input do usuário é enviado por um canal isolado de memória e interpretado estritamente como dado literal (string), impedindo que códigos maliciosos como ' OR '1'='1 alterem a lógica lógica booleana da consulta. 

### 🔑 Módulo 2: IDOR (Insecure Direct Object References)

### Código Vulnerável (app_idor_vulnerable.py)

python

from flask import Flask, request, jsonify

app = Flask(__name__)

INVOICES = {
    1: {"user": "alice", "valor": "R$ 150,00", "status": "Pago"},
    2: {"user": "alice", "valor": "R$ 320,00", "status": "Pendente"},
    3: {"user": "bob", "valor": "R$ 5.000,00", "status": "Pago"}
}

@app.route('/invoice/view', methods=['GET'])
def view_invoice():
    current_user = "alice" # Simulação de usuário logado
    invoice_id = int(request.args.get('id'))
    
    # O ERRO: O sistema busca a fatura pelo ID, mas não checa se ela pertence à Alice
    invoice = INVOICES.get(invoice_id)
    
    if invoice:
        return jsonify(invoice)
    return "Fatura não encontrada", 404

Use code with caution.

### Código Corrigido (app_idor_secure.py)

python

@app.route('/invoice/view', methods=['GET'])
def view_invoice_secure():
    current_user = "alice" 
    invoice_id = int(request.args.get('id'))
    invoice = INVOICES.get(invoice_id)
    
    if not invoice:
        return "Fatura não encontrada", 404
        
    # A CORREÇÃO: Controle de Acesso Baseado em Atributos (ABAC)
    if invoice["user"] != current_user:
        return "Acesso Negado: Você não tem permissão para ver este documento.", 403
        
    return jsonify(invoice)

Use code with caution.

**Explicação Técnica:** A correção impede a confiança cega nos parâmetros vindo do cliente HTTP. O backend intercepta a requisição, valida a identidade do token ou cookie de sessão do usuário logado e confronta essa informação com o campo do proprietário do objeto salvo no banco de dados antes de serializar a resposta. 

### 🎨 Módulo 3: Cross-Site Scripting (XSS)

### Explicação e Exemplo de Sanitização com Bleach

O Jinja2 protege contra XSS por padrão, mas quando desenvolvedores desativam o mecanismo usando o filtro | safe, abrem uma brecha. A solução é higienizar a entrada com uma lista de permissões (*allowlist*): 

python

import bleach

input_do_usuario = "<script>alert('XSS')</script><strong>Texto Legítimo</strong>"
tags_permitidas = ['strong', 'em', 'p', 'br']

# O Python reconstrói a árvore DOM e remove elementos fora da allowlist
dados_limpos = bleach.clean(input_do_usuario, tags=tags_permitidas)
# Resultado: "&lt;script&gt;alert('XSS')&lt;/script&gt;<strong>Texto Legítimo</strong>"

Use code with caution.

### 🛝 4. Roteiro Prontos para os Slides

### Slide 1: Capa

* **Título:** Segurança no Desenvolvimento Web: Pensando como Atacante, Construindo como Engenheiro
* **Subtítulo:** OWASP Top 10 Prático com Python e Flask
* **Facilitador:** [Seu Nome]

### Slide 2: O Cenário Atual e Sistemas de Informação

* **Abordagem Tradicional:** Fazer o software funcionar a qualquer custo (foco apenas em regras de negócio).
* **O Problema:** Vulnerabilidades descobertas tardiamente geram prejuízos financeiros e quebra de conformidade (LGPD).
* **A Solução:** *Security by Design* e *DevSecOps* — Integrar segurança em cada linha de código digitada.
* **O Guia:** OWASP Top 10 como padrão global de mercado para mitigar os riscos mais críticos.

### Slide 3: Módulo 1 - SQL Injection (O Ataque)

* **O que é:** Injeção de comandos SQL arbitrários através de dados fornecidos pelo usuário.
* **A Causa Raiz:** O backend aceita uma string única unificada (Código + Dado) sem separação prévia.
* **Cenário Prático:** Injeção do payload ' OR '1'='1 para quebrar a lógica booleana da cláusula WHERE.

### Slide 4: Módulo 1 - SQL Injection (A Correção)

* **Estratégia Incorreta:** Tentar sanitizar strings manualmente com .replace("'", "") (Facilmente burlável).
* **A Solução Definitiva:** Consultas Parametrizadas (*Prepared Statements* / Placeholders ?).
* **Como Funciona:** O servidor pré-compila a estrutura rígida da query. O input entra estritamente como dado literal.

### Slide 5: Módulo 2 - IDOR (O Ataque)

* **O que é:** *Insecure Direct Object Reference* (Referência Direta Insegura a Objetos).
* **A Causa Raiz:** O sistema confia no identificador numérico enviado diretamente pela requisição HTTP do cliente (URL ou JSON).
* **Falha Conceitual:** Assumir que o fluxo da interface gráfica (UI) dita as regras de autorização do backend.

### Slide 6: Módulo 2 - IDOR (A Correção)

* **O Conceito:** Controle de Acesso Baseado em Atributos (ABAC).
* **A Solução Definitiva:** Validação de Propriedade Cruzada no Servidor.
* **Implementação:** Confrontar se o dono do registro no banco de dados bate com a sessão ativa do usuário antes de entregar o recurso.

### Slide 7: Módulo 3 - XSS e Jinja2 (O Ataque)

* **O que é:** *Cross-Site Scripting* (Injeção de Scripts no Lado do Cliente).
* **Mecanismo do Flask:** O Jinja2 protege a aplicação por padrão através do *Auto-escaping*.
* **A Falha Humana:** O desenvolvedor desativa essa segurança intencionalmente usando o filtro | safe para renderizar formatações de editores de texto estruturados.

### Slide 8: Módulo 3 - XSS e Jinja2 (A Correção)

* **A Solução Definitiva:** Sanitização Avançada de Árvore DOM através de uma Lista de Permissões (*Allowlist*).
* **Uso da Biblioteca Bleach (Mozilla):** O Python reconstrói a estrutura HTML na memória, remove cirurgicamente tags invasoras (<script>) e atributos de eventos (onmouseover), mantendo a formatação visual segura.

### Slide 9: Módulo 4 - Tratamento de Erros Seguro

* **O Risco:** Exibir *Stack Traces* completos ou erros brutos do banco de dados na tela do usuário.
* **O Impacto:** Vazamento de informações de infraestrutura (versão do banco, nomes de tabelas).
