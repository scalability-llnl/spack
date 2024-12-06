# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class EsysParticle(CMakePackage):
    """ESyS-Particle is Open Source software for particle-based numerical
    modelling. The software implements the Discrete Element Method (DEM),
    a widely used technique for modelling processes involving large
    deformations, granular flow and/or fragmentation."""

    homepage = "https://launchpad.net/esys-particle"
    url = "https://launchpadlibrarian.net/539636757/esys-particle-3.0-alpha.tar.gz"

    maintainers("snehring")

    license("Apache-2.0")

    version("3.0-alpha", sha256="4fba856a95c93991cacb904e6a54a7ded93558f7adc8c3e6da99bc347843a434")

    depends_on("cxx", type="build")  # generated

    depends_on("mpi")
    depends_on("boost@1.71.0+python")
    depends_on("python@3.6:")
    depends_on("py-setuptools", type="build")

    @when("@3.0-alpha")
    def patch(self):
        files = find(".", "CMakeLists.txt")
        for file in files:
            filter_file("PYTHON_LIBRARIES", "Python_LIBRARIES", file, string=True)

    def setup_run_environment(self, env):
        pylibpath = join_path(
            self.prefix.lib, "python{0}".format(self.spec["python"].version.up_to(2))
        )
        env.prepend_path("PYTHONPATH", join_path(pylibpath, "dist-packages"))
