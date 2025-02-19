# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Percept(CMakePackage):
    """Parallel mesh refinement and adaptivity tools for the finite
    element method.
    """

    homepage = "https://github.com/PerceptTools/percept"
    git = "https://github.com/PerceptTools/percept.git"

    # The open version of Percept does not seem to be supported on
    # github and it doesn't have tags. So we specify a specific commit
    # here and the patch allows us to build the mesh_transfer exe and
    # creates a make install target so Spack can install Percept
    version("master", commit="363cdd0050443760d54162f140b2fb54ed9decf0")

    depends_on("cxx", type="build")  # generated
    patch("cmakelists.patch")

    depends_on("googletest~shared")
    depends_on("opennurbs@percept")
    depends_on("boost+graph+mpi")
    depends_on("yaml-cpp+pic~shared@0.5.3:")
    depends_on(
        "trilinos"
        "~shared+exodus+mpi+tpetra+epetra+epetraext+muelu+belos+ifpack2+amesos2"
        "+zoltan+stk+boost~superlu-dist+superlu+hdf5+aztec+sacado"
        "~openmp+shards+intrepid"
        "@master,12.14.1:"
    )

    def cmake_args(self):
        spec = self.spec
        options = []

        options.extend(
            [
                "-DSTK_PERCEPT_LITE:BOOL=OFF",
                "-DSTK_ADAPT_HAVE_YAML_CPP:BOOL=ON",
                "-DTrilinos_DIR:PATH=%s" % spec["trilinos"].prefix,
                "-DYAML_DIR:PATH=%s" % spec["yaml-cpp"].prefix,
                "-DBOOST_DIR:PATH=%s" % spec["boost"].prefix,
                "-DOPENNURBS_DIR:PATH=%s" % spec["opennurbs"].prefix,
                "-DOPENNURBS_INCLUDE_DIR:PATH=%s" % spec["opennurbs"].prefix.include,
                "-DOPENNURBS_LIBRARY_DIR:PATH=%s" % spec["opennurbs"].prefix.lib,
                "-DPERCEPT_TPLS_INSTALL_DIR:PATH=%s" % spec["googletest"].prefix,
            ]
        )

        return options
