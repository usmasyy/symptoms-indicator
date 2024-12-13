from .disease_analyzer import DiseaseAnalyzer

__version__ = '1.0.0'
__author__ = 'Disease Support System Team'
__description__ = 'A bioinformatics-based disease diagnosis system using global sequence alignment'

# Export the main analyzer class
__all__ = ['DiseaseAnalyzer']

# Configure logging
import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Package initialization message
logger = logging.getLogger(__name__)
logger.info(f"Initializing Disease Support System v{__version__}")
