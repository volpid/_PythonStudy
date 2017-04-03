
#include <Python.h>

static PyObject* ErrorObject;
static PyObject* write_log(PyObject* self, PyObject* args)
{
    char* msg;
    FILE* fp;

    if(!PyArg_ParseTuple(args, "s", &msg))    
    {
        return NULL;
    }

    fp = fopen("./_Output/pylog.txt", "wt+");
    fprintf(fp, msg);
    fclose(fp);

    return Py_BuildValue("i", 0);
}

static struct PyMethodDef myLibMethod[] = 
{
    {"wlog", write_log, METH_VARARGS, NULL},
    {NULL, NULL},
};

static struct PyModuleDef myLibmodule =
{
    PyModuleDef_HEAD_INIT,
    "myLib",
    NULL,
    -1,
    myLibMethod
};

PyMODINIT_FUNC PyInit_myLib(void)
{
    PyObject* m;

    m = PyModule_Create(&myLibmodule);
    if (m == NULL)
    {
        return NULL;
    }

    ErrorObject = PyErr_NewException("mylib.error", NULL, NULL);
    Py_INCREF(ErrorObject);
    PyModule_AddObject(m, "error", ErrorObject);

    return m;
}