// should sync
// -
// https://github.com/cubao/polyline-ruler/blob/master/src/pybind11_polyline_ruler.hpp
// -
// https://github.com/cubao/headers/tree/main/include/cubao/pybind11_polyline_ruler.hpp

#pragma once

#include <pybind11/eigen.h>
#include <pybind11/iostream.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/stl_bind.h>

#include "cubao_inline.hpp"
#include "cheap_ruler.hpp"

namespace cubao
{
namespace py = pybind11;
using namespace pybind11::literals;
using rvp = py::return_value_policy;

CUBAO_INLINE void bind_cheap_ruler(py::module &m)
{
    py::class_<PolylineRuler>(m, "CheapRuler", py::module_local()) //
                                                                   //
        ;
}
} // namespace cubao
