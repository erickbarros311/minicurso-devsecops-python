from flask import Flask, request, render_template_string

app = Flask(__name__)

# O filtro "| safe" diz ao Jinja2: "Confie neste conteúdo, renderize como HTML"
TEMPLATE_VULNERAVEL = """
<!DOCTYPE html>
<html>
<body>
    <h2>Sistema de Comentários</h2>
    <p>O que os usuários estão dizendo:</p>
    <div style="border: 1px solid #ccc; padding: 10px;">
        {{ comentario | safe }}
    </div>
</body>
</html>
"""

@app.route('/')
def index():
    # Simulando um comentário vindo da URL
    comentario_usuario = request.args.get('comentario', 'Deixe seu comentário!')
    return render_template_string(TEMPLATE_VULNERAVEL, comentario=comentario_usuario)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
