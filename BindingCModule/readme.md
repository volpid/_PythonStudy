
cmodule 설치 
===

1. Visual studio command prompt 실행

1. python setup.py install

1. pyd가 생성 + 복사 된다.

1. \(파이썬 경로\)\\Lib\\site-packages\\

***

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