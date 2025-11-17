# lambda-authentication

AWS Lambda function para autenticação de microserviços utilizando JWT (JSON Web Tokens).

## 🎯 Funcionalidades

- **Geração de Token JWT**: Cria tokens de autenticação seguros para microserviços
- **Validação de Token**: Verifica a autenticidade e validade dos tokens
- **Validação de Role**: Controla acesso baseado em roles/permissões do usuário

## 📦 Instalação

```bash
npm install
```

## 🚀 Uso

### Como AWS Lambda

A função pode ser invocada através de API Gateway ou diretamente via AWS SDK. O handler principal está em `index.js`.

#### Estrutura da Requisição

```json
{
  "operation": "generate|validate|validateRole",
  "payload": {},
  "token": "...",
  "requiredRoles": ["admin", "user"],
  "expiresIn": "1h"
}
```

### Operação: Gerar Token

**Request:**
```json
{
  "operation": "generate",
  "payload": {
    "userId": "123",
    "role": "admin",
    "email": "user@example.com"
  },
  "expiresIn": "2h"
}
```

**Response:**
```json
{
  "success": true,
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

### Operação: Validar Token

**Request:**
```json
{
  "operation": "validate",
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Response (Sucesso):**
```json
{
  "success": true,
  "valid": true,
  "decoded": {
    "userId": "123",
    "role": "admin",
    "email": "user@example.com",
    "iat": 1234567890,
    "exp": 1234571490
  }
}
```

**Response (Token Inválido):**
```json
{
  "success": false,
  "valid": false,
  "error": "Token inválido"
}
```

### Operação: Validar Token e Role

**Request:**
```json
{
  "operation": "validateRole",
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "requiredRoles": ["admin", "superadmin"]
}
```

**Response (Sucesso):**
```json
{
  "success": true,
  "valid": true,
  "hasRole": true,
  "decoded": {
    "userId": "123",
    "role": "admin",
    "email": "user@example.com"
  }
}
```

**Response (Sem Permissão):**
```json
{
  "success": false,
  "valid": true,
  "hasRole": false,
  "error": "Usuário não possui a role necessária para acessar este recurso"
}
```

## 🔧 Uso Programático

Você também pode usar as funções diretamente no seu código Node.js:

```javascript
const { generateToken, validateToken, validateRole, validateTokenAndRole } = require('./auth');

// Gerar token
const token = generateToken(
  { userId: '123', role: 'admin' },
  'seu-secret',
  { expiresIn: '1h' }
);

// Validar token
try {
  const decoded = validateToken(token, 'seu-secret');
  console.log('Token válido:', decoded);
} catch (error) {
  console.error('Token inválido:', error.message);
}

// Validar role
const hasRole = validateRole(decoded, 'admin');
console.log('Tem permissão admin:', hasRole);

// Validar token e role em uma operação
const result = validateTokenAndRole(token, 'seu-secret', ['admin', 'user']);
console.log('Resultado:', result);
```

## ⚙️ Configuração

### Variáveis de Ambiente

Configure as seguintes variáveis de ambiente na sua função Lambda:

- `JWT_SECRET`: Chave secreta para assinar e validar tokens JWT (obrigatório em produção)

⚠️ **IMPORTANTE**: Nunca commite secrets no código. Use sempre variáveis de ambiente ou AWS Secrets Manager.

### Exemplo de Configuração na AWS

```bash
aws lambda update-function-configuration \
  --function-name lambda-authentication \
  --environment Variables="{JWT_SECRET=seu-secret-super-seguro}"
```

## 🧪 Testes

Execute os testes automatizados:

```bash
npm test
```

Os testes cobrem:
- Geração de tokens válidos e inválidos
- Validação de tokens
- Validação de roles
- Cenários de erro

## 📋 Códigos de Status HTTP

- `200`: Operação bem-sucedida
- `400`: Requisição inválida (parâmetros faltando ou inválidos)
- `401`: Token inválido ou expirado
- `403`: Token válido mas usuário sem permissão (role incorreta)
- `500`: Erro interno do servidor

## 🔐 Segurança

- Use sempre uma chave secreta forte e única (`JWT_SECRET`)
- Configure tempos de expiração apropriados para seus tokens
- Use HTTPS em todas as comunicações
- Rotacione suas chaves secretas periodicamente
- Não inclua informações sensíveis no payload do token

## 📚 Estrutura do Projeto

```
lambda-authentication/
├── index.js          # Lambda handler principal
├── auth.js           # Funções de autenticação
├── test/
│   └── test.js       # Testes automatizados
├── package.json
└── README.md
```

## 🏗️ Deploy na AWS

### Usando AWS CLI

```bash
# Criar arquivo ZIP
zip -r function.zip index.js auth.js node_modules/

# Criar função Lambda
aws lambda create-function \
  --function-name lambda-authentication \
  --runtime nodejs18.x \
  --role arn:aws:iam::ACCOUNT_ID:role/lambda-role \
  --handler index.handler \
  --zip-file fileb://function.zip

# Atualizar função existente
aws lambda update-function-code \
  --function-name lambda-authentication \
  --zip-file fileb://function.zip
```

### Usando Terraform

```hcl
resource "aws_lambda_function" "authentication" {
  filename      = "function.zip"
  function_name = "lambda-authentication"
  role          = aws_iam_role.lambda_role.arn
  handler       = "index.handler"
  runtime       = "nodejs18.x"

  environment {
    variables = {
      JWT_SECRET = var.jwt_secret
    }
  }
}
```

## 🤝 Contribuindo

FIAP SOAT - Grupo 36

## 📄 Licença

ISC
