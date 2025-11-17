const { generateToken, validateToken, validateRole, validateTokenAndRole } = require('../auth');

// Cores para output
const colors = {
  green: '\x1b[32m',
  red: '\x1b[31m',
  yellow: '\x1b[33m',
  reset: '\x1b[0m'
};

let testsPassed = 0;
let testsFailed = 0;

function assert(condition, testName) {
  if (condition) {
    console.log(`${colors.green}✓${colors.reset} ${testName}`);
    testsPassed++;
  } else {
    console.log(`${colors.red}✗${colors.reset} ${testName}`);
    testsFailed++;
  }
}

function assertThrows(fn, testName) {
  try {
    fn();
    console.log(`${colors.red}✗${colors.reset} ${testName} - não lançou erro`);
    testsFailed++;
  } catch (error) {
    console.log(`${colors.green}✓${colors.reset} ${testName}`);
    testsPassed++;
  }
}

console.log('\n=== Testes de Geração de Token ===\n');

// Teste 1: Geração básica de token
try {
  const token = generateToken({ userId: '123', role: 'admin' }, 'test-secret');
  assert(typeof token === 'string' && token.length > 0, 'Deve gerar token válido');
} catch (error) {
  assert(false, 'Deve gerar token válido');
}

// Teste 2: Token com payload customizado
try {
  const token = generateToken({ 
    userId: '456', 
    role: 'user', 
    email: 'test@example.com' 
  }, 'test-secret');
  assert(typeof token === 'string' && token.length > 0, 'Deve gerar token com payload customizado');
} catch (error) {
  assert(false, 'Deve gerar token com payload customizado');
}

// Teste 3: Token com expiração customizada
try {
  const token = generateToken({ userId: '789' }, 'test-secret', { expiresIn: '2h' });
  assert(typeof token === 'string' && token.length > 0, 'Deve gerar token com expiração customizada');
} catch (error) {
  assert(false, 'Deve gerar token com expiração customizada');
}

// Teste 4: Erro ao gerar token sem payload
assertThrows(() => {
  generateToken(null, 'test-secret');
}, 'Deve lançar erro ao gerar token sem payload');

// Teste 5: Erro ao gerar token sem secret
assertThrows(() => {
  generateToken({ userId: '123' }, null);
}, 'Deve lançar erro ao gerar token sem secret');

console.log('\n=== Testes de Validação de Token ===\n');

// Teste 6: Validação de token válido
try {
  const token = generateToken({ userId: '123', role: 'admin' }, 'test-secret');
  const decoded = validateToken(token, 'test-secret');
  assert(decoded.userId === '123' && decoded.role === 'admin', 'Deve validar token válido corretamente');
} catch (error) {
  assert(false, 'Deve validar token válido corretamente');
}

// Teste 7: Erro ao validar token com secret incorreto
try {
  const token = generateToken({ userId: '123' }, 'test-secret');
  assertThrows(() => {
    validateToken(token, 'wrong-secret');
  }, 'Deve lançar erro ao validar token com secret incorreto');
} catch (error) {
  assert(false, 'Erro inesperado no teste de secret incorreto');
}

// Teste 8: Erro ao validar token inválido
assertThrows(() => {
  validateToken('invalid-token', 'test-secret');
}, 'Deve lançar erro ao validar token inválido');

// Teste 9: Erro ao validar token vazio
assertThrows(() => {
  validateToken('', 'test-secret');
}, 'Deve lançar erro ao validar token vazio');

// Teste 10: Erro ao validar token expirado
try {
  const token = generateToken({ userId: '123' }, 'test-secret', { expiresIn: '0s' });
  // Aguardar um pouco para garantir que o token expire
  setTimeout(() => {
    assertThrows(() => {
      validateToken(token, 'test-secret');
    }, 'Deve lançar erro ao validar token expirado');
  }, 100);
} catch (error) {
  assert(false, 'Erro inesperado no teste de token expirado');
}

