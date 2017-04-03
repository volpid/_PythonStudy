
#include <Python.h>

static PyObject* SpamError;

static PyObject* spam_strlen(PyObject* self, PyObject* args)
{
    char* str;
    int len;

    if (!PyArg_ParseTuple(args, "s", &str))
    {
        return NULL;
    }

    len = strlen(str);

    return Py_BuildValue("i", len);
}

static PyObject* spam_division(PyObject* self, PyObject* args)
{
    int quotient = 0;
    int dividend = 0;
    int divisor = 0;

    if (!PyArg_ParseTuple(args, "ii", &dividend, &divisor))
    {
        return NULL;
    }

    if (divisor != 0)
    {
        quotient = dividend / divisor;
    }
    else
    {
        PyErr_SetString(SpamError, "devisor is zero");
        return NULL;
    }

    return Py_BuildValue("i", quotient);
}

static PyMethodDef SpamMethods[] =
{
    {"strlen", spam_strlen, METH_VARARGS, "count a string length."},
    {"division", spam_division, METH_VARARGS, "division function"},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef spammodule =
{
    PyModuleDef_HEAD_INIT,
    "spam",
    NULL,
    -1,
    SpamMethods
};

PyMODINIT_FUNC PyInit_spam(void)
{
    PyObject* m;

    m = PyModule_Create(&spammodule);
    if (m == NULL)
    {
        return NULL;
    }

    SpamError = PyErr_NewException("spam.error", NULL, NULL);
    Py_INCREF(SpamError);
    PyModule_AddObject(m, "error", SpamError);

    return m;
}