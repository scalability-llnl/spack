# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyNetcdf4(PythonPackage):
    """Python interface to the netCDF Library."""

    homepage = "https://github.com/Unidata/netcdf4-python"
    pypi = "netCDF4/netcdf4-1.2.7.tar.gz"

    maintainers("skosukhin")

    license("MIT")

    version(
        "1.7.1.post2", sha256="37d557e36654889d7020192bfb56f9d5f93894cb32997eb837ae586c538fd7b6"
    )
    version("1.6.5", sha256="824881d0aacfde5bd982d6adedd8574259c85553781e7b83e0ce82b890bfa0ef")
    version("1.6.2", sha256="0382b02ff6a288419f6ffec85dec40f451f41b8755547154c575ddd9f0f4ae53")
    version("1.5.8", sha256="ca3d468f4812c0999df86e3f428851fb0c17ac34ce0827115c246b0b690e4e84")
    version("1.5.3", sha256="2a3ca855848f4bbf07fac366da77a681fcead18c0a8813d91d46302f562dc3be")
    version("1.4.2", sha256="b934af350459cf9041bcdf5472e2aa56ed7321c018d918e9f325ec9a1f9d1a30")

    variant("mpi", default=True, description="Parallel IO support")

    depends_on("python", type=("build", "link", "run"))
    depends_on("py-cython@0.29:", when="@1.6.5:", type="build")
    depends_on("py-cython@0.19:", type="build")
    depends_on("py-setuptools@61:", when="@1.6.5:", type="build")
    depends_on("py-setuptools@41.2:", when="@1.6.2:", type="build")
    depends_on("py-setuptools@18:", when="@1.4.2:1.5.8", type="build")
    depends_on("py-setuptools-scm@3.4:+toml", when="@1.7:", type="build")
    depends_on("py-cftime", type=("build", "run"))
    depends_on("py-certifi", when="@1.6.5:", type=("build", "run"))
    depends_on("py-numpy", when="@1.6.5:", type=("build", "link", "run"))
    depends_on("py-numpy@1.9:", when="@1.5.4:1.6.2", type=("build", "link", "run"))
    depends_on("py-numpy@1.7:", type=("build", "link", "run"))
    # https://github.com/Unidata/netcdf4-python/pull/1317
    depends_on("py-numpy@:1", when="@:1.6", type=("build", "link", "run"))
    depends_on("py-mpi4py", when="+mpi", type=("build", "run"))
    depends_on("netcdf-c", when="-mpi")
    depends_on("netcdf-c+mpi", when="+mpi")
    depends_on("hdf5@1.8.0:+hl", when="-mpi")
    depends_on("hdf5@1.8.0:+hl+mpi", when="+mpi")

    # The installation script tries to find hdf5 using pkg-config. However, the
    # version of hdf5 installed with Spack does not have pkg-config files.
    # Therefore, if pkg-config finds hdf5.pc at all (e.g. provided by
    # Ubuntu/Debian package manager), it is definitely not what we need. The
    # following patch disables the usage of pkg-config at all.
    patch("disable_pkgconf.patch")

    # https://github.com/Unidata/netcdf4-python/pull/1322
    patch(
        "https://github.com/Unidata/netcdf4-python/commit/49dcd0b5bd25824c254770c0d41445133fc13a46.patch?full_index=1",
        sha256="71eefe1d3065ad050fb72eb61d916ae1374a3fafd96ddaee6499cda952d992c4",
        when="@1.6: %gcc@14:",
    )

    def url_for_version(self, version):
        url = "https://files.pythonhosted.org/packages/source/n/netCDF4/{}-{}.tar.gz"
        if version >= Version("1.7"):
            name = "netcdf4"
        else:
            name = "netCDF4"
        return url.format(name, version)

    def flag_handler(self, name, flags):
        if name == "cflags":
            if self.spec.satisfies("%oneapi") or self.spec.satisfies("%apple-clang@15:"):
                flags.append("-Wno-error=int-conversion")

        return flags, None, None

    def setup_build_environment(self, env):
        """Ensure installed netcdf and hdf5 libraries are used"""
        # Explicitly set these variables so setup.py won't erroneously pick up
        # system versions
        # See: http://unidata.github.io/netcdf4-python
        env.set("USE_SETUPCFG", "0")
        env.set("USE_NCCONFIG", "1")
        env.set("HDF5_DIR", self.spec["hdf5"].prefix)
        env.set("HDF5_INCDIR", self.spec["hdf5"].prefix.include)
        env.set("HDF5_LIBDIR", self.spec["hdf5"].prefix.lib)
        env.set("NETCDF4_DIR", self.spec["netcdf-c"].prefix)
        env.set("NETCDF4_INCDIR", self.spec["netcdf-c"].prefix.include)
        env.set("NETCDF4_LIBDIR", self.spec["netcdf-c"].prefix.lib)
