## 🔒 Minicurso Prático: Segurança Web com Python e Flask

Este documento contém o planejamento pedagógico completo, códigos-fonte, guia de laboratório e material para slides voltado para alunos de Sistemas de Informação.

### 🗺️ 1. Cronograma e Configuração do Ambiente

**Roadmap do Curso (4 Horas)**

| Horário | Módulo | Foco Teórico | Atividade Prática | Correção Aplicada |
| :--- | :--- | :--- | :--- | :--- |
| **00h - 01h** | 1: SQL Injection | OWASP Top 10 e Árvores SQL | Burlar login com `' OR '1'='1` | Consultas Parametrizadas |
| **01h - 02h** | 2: IDOR | Controle de Acesso e HTTP | Alterar URL para acessar dados | Validação de escopo (ABAC) |
| **02h - 03h** | 3: XSS | Texto Puro vs Execução DOM | Roubo de cookies via Jinja2 | Sanitização com *Bleach* |
| **03h - 04h** | 4: Avaliação | Tomada de Decisão | Desafio CTF ou Quiz Teórico | Revisão Geral |

**Guia de Configuração (Terminal e Dependências)**

Crie um arquivo `requirements.txt` na raiz do repositório:

```text
Flask==3.0.3
SQLAlchemy==2.0.31
bleach==6.1.0
Werkzeug==3.0.3
```

Execute os comandos abaixo para configurar o laboratório:

```bash
# 1. Clonar o repositório e acessar a pasta
git clone https://github.com/SEU_USUARIO_GITHUB/minicurso-devsecops-python.git
cd minicurso-devsecops-python

# 2. Criar e ativar o ambiente virtual (Windows PowerShell / Linux)
python -m venv venv
.\venv\Scripts\Activate.ps1  # Windows
source venv/bin/activate     # Linux/Mac

# 3. Instalar dependências
pip install -r requirements.txt
```

---

### 🏛️ 2. Módulo 1 e 2: Vulnerabilidades de Backend (SQLi e IDOR)

**SQL Injection (SQLi)**
A concatenação direta de strings cria a vulnerabilidade. Ao utilizar o caractere `?` (Placeholders), o banco de dados pré-compila a query, tratando o input estritamente como texto.

```python
from flask import Flask, request
import sqlite3

app = Flask(__name__)

# ❌ CÓDIGO VULNERÁVEL (app_vulnerable.py)
@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    cursor = db.cursor()
    
    # ERRO: Concatenação direta de strings
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    cursor.execute(query)
    
    if cursor.fetchone():
        return "<h1>Login efetuado com sucesso.</h1>"
    return "<h1>Usuário ou senha incorretos.</h1>", 401

# ✅ CÓDIGO CORRIGIDO (app_secure.py)
@app.route('/login_secure', methods=['POST'])
def login_secure():
    username = request.form.get('username')
    password = request.form.get('password')
    cursor = db.cursor()
    
    # CORREÇÃO: Uso de consultas parametrizadas
    query = "SELECT * FROM users WHERE username = ? AND password = ?"
    cursor.execute(query, (username, password))
    
    if cursor.fetchone():
        return "<h1>Login efetuado com sucesso!</h1>"
    return "<h1>Falha na autenticação.</h1>", 401
```

**IDOR (Insecure Direct Object References)**
O sistema não deve confiar no ID enviado pelo cliente. É preciso validar a identidade (sessão) e confrontar com o proprietário do dado no banco (ABAC).

```python
from flask import Flask, request, jsonify

INVOICES = {
    1: {"user": "alice", "valor": "R$ 150,00"},
    2: {"user": "bob", "valor": "R$ 5.000,00"}
}

# ❌ CÓDIGO VULNERÁVEL
@app.route('/invoice/view', methods=['GET'])
def view_invoice():
    invoice_id = int(request.args.get('id'))
    invoice = INVOICES.get(invoice_id) # ERRO: Não checa quem é o dono
    
    return jsonify(invoice) if invoice else ("Não encontrada", 404)

# ✅ CÓDIGO CORRIGIDO
@app.route('/invoice/view_secure', methods=['GET'])
def view_invoice_secure():
    current_user = "alice" # Simulação de sessão
    invoice_id = int(request.args.get('id'))
    invoice = INVOICES.get(invoice_id)
    
    if not invoice:
        return "Fatura não encontrada", 404
        
    # CORREÇÃO: Controle de Acesso Baseado em Atributos (ABAC)
    if invoice["user"] != current_user:
        return "Acesso Negado.", 403
        
    return jsonify(invoice)
```

---

### 🎨 3. Módulo 3: Frontend e XSS (Cross-Site Scripting)

O Jinja2 protege contra XSS nativamente, mas o uso da flag `| safe` abre brechas. A solução é higienizar a entrada com uma *allowlist* usando a biblioteca Bleach.

```python
import bleach

input_do_usuario = "<script>alert('XSS')</script><strong>Texto Legítimo</strong>"
tags_permitidas = ['strong', 'em', 'p', 'br']

# O Python reconstrói a árvore DOM e remove elementos maliciosos
dados_limpos = bleach.clean(input_do_usuario, tags=tags_permitidas)

print(dados_limpos)
# Saída: &lt;script&gt;alert('XSS')&lt;/script&gt;<strong>Texto Legítimo</strong>
```

---

### 🛝 4. Estrutura Base para os Slides

*   **Introdução e Cenário:** 
    *   O problema da abordagem tradicional (foco apenas em regras de negócio).
    *   A solução via *Security by Design*, integração *DevSecOps* e o padrão global OWASP Top 10.
*   **Ataques e Defesas:**
    *   **SQLi:** A causa raiz é a união de código e dado. Defesa: *Prepared Statements*. Evite sanitização manual (ex: `.replace()`).
    *   **IDOR:** A causa raiz é assumir que o fluxo da UI dita as regras de autorização. Defesa: Validação de Propriedade Cruzada no Servidor (ABAC).
    *   **XSS:** A injeção de scripts no cliente, geralmente causada por desativar o *Auto-escaping*. Defesa: Sanitização avançada de DOM (ex: *Bleach*).
*   **Tratamento de Erros:** Exibir *Stack Traces* completos vaza informações sensíveis de infraestrutura. Trate exceções silenciosamente no frontend e gere logs seguros no backend.
