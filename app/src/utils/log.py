import logging

from ddtrace import tracer
from pythonjsonlogger import jsonlogger


class DatadogLogConfig:
    """Configuração de logs com integração Datadog e trace_id."""

    def __init__(self, service_name: str, environment: str):
        self.service_name = service_name
        self.environment = environment
        self.logger = None

    def configure(self) -> logging.Logger:
        """Configura e retorna o logger com Datadog."""
        self.logger = logging.getLogger(self.service_name)
        self.logger.setLevel(logging.DEBUG)

        # Handler JSON para Datadog
        handler = logging.StreamHandler()
        formatter = DatadogJsonFormatter(self.service_name, self.environment)
        handler.setFormatter(formatter)

        if not self.logger.handlers:
            self.logger.addHandler(handler)

        return self.logger

    def get_logger(self) -> logging.Logger:
        """Retorna o logger configurado."""
        if self.logger is None:
            self.configure()
        return self.logger


class DatadogJsonFormatter(jsonlogger.JsonFormatter):
    """Formatter customizado para incluir trace_id do Datadog."""

    def __init__(self, service_name: str, environment: str):
        super().__init__()
        self.service_name = service_name
        self.environment = environment

    def add_fields(self, log_record, record, message_dict):
        super().add_fields(log_record, record, message_dict)

        # Adiciona informações Datadog
        log_record['service'] = self.service_name
        log_record['environment'] = self.environment

        # Adiciona trace_id do contexto
        span = tracer.current_span()
        if span:
            log_record['dd.trace_id'] = span.trace_id
            log_record['dd.span_id'] = span.span_id

        log_record['level'] = record.levelname
