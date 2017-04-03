
#include <Python.h>
#include <structmember.h>

#define PI 3.14

typedef struct
{
    PyObject_HEAD
    PyObject* color;
    int radius;
} circle_CircleObject;

static PyObject* Circle_new(PyTypeObject* type, PyObject* args, PyObject* keywords)
{
    circle_CircleObject* self;
    self = (circle_CircleObject*) type->tp_alloc(type, 0);
    if (self != NULL)
    {
        self->color = PyUnicode_FromString("");
        if (self->color == NULL)
        {
            Py_DECREF(self);
            return NULL;
        }

        self->radius = 0;
    }

    return (PyObject*) self;
}

static void Circle_dealloc(circle_CircleObject* self)
{
    Py_XDECREF(self->color);
    Py_TYPE(self)->tp_free((PyObject*) self);
}

static int Circle_init(circle_CircleObject* self, PyObject* args, PyObject* keywords)
{
    PyObject* color = NULL;
    PyObject* temp = NULL;
    static char* keywordList[] = {"color", "radius", NULL};
    if (!PyArg_ParseTupleAndKeywords(args, keywords, "Si", keywordList, &color, &self->radius))
    {
        return -1;
    }

    if (color)
    {
        temp = self->color;
        Py_INCREF(color);
        self->color = color;
        Py_XDECREF(temp);
    }

    return 0;
}

static PyObject* Circle_color(circle_CircleObject* self)
{
    static PyObject* fmt = NULL;
    PyObject* tmp;
    PyObject* result;

    if (fmt == NULL)
    {
        fmt = PyUnicode_FromString("The circle color is %s");
        if (fmt == NULL)
        {
            return NULL;
        }
    }

    if (self->color == NULL)
    {
        PyErr_SetString(PyExc_AttributeError, "color");
        return NULL;
    }

    tmp = Py_BuildValue("S", self->color);
    if (tmp == NULL)
    {
        return NULL;
    }

    result = PyUnicode_Format(fmt, tmp);
    Py_DECREF(tmp);

    return result;
}

static PyObject* Circle_area(circle_CircleObject* self)
{
    int area_circle = 0;

    if (self->radius < 0)
    {
        PyErr_SetString(PyExc_AttributeError, "radius");
        return NULL;
    }

    area_circle = (int) (2 * PI * self->radius);
    return Py_BuildValue("i", area_circle);
}

static PyObject* Circle_add(circle_CircleObject* self, circle_CircleObject* target)
{
    self->radius += target->radius;
    return Py_BuildValue("i", self->radius);
}

static PyObject* Circle_multiply(circle_CircleObject* self, circle_CircleObject* target)
{
    PyErr_SetString(PyExc_NotImplementedError, "multiply is not implemented");
    return NULL;
}

struct PyMemberDef Circle_Members[] =
{
    {"color", T_OBJECT_EX, offsetof(circle_CircleObject, color), 0, "color of circle"},
    {"radius", T_INT, offsetof(circle_CircleObject, radius), 0, "radius of circle"},
    {NULL},
};

struct PyMethodDef Circle_Method[] = 
{
    {"color", (PyCFunction) Circle_color, METH_NOARGS, "return the color of circle"},
    {"area", (PyCFunction) Circle_area, METH_NOARGS, "area of circle"},
    {NULL, NULL},
};

static PyNumberMethods circle_Number = 
{
    (binaryfunc) Circle_add,
    (binaryfunc) 0,
    (binaryfunc) Circle_multiply,
    (binaryfunc) 0,
};

static PyTypeObject circle_CircleType = 
{
    PyObject_HEAD_INIT(NULL) 
    0,
    "circle.Circle",
    sizeof(circle_CircleObject),
    0, 
    (destructor) Circle_dealloc, 
    0, 
    0, 
    0, 
    0, 
    0,
    &circle_Number,
    0, 
    0, 
    0, 
    0, 
    0, 
    0, 
    0, 
    0, 
    Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,
    "circle objects",
    0,
    0,
    0,
    0,
    0,
    0,
    Circle_Method,
    Circle_Members,
    0,
    0,
    0,
    0,
    0,
    0,
    (initproc) Circle_init,
    0,
    Circle_new,
};

PyMODINIT_FUNC initcircle(void)
{
    PyObject* m;

    circle_CircleType.tp_new = PyType_GenericNew;
    if (PyType_Ready(&circle_CircleType) < 0)
    {
        return;
    }

    m = Py_InitModule3("circle", NULL, "Example New Type");
    if (m == NULL)
    {
        return;
    }

    Py_INCREF(&circle_CircleType);
    PyModule_AddObject(m, "Circle", (PyObject*) &circle_CircleType);
}