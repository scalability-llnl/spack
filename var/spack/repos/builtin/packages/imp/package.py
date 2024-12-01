# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *
from spack.pkg.builtin.boost import Boost


class Imp(CMakePackage):
    """IMP, the Integrative Modeling Platform."""

    homepage = "https://integrativemodeling.org"
    url = "https://github.com/salilab/imp/archive/2.8.0.tar.gz"

    license("LGPL-2.1-or-later")

    version("2.8.0", sha256="0b46b8988febd7cdfc5838849007f9a547493ed4b6c752fe54571467eeb1acd2")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("python@2.7:")
    depends_on("swig")
    depends_on("boost@1.40:")

    # TODO: replace this with an explicit list of components of Boost,
    # for instance depends_on('boost +filesystem')
    # See https://github.com/spack/spack/pull/22303 for reference
    depends_on(Boost.with_default_variants)
    depends_on("hdf5")
    depends_on("eigen")
