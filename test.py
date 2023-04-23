from _collections import _tuplegetter
from inspect import isgenerator
from sys import stdout
import traceback
import asyncio
import bmkg
import os

INDENTATION = 2

def _test_properties(obj, indent_level=0, in_recursion=False):
  exists = not in_recursion
  
  for name in dir(obj.__class__):
    attr = getattr(obj.__class__, name)
    
    if (isinstance(attr, property) and
        attr.fget) or isinstance(attr, _tuplegetter):
      if not exists:
        print()
        exists = True
      
      stdout.write(f'{" " * indent_level}{obj.__class__.__name__}#{name}')
      
      data = getattr(obj, name) if isinstance(attr,
                                              _tuplegetter) else attr.fget(obj)
      
      if isgenerator(data):
        stdout.write('[0] -> ')
        
        for i, each in enumerate(data):
          if i > 0:
            stdout.write(
              f'{" " * indent_level}{obj.__class__.__name__}#{name}[{i}] -> '
            )
          
          _test_properties(each, indent_level + INDENTATION, True)
        
        continue
      
      stdout.write(' -> ')
      
      if getattr(data, '__module__', '').startswith('python_weather'):
        _test_properties(data, indent_level + INDENTATION, True)
      else:
        print(repr(data))
  
  if not exists:
    print(repr(obj))

def test(obj):
  try:
    if isgenerator(obj):
      for i, each in enumerate(obj):
        print(f'{each.__class__.__name__}[{i}] -> ')
        _test_properties(each, INDENTATION)
    else:
      _test_properties(obj)
  except:
    print(f'\n\n{traceback.format_exc().rstrip()}')
    exit(1)

async def getweather():
  async with bmkg.Client(unit=bmkg.IMPERIAL) as client:
    print('client.get_forecast:')
    test(await client.get_forecast())
    
    print('\nclient.get_latest_earthquake:')
    test(await client.get_latest_earthquake())
    
    print('\nclient.get_recent_earthquakes:')
    test(await client.get_recent_earthquakes())
    
    print('\nclient.get_felt_earthquakes:')
    test(await client.get_felt_earthquakes())

if __name__ == '__main__':
  if os.name == 'nt':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
  
  asyncio.run(getweather())
