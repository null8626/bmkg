"""
Unofficial BMKG API wrapper for python.
Original main website: https://www.bmkg.go.id/
"""

from .bmkg import BMKG, BMKGSettings, Province
__version__ = '0.1.1'
__all__ = ('BMKG', 'version', 'BMKGSettings', 'Province')