console.log('\n=== Testes de Validação de Role ===\n');

// Teste 11: Validação de role única válida
try {
  const decoded = { userId: '123', role: 'admin' };
  assert(validateRole(decoded, 'admin') === true, 'Deve validar role única válida');
} catch (error) {
  assert(false, 'Deve validar role única válida');
}

// Teste 12: Validação de role única inválida
try {
  const decoded = { userId: '123', role: 'user' };
  assert(validateRole(decoded, 'admin') === false, 'Deve rejeitar role única inválida');
} catch (error) {
  assert(false, 'Deve rejeitar role única inválida');
}

// Teste 13: Validação de múltiplas roles (array de roles no token)
try {
  const decoded = { userId: '123', role: ['user', 'admin'] };
  assert(validateRole(decoded, 'admin') === true, 'Deve validar role em array de roles');
} catch (error) {
  assert(false, 'Deve validar role em array de roles');
}

// Teste 14: Validação com array de roles requeridas
try {
  const decoded = { userId: '123', role: 'admin' };
  assert(validateRole(decoded, ['admin', 'superadmin']) === true, 'Deve validar com array de roles requeridas');
} catch (error) {
  assert(false, 'Deve validar com array de roles requeridas');
}

// Teste 15: Validação de token sem role
try {
  const decoded = { userId: '123' };
  assert(validateRole(decoded, 'admin') === false, 'Deve retornar false para token sem role');
} catch (error) {
  assert(false, 'Deve retornar false para token sem role');
}

// Teste 16: Erro ao validar role com token inválido
assertThrows(() => {
  validateRole(null, 'admin');
}, 'Deve lançar erro ao validar role com token inválido');

console.log('\n=== Testes de Validação Combinada (Token + Role) ===\n');

// Teste 17: Validação combinada com sucesso
try {
  const token = generateToken({ userId: '123', role: 'admin' }, 'test-secret');
  const result = validateTokenAndRole(token, 'test-secret', 'admin');
  assert(result.valid === true && result.hasRole === true, 'Deve validar token e role com sucesso');
} catch (error) {
  assert(false, 'Deve validar token e role com sucesso');
}

// Teste 18: Validação combinada - token válido mas role incorreta
try {
  const token = generateToken({ userId: '123', role: 'user' }, 'test-secret');
  const result = validateTokenAndRole(token, 'test-secret', 'admin');
  assert(result.valid === true && result.hasRole === false, 'Deve detectar role incorreta mesmo com token válido');
} catch (error) {
  assert(false, 'Deve detectar role incorreta mesmo com token válido');
}

// Teste 19: Validação combinada - token inválido
try {
  const result = validateTokenAndRole('invalid-token', 'test-secret', 'admin');
  assert(result.valid === false && result.hasRole === false, 'Deve detectar token inválido');
} catch (error) {
  assert(false, 'Deve detectar token inválido');
}

// Teste 20: Validação combinada com múltiplas roles
try {
  const token = generateToken({ userId: '123', role: 'user' }, 'test-secret');
  const result = validateTokenAndRole(token, 'test-secret', ['admin', 'user']);
  assert(result.valid === true && result.hasRole === true, 'Deve validar com múltiplas roles');
} catch (error) {
  assert(false, 'Deve validar com múltiplas roles');
}

// Aguarda testes assíncronos e imprime resultado final
setTimeout(() => {
  console.log(`\n${'='.repeat(50)}`);
  console.log(`\nResultado dos Testes:`);
  console.log(`${colors.green}Passou: ${testsPassed}${colors.reset}`);
  console.log(`${colors.red}Falhou: ${testsFailed}${colors.reset}`);
  console.log(`Total: ${testsPassed + testsFailed}\n`);

  if (testsFailed > 0) {
    process.exit(1);
  } else {
    console.log(`${colors.green}Todos os testes passaram!${colors.reset}\n`);
    process.exit(0);
  }
}, 200);
