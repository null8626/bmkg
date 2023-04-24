"""
The MIT License (MIT)
Copyright (c) 2021-2023 null (https://github.com/null8626)
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the 'Software'), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED 'AS IS', WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from enum import auto, Enum

from .constants import METRIC, VALID_UNITS

class BasicEnum(Enum):
  __slots__ = ()
  
  def __repr__(self) -> str:
    """:class:`str`: The string representation of this object."""
    
    return f'{self.__class__.__name__}.{self.name}'
  
  def __str__(self) -> str:
    """:class:`str`: The stylized name for this :class:`Enum`."""
    
    return self.name.replace('_', ' ').title()

class CustomizableUnit:
  __slots__ = ('__unit', 'english')
  
  def __init__(self, unit: auto, english: bool):
    self.unit = unit
    self.english = english
  
  @property
  def unit(self) -> auto:
    """:class:`auto`: The measuring unit used to display information in this object."""
    
    return self.__unit
  
  @unit.setter
  def unit(self, to: auto):
    """
    Sets the default measuring unit used to display information in this object.
    
    Parameters
    ----------
    to: :class:`auto`
      The new default measuring unit to be used to display information in this object. Must be either :attr:`METRIC` or :attr:`IMPERIAL`.
    Raises
    ------
    Error
      If the ``to`` argument is not either :attr:`METRIC` or :attr:`IMPERIAL`.
    """
    
    if to not in VALID_UNITS:
      raise Error('Invalid measuring unit specified!')
    
    self.__unit = to
