# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *
from spack.pkg.builtin.boost import Boost


class PyQuast(PythonPackage):
    """Quality Assessment Tool for Genome Assemblies"""

    homepage = "https://cab.spbu.ru/software/quast"
    pypi = "quast/quast-5.2.0.tar.gz"

    license("GPL-2.0-only")

    version("5.2.0", sha256="23649fbd93253c6da982c0b67d719f9262461deecdc6dffbd690b75dfd790ad7")
    version("5.0.2", sha256="cdb8f83e20cc38f218ff7172b454280fcb1c7e2dff74e1f8618cacc53d46b48e")
    version("5.0.1", sha256="b1e4443b6598b01faaefddfc0f06fb270414ed4bdaffd0ad9aa420bc0d07d8ad")
    version("5.0.0", sha256="46bba247c7f92c2ccaca8c0abeab2a8d40a257a0cbe2fa0a4ffa981ca0267526")
    version("4.6.3", sha256="f9267e5deadf20cfe67731a42e775e7ef1d0850927a2a76c4b3d49bc77b1fab5")
    version("4.6.1", sha256="7ace5bebebe9d2a70ad45e5339f998bd651c1c6b9025f7a3b51f44c87ea5bae0")
    version("4.6.0", sha256="3a7ee7a2abfeb0541b299b67f263ba95f9743f8809ddf5dfaca9c3c8f9b6a215")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("boost@1.56.0")

    # TODO: replace this with an explicit list of components of Boost,
    # for instance depends_on('boost +filesystem')
    # See https://github.com/spack/spack/pull/22303 for reference
    depends_on(Boost.with_default_variants)
    depends_on("perl@5.6.0:", type=("build", "run"))
    depends_on("python@2.5:,3.3:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-matplotlib", type=("build", "run"))
    depends_on("py-joblib", type=("build", "run"))
    depends_on("py-simplejson", type=("build", "run"))
    depends_on("java", type=("build", "run"))
    depends_on("perl-time-hires", type=("build", "run"))
    depends_on("gnuplot", type=("build", "run"))
    depends_on("mummer", type=("build", "run"))
    depends_on("bedtools2", type=("build", "run"))
    depends_on("bwa", type=("build", "run"))
    depends_on("glimmer", type=("build", "run"))
