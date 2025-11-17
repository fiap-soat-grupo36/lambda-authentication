const { generateToken, validateToken, validateRole, validateTokenAndRole } = require('./auth');

/**
 * AWS Lambda Handler para autenticação de microserviços
 * 
 * Operações suportadas:
 * - generate: Gera um novo token JWT
 * - validate: Valida um token JWT
 * - validateRole: Valida token e verifica role de acesso
 */
exports.handler = async (event) => {
  try {
    // Obtém a secret do ambiente (deve ser configurada na Lambda)
    const secret = process.env.JWT_SECRET || 'default-secret-change-in-production';
    
    // Parse do body se for string
    const body = typeof event.body === 'string' ? JSON.parse(event.body) : event.body || {};
    const operation = body.operation || event.operation;

    switch (operation) {
      case 'generate':
        return handleGenerate(body, secret);
      
      case 'validate':
        return handleValidate(body, secret);
      
      case 'validateRole':
        return handleValidateRole(body, secret);
      
      default:
        return createResponse(400, {
          error: 'Operação inválida. Use: generate, validate, ou validateRole'
        });
    }
  } catch (error) {
    console.error('Erro no handler:', error);
    return createResponse(500, {
      error: 'Erro interno do servidor',
      message: error.message
    });
  }
};

/**
 * Handler para geração de token
 */
function handleGenerate(body, secret) {
  try {
    const { payload, expiresIn } = body;
    
    if (!payload) {
      return createResponse(400, {
        error: 'Payload é obrigatório para gerar token'
      });
    }

    const options = expiresIn ? { expiresIn } : {};
    const token = generateToken(payload, secret, options);

    return createResponse(200, {
      success: true,
      token
    });
  } catch (error) {
    return createResponse(400, {
      error: error.message
    });
  }
}

/**
 * Handler para validação de token
 */
function handleValidate(body, secret) {
  try {
    const { token } = body;
    
    if (!token) {
      return createResponse(400, {
        error: 'Token é obrigatório para validação'
      });
    }

    const decoded = validateToken(token, secret);

    return createResponse(200, {
      success: true,
      valid: true,
      decoded
    });
  } catch (error) {
    return createResponse(401, {
      success: false,
      valid: false,
      error: error.message
    });
  }
}

/**
 * Handler para validação de token e role
 */
function handleValidateRole(body, secret) {
  try {
    const { token, requiredRoles } = body;
    
    if (!token) {
      return createResponse(400, {
        error: 'Token é obrigatório para validação'
      });
    }

    if (!requiredRoles) {
      return createResponse(400, {
        error: 'RequiredRoles é obrigatório para validação de role'
      });
    }

    const result = validateTokenAndRole(token, secret, requiredRoles);

    if (!result.valid) {
      return createResponse(401, {
        success: false,
        valid: false,
        error: result.error
      });
    }

    if (!result.hasRole) {
      return createResponse(403, {
        success: false,
        valid: true,
        hasRole: false,
        error: 'Usuário não possui a role necessária para acessar este recurso'
      });
    }

    return createResponse(200, {
      success: true,
      valid: true,
      hasRole: true,
      decoded: result.decoded
    });
  } catch (error) {
    return createResponse(400, {
      error: error.message
    });
  }
}

/**
 * Cria resposta padronizada para Lambda
 */
function createResponse(statusCode, body) {
  return {
    statusCode,
    headers: {
      'Content-Type': 'application/json',
      'Access-Control-Allow-Origin': '*'
    },
    body: JSON.stringify(body)
  };
}
