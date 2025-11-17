const jwt = require('jsonwebtoken');

/**
 * Gera um token JWT para autenticação de microserviços
 * @param {Object} payload - Dados a serem incluídos no token (userId, role, etc)
 * @param {string} secret - Chave secreta para assinar o token
 * @param {Object} options - Opções adicionais (expiresIn, etc)
 * @returns {string} Token JWT gerado
 */
function generateToken(payload, secret, options = {}) {
  if (!payload || typeof payload !== 'object') {
    throw new Error('Payload deve ser um objeto válido');
  }
  
  if (!secret || typeof secret !== 'string') {
    throw new Error('Secret deve ser uma string válida');
  }

  const defaultOptions = {
    expiresIn: '1h',
    ...options
  };

  return jwt.sign(payload, secret, defaultOptions);
}

/**
 * Valida a autenticidade de um token JWT
 * @param {string} token - Token JWT a ser validado
 * @param {string} secret - Chave secreta usada para verificar o token
 * @returns {Object} Payload decodificado do token
 * @throws {Error} Se o token for inválido ou expirado
 */
function validateToken(token, secret) {
  if (!token || typeof token !== 'string') {
    throw new Error('Token deve ser uma string válida');
  }
  
  if (!secret || typeof secret !== 'string') {
    throw new Error('Secret deve ser uma string válida');
  }

  try {
    return jwt.verify(token, secret);
  } catch (error) {
    if (error.name === 'TokenExpiredError') {
      throw new Error('Token expirado');
    } else if (error.name === 'JsonWebTokenError') {
      throw new Error('Token inválido');
    }
    throw error;
  }
}

/**
 * Valida se o usuário tem a role necessária para acessar um recurso
 * @param {Object} decodedToken - Token decodificado contendo informações do usuário
 * @param {string|string[]} requiredRoles - Role(s) necessária(s) para acesso
 * @returns {boolean} true se o usuário tem a role necessária, false caso contrário
 */
function validateRole(decodedToken, requiredRoles) {
  if (!decodedToken || typeof decodedToken !== 'object') {
    throw new Error('Token decodificado deve ser um objeto válido');
  }

  if (!decodedToken.role) {
    return false;
  }

  const roles = Array.isArray(requiredRoles) ? requiredRoles : [requiredRoles];
  
  if (Array.isArray(decodedToken.role)) {
    return decodedToken.role.some(role => roles.includes(role));
  }
  
  return roles.includes(decodedToken.role);
}

/**
 * Valida token e role em uma única operação
 * @param {string} token - Token JWT a ser validado
 * @param {string} secret - Chave secreta usada para verificar o token
 * @param {string|string[]} requiredRoles - Role(s) necessária(s) para acesso
 * @returns {Object} Objeto com resultado da validação
 */
function validateTokenAndRole(token, secret, requiredRoles) {
  try {
    const decoded = validateToken(token, secret);
    const hasRole = validateRole(decoded, requiredRoles);
    
    return {
      valid: true,
      hasRole,
      decoded
    };
  } catch (error) {
    return {
      valid: false,
      hasRole: false,
      error: error.message
    };
  }
}

module.exports = {
  generateToken,
  validateToken,
  validateRole,
  validateTokenAndRole
};
