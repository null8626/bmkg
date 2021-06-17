"""
Unofficial BMKG API wrapper for python.
Original main website: https://www.bmkg.go.id/
"""

from .bmkg import BMKG, version
__version__ = version
__all__ = ('BMKG', 'version')