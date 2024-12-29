# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Libhio(AutotoolsPackage):
    """libHIO is a flexible, high-performance parallel IO package developed
    at LANL.  libHIO supports IO to either a conventional PFS or to Cray
    DataWarp with management of Cray DataWarp space and stage-in and
    stage-out from and to the PFS.
    """

    homepage = "https://github.com/hpc/libhio"
    url = "https://github.com/hpc/libhio/releases/download/hio.1.4.1.0/libhio-1.4.1.0.tar.bz2"
    git = "https://github.com/hpc/libhio.git"
    maintainers("plamborn")

    #
    # We don't include older versions since they are missing features
    # needed by current and future consumers of libhio
    #
    version("master", branch="master")
    version("1.4.1.6", sha256="863e7274f9e32d97bd5d9e6745ad9449735bdc8bd5623f152a32be45e6f3a212")
    version("1.4.1.5", sha256="76f5a0eb306e9596cdef558586ed2ba47bf50a9cc7782beb1a8b37115c00b1ee")
    version("1.4.1.4", sha256="6998a424cff97be9a207032b3addd19f292d8ebda72043be92a8f942ae3b4da1")
    version("1.4.1.3", sha256="b6ad2354f1bc597e7e55fc989ff50944835d64149f4925c2f45df950919e4d08")
    version("1.4.1.2", sha256="87a0f9b72b7aa69485c40d9bd36f02af653b70e8eed3eb0b50eaeb02ff0a9049")
    version("1.4.1.1", sha256="5c65d18bf74357f9d9960bf6b9ad2432f8fc5a2b653e72befe4d1caabb9a2f7a")
    version("1.4.1.0", sha256="963f4a8d365afd92a5593f80946e2c4c79f4185d897436a43fae61dae5567ac4")

    depends_on("c", type="build")  # generated

    #
    # main users of libhio thru spack will want to use HFDF5 plugin,
    # so make hdf5 variant a default
    #
    variant("hdf5", default=True, description="Enable HDF5 support")

    depends_on("json-c")
    depends_on("bzip2")
    depends_on("pkgconfig", type="build")
    depends_on("mpi")

    #
    # libhio depends on hdf5+mpi if hdf5 is being used since it
    # autodetects the presence of an MPI and/or uses mpicc by default to build
    depends_on("hdf5+mpi", when="+hdf5")

    #
    # wow, we need to patch libhio
    #
    patch("0001-configury-fix-a-problem-with-bz2-configury.patch", when="@1.4.1.0")
    patch("0001-hdf5-make-docs-optional.patch", when="@1.4.1.0")
    patch("0001-spack-fix-for-spack-to-work-on-non-cray-systems.patch", when="@1.4.1.2")

    def configure_args(self):
        spec = self.spec
        args = []

        args.append("--with-external_bz2={0}".format(spec["bzip2"].prefix))
        if spec.satisfies("+hdf5"):
            args.append("--with-hdf5={0}".format(spec["hdf5"].prefix))

        args.append("--with-external-json={0}".format(spec["json-c"].prefix))

        return args
