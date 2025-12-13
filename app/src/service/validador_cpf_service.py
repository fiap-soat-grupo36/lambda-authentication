from distutils.command.clean import clean

from src.exception.validacoes_exception import CPFInvalidoError


class ValidadorCPFService:

    def clean(cpf: str) -> str:

        return ''.join(ch for ch in cpf if ch.isdigit())

    def validar_cpf(cpf: str) -> str:
        cpf = clean(cpf)

        if len(cpf) != 11:
            raise CPFInvalidoError("CPF deve conter 11 dígitos.")

        if cpf == cpf[0] * 11:
            raise CPFInvalidoError("CPF inválido: sequência repetida.")

        if not ValidadorCPFService._valida_digitos(cpf):
            raise CPFInvalidoError("CPF inválido: dígitos verificadores incorretos.")

        return cpf

    def _valida_digitos(cpf: str) -> bool:

        def calcula_digito(cpf_slice, weight_start):
            total = 0
            weight = weight_start

            for char in cpf_slice:
                total += int(char) * weight
                weight -= 1

            remainder = total % 11
            return "0" if remainder < 2 else str(11 - remainder)

        digito_verificador_1 = calcula_digito(cpf[:9], 10)
        digito_verificador_2 = calcula_digito(cpf[:10], 11)

        return cpf[-2] == digito_verificador_1 and cpf[-1] == digito_verificador_2
