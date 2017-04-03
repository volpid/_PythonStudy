
#include "Python.h"

static PyObject* ErrorObject;
static PyObject* write_log(PyObject* self, PyObject* args)
{
    char* msg;
    FILE* fp;

    if(!PyArg_ParseTuple(args, "s", &msg))    
    {
        return NULL;
    }

    fp = fopen("./pylog.txt", "wt+");
    fprintf(fp, msg);
    fclose(fp);

    return Py_BuildValue("i", 0);
}

static struct PyMethodDef methods[] = 
{
    {"wlog", write_log, METH_VARARGS, NULL},
    {NULL, NULL},
};

void initmyLib(void)
{
    PyObject* m;
    m = Py_InitModule("myLib", methods);
    ErrorObject = Py_BuildValue("s", "error");
}