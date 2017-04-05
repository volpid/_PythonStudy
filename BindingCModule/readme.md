
cmodule 설치 
===

1. Visual studio command prompt 실행

1. python setup.py install

1. pyd가 생성 + 복사 된다.

1. \(파이썬 경로\)\\Lib\\site-packages\\

* setup.py  
아래와 같은 셋업 설정이 들어간다.
```python
    setup(name = 'myLib',
	version = '1.0',
	descriptoin = 'print log',
	ahthor = '--',
	url = '--',
	ext_modules = [Extension("myLib", ["./CModules/myLib.c"])]
	)
```

Extending and Embedding Overview
===

Extending Python and embedding Python is quite the same activity.

* from python to C

> 1. Convet data values from Python To C
> 1. Perform a funtion call to a C routine using the converted values
> 1. Convert the data values from the call from C to Python

* embedding Python

> 1. Convert data value form C to Python
> 1. Perform a function call to a Python interface routine using the convert values
> 1. Convert the data values form the call from Python To C