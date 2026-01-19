import pytest

from src.exception.validacoes_exception import CPFInvalidoError
from src.service.validador_cpf_service import ValidadorCPFService


class TestValidadorCPFService:
    def test_validar_cpf_sucesso_limpo(self):
        cpf_valido = '529.982.247-25'
        resultado = ValidadorCPFService.validar_cpf(cpf_valido)
        assert resultado == cpf_valido

    def test_validar_cpf_sucesso_com_formatacao(self):
        cpf_input = '529.982.247-25'
        cpf_esperado = '529.982.247-25'
        resultado = ValidadorCPFService.validar_cpf(cpf_input)
        assert resultado == cpf_esperado

    def test_deve_falhar_tamanho_incorreto(self):
        with pytest.raises(CPFInvalidoError) as exc:
            ValidadorCPFService.validar_cpf('12345')
        assert '11 dígitos' in str(exc.value)

    def test_deve_falhar_numeros_repetidos(self):
        with pytest.raises(CPFInvalidoError) as exc:
            ValidadorCPFService.validar_cpf('11111111111')
        assert 'sequência repetida' in str(exc.value)

    def test_deve_falhar_digito_verificador(self):
        cpf_falso = '52998224799'
        with pytest.raises(CPFInvalidoError) as exc:
            ValidadorCPFService.validar_cpf(cpf_falso)
        assert 'dígitos verificadores incorretos' in str(exc.value)
