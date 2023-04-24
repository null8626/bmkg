from inspect import isgenerator
from sys import stdout
import asyncio
import bmkg
import os

INDENTATION = 2

is_local = lambda data: getattr(data, '__module__', '').startswith('bmkg') # yapf: disable

def _test(obj, indent_level=0):
  for name in dir(obj.__class__):
    attr = getattr(obj.__class__, name)
    
    if isinstance(attr, property) and attr.fget:
      stdout.write(f'{" " * indent_level}{obj.__class__.__name__}#{name}')
      
      data = getattr(obj, name)
      
      if isgenerator(data):
        stdout.write('[0] -> ')
        
        for i, each in enumerate(data):
          if i > 0:
            stdout.write(
              f'{" " * indent_level}{obj.__class__.__name__}#{name}[{i}] -> '
            )
          
          print(repr(each))
          _test(each, indent_level + INDENTATION)
        
        continue
      
      print(f' -> {data!r}')
      
      if is_local(data):
        _test(data, indent_level + INDENTATION)

def test(obj):
  print(f'{obj!r} -> ')
  _test(obj, INDENTATION)

def test_iter(obj):
  for i, each in enumerate(obj):
    print(f'[{i}] -> {each!r}')
    _test(each, INDENTATION)

async def getweather():
  async with bmkg.Client(unit=bmkg.IMPERIAL) as client:
    print('client.get_forecast:')
    test(await client.get_forecast())
    
    print('\nclient.get_latest_earthquake:')
    test(await client.get_latest_earthquake())
    
    print('\nclient.get_recent_earthquakes:')
    test_iter(await client.get_recent_earthquakes())
    
    print('\nclient.get_felt_earthquakes:')
    test_iter(await client.get_felt_earthquakes())

if __name__ == '__main__':
  if os.name == 'nt':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
  
  asyncio.run(getweather())
