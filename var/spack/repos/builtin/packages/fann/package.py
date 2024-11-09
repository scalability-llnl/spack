# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Fann(CMakePackage):
    """
    Fast Artificial Neural Network Library is a free open source neural network
    library, which implements multilayer artificial neural networks in C with
    support for both fully connected and sparsely connected networks.
    Cross-platform execution in both fixed and floating point are supported. It
    includes a framework for easy handling of training data sets. It is easy to
    use, versatile, well documented, and fast. Bindings to more than 20
    programming languages are available. An easy to read introduction article
    and a reference manual accompanies the library with examples and
    recommendations on how to use the library. Several graphical user
    interfaces are also available for the library.
    """

    homepage = "https://leenissen.dk/fann/wp/"
    url = "https://github.com/libfann/fann/archive/2.2.0.tar.gz"

    license("LGPL-2.0-or-later")

    version("2.2.0", sha256="f31c92c1589996f97d855939b37293478ac03d24b4e1c08ff21e0bd093449c3c")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
