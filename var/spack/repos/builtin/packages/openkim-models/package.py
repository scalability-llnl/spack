# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class OpenkimModels(CMakePackage):
    """OpenKIM is an online framework for making molecular simulations
    reliable, reproducible, and portable. Computer implementations of
    inter-atomic models are archived in OpenKIM, verified for coding
    integrity, and tested by computing their predictions for a variety
    of material properties.  Models conforming to the KIM application
    programming interface (API) work seamlessly with major simulation
    codes that have adopted the KIM API standard.

    This package provides all models archived at openkim.org that are
    compatible with the kim-api package.
    """

    homepage = "https://openkim.org/"
    url = "https://s3.openkim.org/archives/collection/openkim-models-2021-01-28.txz"

    maintainers("ellio167")

    extends("kim-api")
    depends_on("kim-api@2.2.1:", when="@2021-01-28:")
    depends_on("kim-api@2.1.0:", when="@2019-07-25:")
    depends_on("kim-api@:2.0.2", when="@:2019-03-29")

    license("CDDL-1.0")

    version(
        "2021-01-28", sha256="8824adee02ae4583bd378cc81140fbb49515c5965708ee98d856d122d48dd95f"
    )
    version(
        "2019-07-25", sha256="50338084ece92ec0fb13b0bbdf357b5d7450e26068ba501f23c315f814befc26"
    )
    version(
        "2019-03-29", sha256="053dda2023fe4bb6d7c1d66530c758c4e633bbf1f1be17b6b075b276fe8874f6"
    )

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    def cmake_args(self):
        args = []
        args.append(
            ("-DKIM_API_MODEL_DRIVER_INSTALL_PREFIX={0}" + "/lib/kim-api/model-drivers").format(
                prefix
            )
        )

        if self.spec.satisfies("@2019-07-25:"):
            args.append(
                (
                    "-DKIM_API_PORTABLE_MODEL_INSTALL_PREFIX={0}" + "/lib/kim-api/portable-models"
                ).format(prefix)
            )
        else:
            args.append(
                ("-DKIM_API_MODEL_INSTALL_PREFIX={0}" + "/lib/kim-api/models").format(prefix)
            )

        args.append(
            (
                "-DKIM_API_SIMULATOR_MODEL_INSTALL_PREFIX={0}" + "/lib/kim-api/simulator-models"
            ).format(prefix)
        )
        return args
