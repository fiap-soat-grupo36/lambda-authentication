"""
Configuração do pytest para ajustar o PYTHONPATH.
"""
import sys
from pathlib import Path

# Adiciona o diretório app ao PYTHONPATH
app_dir = Path(__file__).parent
if str(app_dir) not in sys.path:
    sys.path.insert(0, str(app_dir))
