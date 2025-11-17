// Exemplos de uso da Lambda de Autenticação

const { handler } = require('./index');

// Exemplos de eventos que podem ser enviados para a Lambda

// ============================================
// Exemplo 1: Gerar Token de Autenticação
// ============================================
const generateTokenEvent = {
  body: JSON.stringify({
    operation: 'generate',
    payload: {
      userId: '12345',
      role: 'admin',
      email: 'admin@example.com',
      name: 'Admin User'
    },
    expiresIn: '2h' // Opcional, padrão é 1h
  })
};

console.log('=== Exemplo 1: Gerar Token ===');
handler(generateTokenEvent).then(response => {
  console.log('Status:', response.statusCode);
  console.log('Response:', JSON.parse(response.body));
  console.log('\n');
  
  // Salvar token para próximos exemplos
  const tokenData = JSON.parse(response.body);
  const token = tokenData.token;
  
  // ============================================
  // Exemplo 2: Validar Token
  // ============================================
  const validateTokenEvent = {
    body: JSON.stringify({
      operation: 'validate',
      token: token
    })
  };
  
  console.log('=== Exemplo 2: Validar Token ===');
  return handler(validateTokenEvent);
}).then(response => {
  console.log('Status:', response.statusCode);
  console.log('Response:', JSON.parse(response.body));
  console.log('\n');
  
  // ============================================
  // Exemplo 3: Validar Token com Role Correta
  // ============================================
  // Primeiro, gerar um token com role específica
  const generateAdminTokenEvent = {
    body: JSON.stringify({
      operation: 'generate',
      payload: {
        userId: '99999',
        role: 'admin',
        email: 'admin@example.com'
      }
    })
  };
  
  return handler(generateAdminTokenEvent);
}).then(response => {
  const tokenData = JSON.parse(response.body);
  const adminToken = tokenData.token;
  
  const validateRoleEvent = {
    body: JSON.stringify({
      operation: 'validateRole',
      token: adminToken,
      requiredRoles: ['admin', 'superadmin'] // Aceita qualquer uma dessas roles
    })
  };
  
  console.log('=== Exemplo 3: Validar Token e Role (Sucesso) ===');
  return handler(validateRoleEvent);
}).then(response => {
  console.log('Status:', response.statusCode);
  console.log('Response:', JSON.parse(response.body));
  console.log('\n');
  
  // ============================================
  // Exemplo 4: Validar Token com Role Incorreta
  // ============================================
  const generateUserTokenEvent = {
    body: JSON.stringify({
      operation: 'generate',
      payload: {
        userId: '88888',
        role: 'user',
        email: 'user@example.com'
      }
    })
  };
  
  return handler(generateUserTokenEvent);
}).then(response => {
  const tokenData = JSON.parse(response.body);
  const userToken = tokenData.token;
  
  const validateRoleEvent = {
    body: JSON.stringify({
      operation: 'validateRole',
      token: userToken,
      requiredRoles: 'admin' // Requer role admin
    })
  };
  
  console.log('=== Exemplo 4: Validar Token e Role (Falha - Role Incorreta) ===');
  return handler(validateRoleEvent);
}).then(response => {
  console.log('Status:', response.statusCode);
  console.log('Response:', JSON.parse(response.body));
  console.log('\n');
  
  // ============================================
  // Exemplo 5: Validar Token Inválido
  // ============================================
  const invalidTokenEvent = {
    body: JSON.stringify({
      operation: 'validate',
      token: 'token-invalido-123'
    })
  };
  
  console.log('=== Exemplo 5: Validar Token Inválido ===');
  return handler(invalidTokenEvent);
}).then(response => {
  console.log('Status:', response.statusCode);
  console.log('Response:', JSON.parse(response.body));
  console.log('\n');
  
  // ============================================
  // Exemplo 6: Token com Múltiplas Roles
  // ============================================
  const generateMultiRoleTokenEvent = {
    body: JSON.stringify({
      operation: 'generate',
      payload: {
        userId: '77777',
        role: ['user', 'moderator', 'admin'],
        email: 'superuser@example.com'
      }
    })
  };
  
  return handler(generateMultiRoleTokenEvent);
}).then(response => {
  const tokenData = JSON.parse(response.body);
  const multiRoleToken = tokenData.token;
  
  const validateMultiRoleEvent = {
    body: JSON.stringify({
      operation: 'validateRole',
      token: multiRoleToken,
      requiredRoles: ['moderator'] // Usuário tem essa role
    })
  };
  
  console.log('=== Exemplo 6: Token com Múltiplas Roles ===');
  return handler(validateMultiRoleEvent);
}).then(response => {
  console.log('Status:', response.statusCode);
  console.log('Response:', JSON.parse(response.body));
  console.log('\n');
  
  // ============================================
  // Exemplo 7: Operação Inválida
  // ============================================
  const invalidOperationEvent = {
    body: JSON.stringify({
      operation: 'operacao-invalida'
    })
  };
  
  console.log('=== Exemplo 7: Operação Inválida ===');
  return handler(invalidOperationEvent);
}).then(response => {
  console.log('Status:', response.statusCode);
  console.log('Response:', JSON.parse(response.body));
  console.log('\n');
  
  console.log('=== Todos os exemplos executados com sucesso! ===');
}).catch(error => {
  console.error('Erro ao executar exemplos:', error);
});

/* 
  Exemplos de integração com API Gateway:
  
  POST /auth
  Body:
  {
    "operation": "generate",
    "payload": {
      "userId": "123",
      "role": "admin"
    }
  }
  
  POST /auth
  Body:
  {
    "operation": "validate",
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
  }
  
  POST /auth
  Body:
  {
    "operation": "validateRole",
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "requiredRoles": ["admin"]
  }
*/
