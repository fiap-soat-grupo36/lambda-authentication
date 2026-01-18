from src.exception.validacoes_exception import CPFInvalidoError


class ValidadorCPFService:
    @staticmethod
    def _limpar_cpf(cpf: str) -> str:
        return ''.join(ch for ch in cpf if ch.isdigit())

    @staticmethod
    def _format_cpf(cpf: str) -> str:
        """
        Normaliza o CPF para o formato '123.456.789-09'.
        Se não houver 11 dígitos, retorna o valor original.
        """
        if cpf is None:
            return cpf
        digits = ''.join(ch for ch in cpf if ch.isdigit())
        if len(digits) != 11:
            return cpf
        return f"{digits[0:3]}.{digits[3:6]}.{digits[6:9]}-{digits[9:11]}"


    @staticmethod
    def validar_cpf(self, cpf: str) -> str:
        cpf = self._limpar_cpf(cpf)

        if len(cpf) != 11:
            raise CPFInvalidoError('CPF deve conter 11 dígitos.')

        if cpf == cpf[0] * 11:
            raise CPFInvalidoError('CPF inválido: sequência repetida.')

        if not self._valida_digitos(cpf):
            raise CPFInvalidoError(
                'CPF inválido: dígitos verificadores incorretos.'
            )

        return self._format_cpf(cpf)

    @staticmethod
    def _valida_digitos(cpf: str) -> bool:
        def calcula_digito(cpf_slice, weight_start):
            total = 0
            weight = weight_start

            for char in cpf_slice:
                total += int(char) * weight
                weight -= 1

            remainder = total % 11
            return '0' if remainder < 2 else str(11 - remainder)

        digito_verificador_1 = calcula_digito(cpf[:9], 10)
        digito_verificador_2 = calcula_digito(cpf[:10], 11)

        return (
            cpf[-2] == digito_verificador_1 and cpf[-1] == digito_verificador_2
        )
