
#include <Python.h>

#include <iostream>
using namespace std;

int main(int argc, char** argv)
{
    PyObject* pName;
    PyObject* pModule;
    PyObject* pDict;
    PyObject* pFunc;
    PyObject* pArgs;
    PyObject* pValue;

    char* ARGS[] = 
    {
        argv[0],
        "test_embedding_python",
        "multiply",
        "3",
        "20"
    };
    
    int ARGC = sizeof(ARGS) / sizeof(char*);
    if (ARGC < 3)
    {
        fprintf(stderr, "Usage : call pythonfile funcname [args]\n");
        return 1;
    }

    Py_Initialize();

    PyRun_SimpleString("import sys\n"
        "import os\n"
        "from pprint import pprint\n"
        "abspath = os.path.abspath('./') + '\\BindingCModule'\n"
        "sys.path.insert(0, abspath)\n"
        "pprint(sys.path)\n"
        "print()\n");  

    pName = PyUnicode_DecodeFSDefault(ARGS[1]);

    pModule = PyImport_Import(pName);
    Py_DECREF(pName);

    if (pModule != nullptr)
    {
        pFunc = PyObject_GetAttrString(pModule, ARGS[2]);

        if (pFunc && PyCallable_Check(pFunc))
        {
            pArgs = PyTuple_New(ARGC - 3);
            for (int idx = 0; idx < ARGC - 3; ++idx)
            {
                pValue = PyLong_FromLong(atoi(ARGS[idx + 3]));
                if (pValue == nullptr)
                {
                    Py_DECREF(pArgs);
                    Py_DECREF(pModule);
                    fprintf(stderr, "Cannot convert argument\n");
                    return 1;
                }

                PyTuple_SetItem(pArgs, idx, pValue);
            }

            pValue = PyObject_CallObject(pFunc, pArgs);
            Py_DECREF(pArgs);

            if (pValue != nullptr)
            {
                printf("result of call : %ld\n", PyLong_AsLong(pValue));
                Py_DECREF(pValue);
            }
            else
            {
                Py_DECREF(pFunc);
                Py_DECREF(pModule);

                PyErr_Print();
                fprintf(stderr, "call failed\n");
                return 1;
            }
        }
        else if (PyErr_Occurred())
        {
            PyErr_Print();
            fprintf(stderr, "cannot find function : %s\n", ARGS[2]);
        }

        Py_XDECREF(pFunc);
        Py_DECREF(pModule);
    }
    else
    {
        PyErr_Print();
        fprintf(stderr, "fail to load : %s\n", ARGS[1]);
        return 1;
    }

    Py_Finalize();
    return 0;
}