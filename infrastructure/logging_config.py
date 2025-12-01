import logging
import sys
from pythonjsonlogger import jsonlogger
import os


def setup_logging():
    """Configure le logging structuré pour l'application."""

    # Récupérer le niveau de log depuis les variables d'environnement
    log_level = os.getenv("LOG_LEVEL", "INFO").upper()

    # Créer le logger principal
    logger = logging.getLogger()
    logger.setLevel(getattr(logging, log_level))

    # Supprimer les handlers existants
    logger.handlers = []

    # Créer le handler pour stdout
    handler = logging.StreamHandler(sys.stdout)

    # Format JSON pour la production
    if os.getenv("ENVIRONMENT") == "production":
        formatter = jsonlogger.JsonFormatter(
            '%(asctime)s %(name)s %(levelname)s %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
    else:
        # Format lisible pour le développement
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

    handler.setFormatter(formatter)
    logger.addHandler(handler)

    # Désactiver les logs trop verbeux de certaines bibliothèques
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)

    return logger


# Logger pour l'application
app_logger = setup_logging()
