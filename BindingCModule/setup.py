
import sys
from distutils.core import setup, Extension

module1 = Extension('myLib', sources = ['./CModules3/myLib.c'])
module2 = Extension('spam', sources = ['./CModules3/spam_strlen.c'])
module3 = Extension('circle', sources = ['./CModules3/circle_prototype.c'])

if sys.version_info < (3,0) :
	module1 = Extension('myLib', sources = ['./CModules2/myLib.c'])
	module2 = Extension('spam', sources = ['./CModules2/spam_strlen.c'])
	module3 = Extension('circle', sources = ['./CModules2/circle_prototype.c'])

setup(name = 'mylib',
	version = '1.0',
	description = 'print log',
	ext_modules = [module1]	
)

setup(name = 'spam',
	version = '1.0',
	description = 'print strlen division',
	ext_modules = [module2]	
)

setup(name = 'circle',
	version = '1.0',
	description = 'circle object',
	ext_modules = [module3]	
)

