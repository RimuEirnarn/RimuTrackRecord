# from sys import path
# from pathlib import Path
# path.insert(0, Path(__file__).parent.parent)
# print(path)

from system.configstore import config

config.data = 'value'
print(config.data)
print(config.nonexistent)
print(config['nonexistent'])