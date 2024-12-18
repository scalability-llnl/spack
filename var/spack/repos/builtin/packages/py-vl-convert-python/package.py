# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyVlConvertPython(PythonPackage):
    """Convert Vega-Lite chart specifications to SVG, PNG, PDF, or Vega"""

    homepage = "https://github.com/vega/vl-convert"
    pypi = "vl_convert_python/vl_convert_python-1.4.0.tar.gz"

    version("1.4.0", sha256="264d6f2338c7d3474e60c6907cca016b880b0c1c9be302bb84abc6690188a7e9")

    version(
        "1.3.0",
        sha256="de1462151dfbba7b2a17881dac1d2269662012c252f1e9d1537a4daed5e36067",
        deprecated=True,
    )
    version(
        "0.13.1",
        sha256="d70a608257dd6b5b782d96cccebfe7289992e522e47a8bebb7d928253ca8b396",
        deprecated=True,
    )

    depends_on("python@3.7:", type=("build", "run"))

    # TODO: This package currently requires internet access to install.
    depends_on("py-maturin@1.1:1", type="build")

    depends_on("cmake", type="build")  # some rust dependencies need this
    depends_on("protobuf", type="build")  # rust dependency prost need this
