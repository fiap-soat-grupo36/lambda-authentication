import json
from datetime import datetime, timedelta
from typing import Dict, Any

import boto3
import jwt


class GeradorTokenJWT:
    _segredo_cache: str | None = None

    @staticmethod
    def _carregar_segredo(secret_name: str, region: str) -> str:

        if GeradorTokenJWT._segredo_cache:
            return GeradorTokenJWT._segredo_cache

        cliente = boto3.client("secretsmanager", region_name=region)
        resposta = cliente.get_secret_value(SecretId=secret_name)

        dados = json.loads(resposta["SecretString"])
        segredo = dados.get("jwt_secret")

        if not segredo:
            raise RuntimeError("Chave 'jwt_secret' não encontrada no Secret.")

        GeradorTokenJWT._segredo_cache = segredo
        return segredo

    @staticmethod
    def gerar_token(
            cpf: str,
            cliente_id: str,
            nome: str,
            ativo: bool,
            secret_name: str,
            region: str,
            expira_em_minutos: int = 30
    ) -> str:

        segredo = GeradorTokenJWT._carregar_segredo(secret_name, region)

        agora = datetime.utcnow()
        expira = agora + timedelta(minutes=expira_em_minutos)

        payload = {
            "cpf": cpf,
            "cliente_id": cliente_id,
            "nome": nome,
            "ativo": ativo,
            "iat": int(agora.timestamp()),
            "exp": int(expira.timestamp())
        }

        token = jwt.encode(payload, segredo, algorithm="HS256")

        if isinstance(token, bytes):
            token = token.decode("utf-8")

        return token

    @staticmethod
    def validar_token(
            token: str,
            secret_name: str,
            region: str,
            algoritmo: str = "HS256"
    ) -> Dict[str, Any]:

        segredo = GeradorTokenJWT._carregar_segredo(secret_name, region)
        payload = jwt.decode(token, segredo, algorithms=[algoritmo])

        return payload
