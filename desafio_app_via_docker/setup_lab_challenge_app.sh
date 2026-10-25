#!/bin/bash

echo "🚀 Iniciando a configuração do Laboratório CTF - OWASP Top 10..."

# 1. Cria a pasta do projeto e entra nela
mkdir -p app_desafios
cd app_desafios

# 2. Cria o arquivo requirements.txt
echo "📦 Criando requirements.txt..."
cat << 'EOF' > requirements.txt
Flask
EOF

# 3. Cria o Dockerfile
echo "🐳 Criando Dockerfile..."
cat << 'EOF' > Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Copia dependências e instala
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia a aplicação
COPY ctf_app.py .

EXPOSE 5050

CMD ["python", "ctf_app.py"]
EOF

# 4. Cria o docker-compose.yml
echo "🐙 Criando docker-compose.yml..."
cat << 'EOF' > docker-compose.yml
version: '3.8'

services:
  app_ctf:
    build: .
    ports:
      - "5050:5050"
    restart: always
EOF

# 5. Cria o código-fonte da aplicação (ctf_app.py)
echo "🐍 Criando ctf_app.py..."
cat << 'EOF' > ctf_app.py
import sqlite3
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)
app.secret_key = "ctf-secret-key"

def init_ctf_db():
    conn = sqlite3.connect("ctf.db")
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ctf_users (
            id INTEGER PRIMARY KEY, username TEXT, password TEXT, flag TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ctf_orders (
            id INTEGER PRIMARY KEY, user_id INTEGER, item TEXT, flag_note TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ctf_reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT, author TEXT, comment TEXT
        )
    """)

    cursor.execute("DELETE FROM ctf_users")
    cursor.execute("DELETE FROM ctf_orders")
    cursor.execute("DELETE FROM ctf_reviews")

    cursor.execute("INSERT INTO ctf_users VALUES (1, 'admin', 'SuperComplexPassword!@#99', 'FLAG{sqli_bypass_auth_master}')")
    cursor.execute("INSERT INTO ctf_users VALUES (2, 'aluno', '123456', 'Sem flag aqui!')")
    
    cursor.execute("INSERT INTO ctf_orders VALUES (101, 1, 'Servidor Blade Xeon', 'FLAG{idor_object_reference_exposed}')")
    cursor.execute("INSERT INTO ctf_orders VALUES (102, 2, 'Cabo de Rede RJ45', 'Pedido normal do aluno')")

    conn.commit()
    conn.close()

init_ctf_db()

@app.route('/ctf/api/login', methods=['POST'])
def ctf_login():
    user = request.json.get('username', '')
    pwd = request.json.get('password', '')
    conn = sqlite3.connect("ctf.db")
    cursor = conn.cursor()
    
    query = f"SELECT username, flag FROM ctf_users WHERE username = '{user}' AND password = '{pwd}'"
    try:
        cursor.execute(query)
        account = cursor.fetchone()
        if account:
            return jsonify({"status": "Autenticado!", "usuario": account[0], "dado_confidencial": account[1]})
        return jsonify({"erro": "Credenciais invalidas"}), 401
    except Exception as e:
        return jsonify({"db_error": str(e)}), 500
    finally:
        conn.close()

@app.route('/ctf/api/orders/<int:order_id>', methods=['GET'])
def ctf_get_order(order_id):
    conn = sqlite3.connect("ctf.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, user_id, item, flag_note FROM ctf_orders WHERE id = ?", (order_id,))
    order = cursor.fetchone()
    conn.close()
    if not order:
        return jsonify({"erro": "Pedido nao encontrado"}), 404
    return jsonify({"order_id": order[0], "item": order[2], "observacoes": order[3]})

MODERATOR_FLAG_COOKIE = "FLAG{xss_stored_cookie_stealer}"

@app.route('/ctf/reviews', methods=['GET', 'POST'])
def ctf_reviews():
    conn = sqlite3.connect("ctf.db")
    cursor = conn.cursor()
    if request.method == 'POST':
        comment = request.form.get('comment', '')
        author = request.form.get('author', 'Anonimo')
        cursor.execute("INSERT INTO ctf_reviews (author, comment) VALUES (?, ?)", (author, comment))
        conn.commit()

    cursor.execute("SELECT author, comment FROM ctf_reviews")
    reviews = cursor.fetchall()
    conn.close()

    html = """
    <!DOCTYPE html>
    <html>
    <head><title>CTF - Painel de Feedback</title></head>
    <body style="font-family:sans-serif; margin:40px;">
        <h2>Deixe seu Feedback</h2>
        <form method="POST">
            Nome: <input type="text" name="author"><br><br>
            Comentario: <textarea name="comment" rows="4" cols="50"></textarea><br><br>
            <button type="submit">Enviar Comentario</button>
        </form>
        <hr>
        <h3>Feedbacks Publicados:</h3>
        {% for r in reviews %}
            <div style="border:1px solid #ccc; padding:10px; margin-bottom:10px;">
                <strong>{{ r[0] }}</strong>: <span>{{ r[1] | safe }}</span>
            </div>
        {% endfor %}
        <script>document.cookie = "auth_session=" + "{{ mod_flag }}";</script>
    </body>
    </html>
    """
    return render_template_string(html, reviews=reviews, mod_flag=MODERATOR_FLAG_COOKIE)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050, debug=False)
EOF

# 6. Sobe a infraestrutura usando Docker Compose
echo "⚙️ Inicializando os containers..."
docker compose up -d --build

echo "✅ Pronto! Aplicação disponível em: http://localhost:5050/ctf/reviews"