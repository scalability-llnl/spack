# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyCythonBbox(PythonPackage):
    """cython_bbox is widely used in object detection tasks. To my
    best knowledge, it was first implemented in Faster-RCNN. Since
    then, almost all object detection projects use the source code
    directly. In order to use it in standalone code snippets or small projects,
    I make it a pypi module. The cython_bbox.pyx is totally borrowed
    from Faster-RCNN. Thanks RBG!"""

    homepage = "https://github.com/samson-wang/cython_bbox.git"
    pypi = "cython-bbox/cython_bbox-0.1.3.tar.gz"

    version("0.1.3", sha256="82e2d887534ecc10d3507489a05b11259f3baacd29eee37e6d8c97e1ffb16554")

    depends_on("c", type="build")  # generated
    depends_on("py-setuptools", type="build")
    depends_on("py-cython", type="build")
    depends_on("py-numpy", type=("build", "run"))
