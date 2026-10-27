import bleach
from flask import Flask, request, render_template_string

app = Flask(__name__)

TEMPLATE_SEGURO = """
<!DOCTYPE html>
<html>
<body>
    <h2>Sistema de Comentários (Protegido)</h2>
    <p>O que os usuários estão dizendo:</p> 
    <div style="border: 1px solid #ccc; padding: 10px;">
        {{ comentario | safe }}
    </div>
</body>
</html>
"""

# 1. Definimos o que é permitido (Whitelist)
TAGS_PERMITIDAS = ['b', 'i', 'u', 'em', 'strong', 'a']
ATRIBUTOS_PERMITIDOS = {
    'a': ['href', 'title'] # Permite apenas links com href e title
}

@app.route('/')
def index():
    comentario_usuario = request.args.get('comentario', 'Deixe seu comentário!')

    # 2. Sanitizamos a entrada com Bleach ANTES de enviar para o template
    comentario_limpo = bleach.clean(
        comentario_usuario,
        tags=TAGS_PERMITIDAS,
        attributes=ATRIBUTOS_PERMITIDOS
    )

    # 3. Agora é seguro usar o | safe no template
    return render_template_string(TEMPLATE_SEGURO, comentario=comentario_limpo)

if __name__ == '__main__':
    app.run(debug=True, port=5001)