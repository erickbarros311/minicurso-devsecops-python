from flask import Flask, request, render_template_string
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

app = Flask(__name__)
# Banco de dados SQLite em memória
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modelo da tabela de usuários
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

# Prepara o banco com usuários de teste
with app.app_context():
    db.create_all()
    user_admin = User(email='admin@empresa.com', password='SenhaSuperSecreta123')
    user_comum = User(email='usuario@empresa.com', password='SenhaComum123')
    db.session.add_all([user_admin, user_comum])
    db.session.commit()

# Interface HTML com CSS integrado para visualização
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <title>Laboratório SQL Injection-Insecure_App</title>
    <style>
        body { font-family: Arial, sans-serif; background: #1e1e2e; color: #cdd6f4; display: flex; justify-content: center; align-items: center; min-height: 100vh; margin: 0; }
        .card { background: #313244; padding: 30px; border-radius: 8px; box-shadow: 0 4px 15px rgba(0,0,0,0.5); width: 380px; }
        h2 { text-align: center; margin-top: 0; color: #a6e3a1; }
        .form-group { margin-bottom: 15px; }
        label { display: block; margin-bottom: 5px; font-size: 14px; }
        input[type="text"] { width: 100%; padding: 10px; border: 1px solid #45475a; border-radius: 4px; background: #181825; color: #cdd6f4; box-sizing: border-box; }
        button { width: 100%; padding: 10px; background: #a6e3a1; border: none; border-radius: 4px; color: #11111b; font-weight: bold; cursor: pointer; margin-top: 10px; font-size: 16px; }
        button:hover { background: #94e2d5; }
        .msg { margin-top: 15px; padding: 10px; border-radius: 4px; text-align: center; word-break: break-all; }
        .success { background: #27412e; color: #a6e3a1; border: 1px solid #a6e3a1; }
        .error { background: #44232f; color: #f38ba8; border: 1px solid #f38ba8; }
        .debug-box { margin-top: 20px; font-size: 12px; background: #11111b; padding: 10px; border-left: 3px solid #f9e2af; border-radius: 4px; font-family: monospace; word-break: break-all; }
    </style>
</head>
<body>
    <div class="card">
        <h2>Portal de Login</h2>
        <form action="/login" method="POST">
            <div class="form-group">
                <label for="email">E-mail / Usuário:</label>
                <!-- Campo texto aberto para aceitar caracteres especiais de SQL Injection -->
                <input type="text" id="email" name="email" required value="{{ email_input or '' }}">
            </div>
            <div class="form-group">
                <label for="password">Senha:</label>
                <input type="text" id="password" name="password" value="{{ password_input or '' }}">
            </div>
            <button type="submit">Entrar</button>
        </form>

        {% if result %}
            <div class="msg {{ result_status }}">
                {{ result }}
            </div>
        {% endif %}

        {% if executed_query %}
            <div class="debug-box">
                <strong>Query SQL Gerada no Servidor:</strong><br><br>
                <code>{{ executed_query }}</code>
            </div>
        {% endif %}
    </div>
</body>
</html>
'''

@app.route('/', methods=['GET'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Captura os dados vindos do formulário HTML
        email = request.form.get('email', '')
        password = request.form.get('password', '')

        # VULNERABILIDADE: Concatenação direta de valores recebidos do formulário
        query = f"SELECT * FROM users WHERE email = '{email}' AND password = '{password}'"

        try:
            user = db.session.execute(text(query)).fetchone()
            if user:
                return render_template_string(
                    HTML_TEMPLATE,
                    result=f"Sucesso! Autenticado como: {user.email}",
                    result_status="success",
                    executed_query=query,
                    email_input=email,
                    password_input=password
                )
            else:
                return render_template_string(
                    HTML_TEMPLATE,
                    result="Falha na autenticação: Credenciais inválidas.",
                    result_status="error",
                    executed_query=query,
                    email_input=email,
                    password_input=password
                )
        except Exception as e:
            return render_template_string(
                HTML_TEMPLATE,
                result=f"Erro de Execução SQL: {str(e)}",
                result_status="error",
                executed_query=query,
                email_input=email,
                password_input=password
            )

    return render_template_string(HTML_TEMPLATE)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)