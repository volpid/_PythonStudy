
#include <Python.h>

static PyObject* ErrorObject;
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
        PyErr_SetString(PyExc_ZeroDivisionError, "devisor is zero");
        return NULL;
    }

    return Py_BuildValue("i", quotient);
}

static PyMethodDef SpamMethod[] =
{
    {"strlen", spam_strlen, METH_VARARGS, "count a string length."},
    {"division", spam_division, METH_VARARGS, "division function"},
    {NULL, NULL, 0, NULL},
};

void initspam(void)
{
    PyObject* m;
    m = Py_InitModule("spam", SpamMethod);
    ErrorObject = Py_BuildValue("s", "error");
}
