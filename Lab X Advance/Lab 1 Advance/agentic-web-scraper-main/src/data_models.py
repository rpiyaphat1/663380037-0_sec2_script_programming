# -*- coding: utf-8 -*-
# agentic-web-scraper/src/data_models.py
from dataclasses import dataclass, asdict

@dataclass
class Product:
    """Data model for a scraped product."""
    name: str
    price: str
    description: str = None
    url: str = None
    image_url: str = None

    def to_dict(self):
        return asdict(self)