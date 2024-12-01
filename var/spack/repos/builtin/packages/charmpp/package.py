# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


import os
import platform
import shutil
import sys

from spack.package import *


class Charmpp(Package):
    """Charm++ is a parallel programming framework in C++ supported by
    an adaptive runtime system, which enhances user productivity and
    allows programs to run portably from small multicore computers
    (your laptop) to the largest supercomputers."""

    homepage = "https://charmplusplus.org"
    url = "https://charm.cs.illinois.edu/distrib/charm-6.8.2.tar.gz"
    git = "https://github.com/UIUC-PPL/charm.git"

    maintainers("matthiasdiener")

    version("main", branch="main")

    version(
        "8.0.0",
        sha256="e30fc1e921e5cbf3406e792d5b0ca5f211c5d8ffbfc56e56d5501d8118abcaf6",
        url="https://github.com/charmplusplus/charm/archive/refs/tags/v8.0.0.tar.gz",
    )
    version("7.0.0", sha256="9c247b421bb157bdf9bc0ced3e25738c7a1dc1f7ec57b7943a7faf97f7e4fb2e")
    version("6.10.2", sha256="7abb4cace8aebdfbb8006eac03eb766897c009cfb919da0d0a33f74c3b4e6deb")
    version("6.10.1", sha256="ab96198105daabbb8c8bdf370f87b0523521ce502c656cb6cd5b89f69a2c70a8")
    version("6.10.0", sha256="7c526a78aa0c202b7f0418b345138e7dc40496f0bb7b9e301e0381980450b25c")
    version("6.9.0", sha256="85ed660e46eeb7a6fc6b32deab08226f647c244241948f6b592ebcd2b6050cbd")
    version("6.8.2", sha256="08e6001b0e9cd00ebde179f76098767149bf7e454f29028fb9a8bfb55778698e")
    version("6.8.1", sha256="bf39666bb9f8bad1cd17dafa3cdf35c7ef64dfaeda835cf66ae530b7baab7583")
    version("6.8.0", sha256="deca68622932ea0c677aa764d6d24cd169a2fd99c06e7d7b6947c0f18ec2f8f3")
    version("6.7.1", sha256="744a093874fbac03b6ae8be3ce434eff46b2ee778561e860802ed578e0810fdf")
    version("6.7.0", sha256="6b0d8215a180c90cf6ee33ff39f66726934df34aaeeed59650dd3a0cc54d0c87")
    version("6.6.1", sha256="2aa16fd3015dce0a0932ab5253578a72ddbcb889bc0d23584c42b28446915467")
    version("6.6.0", sha256="c916010f2d4cc2c6bd30ea19764839d0298fb56d1696d8ff08d9fa9a61dfb1c9")
    version("6.5.1", sha256="68aa43e2a6e476e116a7e80e385c25c6ac6497807348025505ba8bfa256ed34a")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    # Support OpenMPI; see
    # <https://github.com/UIUC-PPL/charm/issues/1206>
    # Patch is no longer needed in versions 6.8.0+
    patch("mpi.patch", when="@:6.7.1")

    # Patch for AOCC
    patch("charm_6.7.1_aocc.patch", when="@6.7.1 %aocc", level=1)
    patch("charm_6.8.2_aocc.patch", when="@6.8.2 %aocc", level=3)

    # support Fujitsu compiler
    patch("fj.patch", when="%fj")

    # support NVIDIA compilers
    patch("nvhpc.patch", when="%nvhpc")

    # Ignore compiler warnings while configuring
    patch("strictpass.patch", when="@:6.8.2")

    # Support Cray Shasta with ARM
    patch("ofi-crayshasta-arm.patch", when="backend=ofi pmi=cray-pmi target=aarch64:")

    # Build targets
    # "target" is reserved, so we have to use something else.
    variant(
        "build-target",
        default="LIBS",
        # AMPI also builds charm++, LIBS also builds AMPI and charm++
        values=("charm++", "AMPI", "LIBS", "ChaNGa"),
        description="Specify the target to build",
    )

    # Communication mechanisms (choose exactly one)
    # - Default to 'multicore' on macOS because that's probably the right choice
    #   for a personal machine.
    if sys.platform == "darwin":
        backend_default = "multicore"
    else:
        backend_default = "netlrts"
    variant(
        "backend",
        default=backend_default,
        values=("mpi", "multicore", "netlrts", "verbs", "gni", "ucx", "ofi", "pami", "pamilrts"),
        description="Set the backend to use",
    )

    # Process management interface
    variant(
        "pmi",
        default="none",
        values=("none", "simplepmi", "slurmpmi", "slurmpmi2", "pmix", "cray-pmi"),
        description="The ucx/ofi/gni backends need PMI to run!",
    )

    # Other options
    variant("papi", default=False, description="Enable PAPI integration")
    variant("syncft", default=False, description="Compile with Charm++ fault tolerance support")
    variant("smp", default=True, description="Enable SMP parallelism")
    variant("tcp", default=False, description="Use TCP as transport mechanism (requires +net)")
    variant("omp", default=False, description="Support for the integrated LLVM OpenMP runtime")
    variant("pthreads", default=False, description="Compile with pthreads Converse threads")
    variant("cuda", default=False, description="Enable CUDA toolkit")

    variant("shared", default=True, description="Enable shared link support")
    variant("production", default=True, description="Build charm++ with all optimizations")
    variant("tracing", default=False, description="Enable tracing modules")

    # Versions 7.0.0+ use CMake by default when it's available. It's more
    # robust.
    depends_on("cmake@3.4:", when="@7.0.0:", type="build")

    depends_on("mpi", when="backend=mpi")
    depends_on("papi", when="+papi")
    depends_on("cuda", when="+cuda")

    depends_on("ucx", when="backend=ucx")
    depends_on("libfabric", when="backend=ofi")
    depends_on("slurm@:17-11-9-2", when="pmi=slurmpmi")
    depends_on("slurm@17-11-9-2:", when="pmi=slurmpmi2")

    # FIXME : As of now spack's OpenMPI recipe does not have a PMIx variant
    # But if users have external installs of OpenMPI with PMIx support, this
    # will allow them to build charm++ with it.
    depends_on("openmpi", when="pmi=pmix")

    depends_on("mpi", when="pmi=simplepmi")
    depends_on("mpi", when="pmi=slurmpmi")
    depends_on("mpi", when="pmi=slurmpmi2")
    depends_on("cray-mpich", when="pmi=cray-pmi")

    # Git versions of Charm++ require automake and autoconf
    depends_on("automake", when="@develop")
    depends_on("autoconf", when="@develop")

    conflicts("~tracing", "+papi")

    conflicts("backend=multicore", when="~smp", msg="The 'multicore' backend always uses SMP")
    conflicts("backend=ucx", when="@:6.9")

    # Shared-lib builds with GCC are broken on macOS:
    # https://github.com/UIUC-PPL/charm/issues/3181
    conflicts("+shared", when="platform=darwin %gcc")

    # Charm++ versions below 7.0.0 have build issues on macOS, mainly due to the
    # pre-7.0.0 `VERSION` file conflicting with other version files on the
    # system: https://github.com/UIUC-PPL/charm/issues/2844. Specifically, it
    # conflicts with LLVM's `<version>` header that was added in llvm@7.0.0 to
    # comply with the C++20 standard:
    # https://en.cppreference.com/w/cpp/header/version. The conflict only occurs
    # on case-insensitive file systems, as typically used on macOS machines.
    conflicts("@:6", when="platform=darwin %apple-clang@7:")
    conflicts("@:6", when="platform=darwin %clang@7:")

    @property
    def charmarch(self):
        plat = sys.platform

        if plat.startswith("linux"):
            plat = "linux"
        elif plat.startswith("win"):
            plat = "win"
        elif plat.startswith("cnl"):
            plat = "cnl"
        elif plat.startswith("cnk"):
            plat = "cnk"

        mach = platform.machine()

        if mach.startswith("ppc"):
            mach = "ppc"
        elif mach.startswith("arm"):
            mach = "arm"

        comm = self.spec.variants["backend"].value

        # Define Charm++ version names for various (plat, mach, comm)
        # combinations. Note that not all combinations are supported.
        versions = {
            ("darwin", "x86_64", "mpi"): "mpi-darwin-x86_64",
            ("darwin", "x86_64", "multicore"): "multicore-darwin-x86_64",
            ("darwin", "x86_64", "netlrts"): "netlrts-darwin-x86_64",
            ("linux", "x86_64", "mpi"): "mpi-linux-x86_64",
            ("linux", "x86_64", "multicore"): "multicore-linux-x86_64",
            ("linux", "x86_64", "netlrts"): "netlrts-linux-x86_64",
            ("linux", "x86_64", "verbs"): "verbs-linux-x86_64",
            ("linux", "x86_64", "ofi"): "ofi-linux-x86_64",
            ("linux", "ppc", "mpi"): "mpi-linux-ppc",
            ("linux", "ppc", "multicore"): "multicore-linux-ppc",
            ("linux", "ppc", "netlrts"): "netlrts-linux-ppc",
            ("linux", "ppc", "pami"): "pami-linux-ppc64le",
            ("linux", "ppc", "verbs"): "verbs-linux-ppc64le",
            ("linux", "arm", "netlrts"): "netlrts-linux-arm7",
            ("linux", "aarch64", "netlrts"): "netlrts-linux-arm8",
            ("win", "x86_64", "mpi"): "mpi-win-x86_64",
            ("win", "x86_64", "multicore"): "multicore-win-x86_64",
            ("win", "x86_64", "netlrts"): "netlrts-win-x86_64",
            ("cnl", "x86_64", "gni"): "gni-crayxc",
            ("cnl", "x86_64", "mpi"): "mpi-crayxc",
        }

        if self.spec.satisfies("@6.10:"):
            versions.update(
                {
                    ("linux", "x86_64", "ucx"): "ucx-linux-x86_64",
                    ("linux", "aarch64", "ucx"): "ucx-linux-arm8",
                }
            )

        # Some versions were renamed/removed in 6.11
        if self.spec.version < Version("6.11.0"):
            versions.update(
                {
                    ("linux", "i386", "mpi"): "mpi-linux",
                    ("linux", "i386", "multicore"): "multicore-linux",
                    ("linux", "i386", "netlrts"): "netlrts-linux",
                    ("linux", "i386", "uth"): "uth-linux",
                    ("linux", "arm", "multicore"): "multicore-arm7",
                    ("linux", "aarch64", "multicore"): "multicore-arm8",
                }
            )
        else:
            versions.update(
                {
                    ("linux", "i386", "mpi"): "mpi-linux-i386",
                    ("linux", "i386", "multicore"): "multicore-linux-i386",
                    ("linux", "i386", "netlrts"): "netlrts-linux-i386",
                    ("linux", "arm", "multicore"): "multicore-linux-arm7",
                    ("linux", "aarch64", "multicore"): "multicore-linux-arm8",
                }
            )

        if self.spec.satisfies("@7:"):
            versions.update(
                {
                    ("linux", "arm", "mpi"): "mpi-linux-arm7",
                    ("linux", "aarch64", "mpi"): "mpi-linux-arm8",
                    ("darwin", "arm", "multicore"): "multicore-darwin-arm8",
                    ("darwin", "arm", "netlrts"): "netlrts-darwin-arm8",
                    ("darwin", "arm", "mpi"): "mpi-darwin-arm8",
                }
            )

            if self.spec.satisfies("backend=ofi pmi=cray-pmi"):
                versions.update(
                    {
                        ("linux", "x86_64", "ofi"): "ofi-crayshasta",
                        ("linux", "aarch64", "ofi"): "ofi-crayshasta",
                    }
                )

        if (plat, mach, comm) not in versions:
            raise InstallError(
                "The communication mechanism %s is not supported "
                "on a %s platform with a %s CPU" % (comm, plat, mach)
            )

        return versions[(plat, mach, comm)]

    # FIXME: backend=mpi also provides mpi, but spack does not support
    # depends_on("mpi") and provides("mpi") in the same package currently.
    # for b in ['multicore', 'netlrts', 'verbs', 'gni', 'ofi', 'pami',
    #          'pamilrts']:
    #    provides('mpi@2', when='@6.7.1:
    #            build-target=AMPI backend={0}'.format(b))
    #    provides('mpi@2', when='@6.7.1:
    #            build-target=LIBS backend={0}'.format(b))

    def install(self, spec, prefix):
        if not ("backend=mpi" in self.spec) or not ("backend=netlrts" in self.spec):
            if self.spec.satisfies("+pthreads"):
                raise InstallError(
                    "The pthreads option is only\
                                    available on the Netlrts and MPI \
                                    network layers."
                )

        if (
            ("backend=ucx" in self.spec)
            or ("backend=ofi" in self.spec)
            or ("backend=gni" in self.spec)
        ):
            if self.spec.satisfies("pmi=none"):
                raise InstallError(
                    "The UCX/OFI/GNI backends need \
                                    PMI to run. Please add pmi=... \
                                    Note that PMIx is the preferred \
                                    option."
                )

        if (
            ("pmi=simplepmi" in self.spec)
            or ("pmi=slurmpmi" in self.spec)
            or ("pmi=slurmpmi2" in self.spec)
        ):
            if self.spec.satisfies("^openmpi"):
                raise InstallError(
                    "To use any process management \
                                    interface other than PMIx, \
                                    a non OpenMPI based MPI must be \
                                    present on the system"
                )

        target = spec.variants["build-target"].value
        builddir = prefix

        # We assume that Spack's compiler wrappers make this work. If
        # not, then we need to query the compiler vendor from Spack
        # here.
        options = [os.path.basename(self.compiler.cc)]

        if "@:6.8.2 %aocc" not in spec:
            options.append(os.path.basename(self.compiler.fc))

        options.append("-j%d" % make_jobs)
        options.append("--destination=%s" % builddir)

        if spec.satisfies("pmi=slurmpmi"):
            options.append("slurmpmi")
        if spec.satisfies("pmi=slurmpmi2"):
            options.append("slurmpmi2")
        if spec.satisfies("pmi=pmix"):
            options.append("ompipmix")
            options.extend(["--basedir=%s" % spec["openmpi"].prefix])

        if spec.satisfies("backend=mpi"):
            # in intelmpi <prefix>/include and <prefix>/lib fails so --basedir
            # cannot be used
            options.extend(
                ["--incdir={0}".format(incdir) for incdir in spec["mpi"].headers.directories]
            )
            options.extend(
                ["--libdir={0}".format(libdir) for libdir in spec["mpi"].libs.directories]
            )

        if spec.satisfies("backend=ucx"):
            options.extend(["--basedir=%s" % spec["ucx"].prefix])
        if spec.satisfies("+papi"):
            options.extend(["papi", "--basedir=%s" % spec["papi"].prefix])
        if "+smp" in spec and "backend=multicore" not in spec:
            # The 'multicore' backend always uses SMP, so we don't have to
            # append the 'smp' option when the 'multicore' backend is active. As
            # of Charm++ v7.0.0 it is actually a build error to append 'smp'
            # with the 'multicore' backend.
            options.append("smp")
        if spec.satisfies("+tcp"):
            if "backend=netlrts" not in spec:
                # This is a Charm++ limitation; it would lead to a
                # build error
                raise InstallError(
                    "The +tcp variant requires " "the backend=netlrts communication mechanism"
                )
            options.append("tcp")
        if spec.satisfies("+omp"):
            options.append("omp")
        if spec.satisfies("+pthreads"):
            options.append("pthreads")
        if spec.satisfies("+cuda"):
            options.append("cuda")

        if spec.satisfies("+shared"):
            options.append("--build-shared")
        if spec.satisfies("+production"):
            options.append("--with-production")
        if spec.satisfies("+tracing"):
            options.append("--enable-tracing")

        # charmpp build was failing with clang based compilers for -DNETWORK=mpi as discussed in
        # https://github.com/charmplusplus/charm/issues/3645
        # Fix was suggested in https://github.com/charmplusplus/charm/pull/3646 and the same has
        # been implemented in v8.0.0
        if self.spec.satisfies("@8.0.0: %aocc"):
            options.append("--disable-fortran")

        # Call "make" via the build script
        # Note: This builds Charm++ in the "tmp" subdirectory of the
        # install directory. Maybe we could set up a symbolic link
        # back to the build tree to prevent this? Alternatively, we
        # could dissect the build script; the build instructions say
        # this wouldn't be difficult.
        build = Executable(join_path(".", "build"))
        build(target, self.charmarch, *options)

        # Charm++'s install script does not copy files, it only creates
        # symbolic links. Fix this.
        for dirpath, dirnames, filenames in os.walk(builddir):
            for filename in filenames:
                filepath = join_path(dirpath, filename)
                if os.path.islink(filepath):
                    tmppath = filepath + ".tmp"
                    # Skip dangling symbolic links
                    try:
                        copy(filepath, tmppath)
                        os.remove(filepath)
                        os.rename(tmppath, filepath)
                    except (IOError, OSError):
                        pass

        tmp_path = join_path(builddir, "tmp")
        if not os.path.islink(tmp_path):
            shutil.rmtree(tmp_path)

        if self.spec.satisfies("@6.9.99"):
            # A broken 'doc' link in the prefix can break the build.
            # Remove it and replace it if it is broken.
            try:
                os.stat(prefix.doc)
            except OSError:
                os.remove(prefix.doc)
                mkdirp(prefix.doc)

    @run_after("install")
    @on_package_attributes(run_tests=True)
    def check_build(self):
        make(
            "-C",
            join_path(self.stage.source_path, "tests"),
            "test",
            "TESTOPTS=++local",
            parallel=False,
        )

    def setup_dependent_build_environment(self, env, dependent_spec):
        if not self.spec.satisfies("backend=mpi"):
            env.set("MPICC", self.prefix.bin.ampicc)
            env.set("MPICXX", self.prefix.bin.ampicxx)
            env.set("MPIF77", self.prefix.bin.ampif77)
            env.set("MPIF90", self.prefix.bin.ampif90)

    def setup_dependent_package(self, module, dependent_spec):
        self.spec.mpicc = self.prefix.bin.ampicc
        self.spec.mpicxx = self.prefix.bin.ampicxx
        self.spec.mpifc = self.prefix.bin.ampif90
        self.spec.mpif77 = self.prefix.bin.ampif77
        self.spec.charmarch = self.charmarch + "-smp" if self.spec.satisfies("+smp") else ""
