# 🛡️ Minicurso: Segurança no Desenvolvimento Web com Python

Bem-vindos ao repositório oficial do minicurso prático de Segurança em Backend com Python! 

Neste laboratório, vamos explorar na prática três das principais vulnerabilidades mapeadas pelo **OWASP Top 10**: SQL Injection (SQLi), Insecure Direct Object Reference (IDOR) e Cross-Site Scripting (XSS). Usaremos o **OWASP Juice Shop** para a fase de ataque e uma aplicação **Flask (Python)** para a fase de defesa e correção de código.

---

## 🛠️ Como subir o ambiente na sua máquina

Para garantir que todos tenham o mesmo ambiente isolado e sem conflitos de dependências, utilizaremos o **Docker**.

### Pré-requisitos (Se já estiver instalado e com as devidas permissões)
* [Docker](https://docs.docker.com/get-docker/) instalado.
* [Docker Compose](https://docs.docker.com/compose/install/) instalado (já embutido nas versões recentes do Docker Desktop).
* Um cliente de requisições HTTP (Postman, Insomnia, Hoppscotch) ou o próprio navegador.

### Passo a passo

1. Clone este repositório:
   ```bash
   git clone [https://github.com/seu-usuario/minicurso-owasp-python.git](https://github.com/seu-usuario/minicurso-owasp-python.git)
   cd minicurso-owasp-python
   ```
2. Suba os containers do laboratório:
   ```bash
   docker compose up -d --build
   ```
3. Verifique se os serviços estão no ar:
   * **Lab CTF Flask (Alvo de Defesa):** `http://localhost:5050`

### Segunda alternativa (através do VirtualBox) - JuiceShopped

Unofficial VirtualBox virtual machine instance of OWASP Juice Shop

### Contributors: [Aut0exec](https://aut0exec.blogspot.com)

1. Crie um diretório na unidadade D: da máquina do aluno

2. Copie a máquina virtual empacotada no formato OVA:
   ```bash
      caminho: \\g7clab03-000\dados$
   ```
3. Importe a máquina vm no virtualbox
   ```bash
   obs.: quando aparecer perguntando para onde será instalado a VM, aponte para o disco local D,
   exemplo: D:\Virtual Box VMs o sistema irá criar o diretório automáticamente
   ```
## Features
	- Devuan Excalibur instance
	- Pre-installed and configured to auto start on boot
		- OWASP Juice Shop version 19.0.0 Node 20
		- VAmPI - Vulnerable API

## Relevant Information

While there shouldn't be a need to log in to the console, should one need to, the information is as follows:

Low privilege user  - __user__:__Password123__

Root privilege user - __root__:__juiceisworththesqueeze__

## Installation - source page

__WARNING!__ Juice Shop is designed to be vulnerable. __DO NOT__ connect this VM to the Internet or sensitive networks.

1. Download the OVA from the [releases page](https://github.com/aut0exec/JuiceShopped/releases)
2. Launch virtualbox
3. File -> Import Appliance
4. Under the source section, select Local File System and then navigate to the location where the OVA file was downloaded
5. The default settings should be sufficient on the right side of the import window
6. Click Import in the bottom right to import the appliance
7. Once the import finishes, start Juice Shop. The machine expects a DHCP server to be present and will automatically request an address.
	- VirtualBox will automatically configure port forwards from the host to the guest for ports TCP/3000 and TCP/5000. Any scanning or interaction from the host with the virtual machine can be done via 127.0.0.1:3000 or 127.0.0.1:5000.

---

## 💻 Desafios de Código (O alcance esperado)

Abaixo estão os trechos de código do nosso backend Python (`ctf_app.py`) que contêm falhas críticas de segurança. Durante a aula, discutiremos por que eles são perigosos e como corrigi-los. 

> ⚠️ **Atenção:** As versões corrigidas (Gabarito) serão postadas nos espaços em branco ao final do minicurso!

### Desafio 1: SQL Injection (SQLi)
**Local:** Rota `/ctf/api/login`  
**O Problema:** A aplicação recebe os dados do usuário e concatena diretamente na string da query SQL, permitindo manipulação da lógica de autenticação.

🔴 **Código Vulnerável:**
```python
@app.route('/ctf/api/login', methods=['POST'])
def ctf_login():
    user = request.json.get('username', '')
    pwd = request.json.get('password', '')
    
    # ❌ VULNERABILIDADE: Concatenação direta de strings na query
    query = f"SELECT username, flag FROM ctf_users WHERE username = '{user}' AND password = '{pwd}'"
    
    cursor.execute(query)
    # ... resto do código ...
```

🟢 **Código Corrigido (Será liberado durante o minicurso):**
```python
# [O CÓDIGO SEGURO COM QUERIES PARAMETRIZADAS SERÁ POSTADO AQUI]
```

---

### Desafio 2: Insecure Direct Object Reference (IDOR)
**Local:** Rota `/ctf/api/orders/<int:order_id>`  
**O Problema:** A API confia cegamente no identificador (`order_id`) passado na URL, sem verificar se o usuário autenticado realmente tem permissão para acessar aquele pedido.

🔴 **Código Vulnerável:**
```python
@app.route('/ctf/api/orders/<int:order_id>', methods=['GET'])
def ctf_get_order(order_id):
    # ❌ VULNERABILIDADE: Busca o pedido apenas pelo ID, sem checar a posse (user_id)
    cursor.execute("SELECT id, user_id, item, flag_note FROM ctf_orders WHERE id = ?", (order_id,))
    order = cursor.fetchone()
    # ... resto do código ...
```

🟢 **Código Corrigido (Será liberado durante o minicurso):**
```python
# [O CÓDIGO SEGURO COM CONTROLE DE ACESSO BASEADO EM IDENTIDADE (BOLA) SERÁ POSTADO AQUI]
```

---

### Desafio 3: Cross-Site Scripting (XSS) Stored
**Local:** Rota `/ctf/reviews` e Template HTML  
**O Problema:** O backend aceita textos com tags HTML maliciosas (`<script>`) e o template renderiza esse conteúdo no navegador dos outros usuários sem realizar o escape (sanitização).

🔴 **Código Vulnerável:**
```python
# No backend: Salva o texto bruto direto no banco de dados
cursor.execute("INSERT INTO ctf_reviews (author, comment) VALUES (?, ?)", (author, comment))
```
```html
<!-- No Frontend (Jinja2): O uso do filtro | safe desabilita a proteção nativa -->
<div class="review">
    <strong>{{ r[0] }}</strong>: <span>{{ r[1] | safe }}</span>
</div>
```

🟢 **Código Corrigido (Será liberado durante o minicurso):**
```python
# [O CÓDIGO SEGURO UTILIZANDO A BIBLIOTECA BLEACH PARA SANITIZAÇÃO SERÁ POSTADO AQUI]
```

---

## 🚩 Mini-CTF (Capture The Flag)

Ao final da nossa análise, vocês colocarão o chapéu de atacante ("Red Team") e tentarão explorar essas vulnerabilidades no nosso servidor local Flask (porta 5050) para roubar as **Flags** (ex: `FLAG{texto_da_flag}`).

- **Desafio 1 (SQLi):** Encontre a chave do cofre do usuário "admin".
- **Desafio 2 (IDOR):** Acesse as notas do pedido de número 101.
- **Desafio 3 (XSS):** Roube o cookie de sessão do Moderador.

As pontuações serão registradas ao vivo no nosso painel do CTFd. Boa sorte e bom hacking (ético)!

---
*Minicurso - XV TECVALE - Encontro Tecnológico do Vale do São Francisco.*  
*Centro Universitário do Vale do São Francisco - UNIRIOS.*
*Desenvolvido pelo Professor: Erick Barros Nascimento.*
