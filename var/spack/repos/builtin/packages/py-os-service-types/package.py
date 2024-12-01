# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyOsServiceTypes(PythonPackage):
    """Python library for consuming OpenStack sevice-types-authority data"""

    homepage = "https://docs.openstack.org/os-service-types/"
    pypi = "os-service-types/os-service-types-1.7.0.tar.gz"

    maintainers("haampie")

    version("1.7.0", sha256="31800299a82239363995b91f1ebf9106ac7758542a1e4ef6dc737a5932878c6c")

    depends_on("python@2.7:2.8,3.5:", type=("build", "run"))
    depends_on("py-pbr@2.0.0:2.0,2.1.1:", type="build")
    depends_on("py-setuptools", type="build")
