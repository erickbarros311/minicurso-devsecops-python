const express = require('express');
const app = express();
const port = 3000;

// Banco de dados fictício em memória
const bancoDeDados = [
  { id: 1, nome: "Admin (Alice)", segredo: "Senha do servidor de provas: admin123" },
  { id: 2, nome: "Aluno (Bob)", segredo: "Estou pensando em trancar o curso." },
  { id: 3, nome: "Aluno (Charlie)", segredo: "Eu copiei o trabalho final." }
];

// Middleware de Autenticação Simulado
// Lê o ID do usuário através do header "Authorization: Bearer <id>"
const mockAuth = (req, res, next) => {
  const token = req.headers['authorization'];
  if (!token) {
    return res.status(401).json({ erro: "Acesso negado. Token não fornecido." });
  }
  
  // Extrai o ID fictício do token (Ex: 'Bearer 2' -> 2)
  const userId = parseInt(token.split(' ')[1]);
  req.usuarioLogadoId = userId; 
  next();
};

// ==========================================
// ROTA CORRIGIDA - Segura (IDOR)
// ==========================================
app.get('/api/alunos/:id', mockAuth, (req, res) => {
  // O servidor pega o ID da URL solicitado pelo cliente
  const idSolicitado = parseInt(req.params.id);

  // CORREÇÃO: Verifica se o ID da URL é igual ao ID do usuário autenticado!
  if (idSolicitado !== req.usuarioLogadoId){
    return res.status(403).json({ erro: "Acesso Negado: Você só tem permissão para visualizar seus prórpios dados."})
  }
 
  const aluno = bancoDeDados.find(a => a.id === idSolicitado);

  if (!aluno) {
    return res.status(404).json({ erro: "Aluno não encontrado." });
  }

  res.json(aluno);
});

app.listen(port, () => {
  console.log(`Servidor Seguro rodando em http://localhost:${port}`);
});
