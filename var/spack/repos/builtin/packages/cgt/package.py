import os
from os import environ as env
import shutil

from spack.package import AutotoolsPackage, depends_on, variant, version, which

class Cgt(AutotoolsPackage):
    """NASA CGT"""

    homepage = "https://www.nas.nasa.gov/software/chimera.html"
    url = "file:///aerolab/admin/software/dist/cgt/chimera2.2git.tar.gz"

    version("2.2git", sha256="e5133b23af83d619ae99cb191539f2f62e88ddfb749a72a4f10fac294cf78597")

    variant("dp",    default=False, description="Enable double precision.")
    variant("oggui", default=True, description="Build Overgrid GUI.")
    variant("tecio", default=True, description="Enable TecIO support.")
    variant("esp",   default=True, description="Enable ESP support.")
    variant("omp",   default=True, description="Enable OpenMP support.")

    # required dependencies
    depends_on("tcl", type=("build", "run"))
    depends_on("tcsh", type="build")  # needed for lib/checkflags.csh, lib/cmpltm.csh

    # optional dependencies
    depends_on("tecio",  type=("build", "run"), when="+tecio")
    #depends_on("libx11", type=("build", "run"), when="+oggui")
    depends_on("tk",     type=("build", "run"), when="+oggui")
    depends_on("esp",    type=("build", "run"), when="+esp")

    # This came from Phil, but I'd rather build all targets
    #@property
    #def build_targets(self):
    #    targets = ["dp", "sp"]
    #    if "+oggui" in self.spec:
    #        targets += ["oggui"]
    #    return targets

    # Leaving this for reference but I'm doing this via the custom install() below
    #install_targets = ["CMD=installall"]

    def configure_args(self):
        spec = self.spec

        # The install phase needs the prefix dir to exist...
        #print(f"from configure_args: making {self.prefix}...")
        mkdirp(self.prefix)
        prefix_exists = os.path.exists(self.prefix)
        #print(f"from configure_args: prefix exists - {prefix_exists}")

        args = [
            f"--with-installdir={self.prefix}",
            f"--with-installalldir={self.prefix}",
        ]

        if self.compiler.name == "gcc":
            cpp=which("cpp")
            args.append(f"--with-cpp={cpp}")

        if spec.satisfies("+tecio"):
            args.append(f"--with-tecio_lib={spec['tecio'].prefix}/libtecio.so")

        if spec.satisfies("+omp"):
            args.append(f"--enable-omp")

        if spec.satisfies("+oggui"):
            args.append(f"--with-tcldir_so={spec['tcl'].prefix}/lib")
            args.append(f"--with-tcldir_inc={spec['tcl'].prefix}/include")
            args.append(f"--with-tkdir_so={spec['tk'].prefix}/lib")
            args.append(f"--with-tkdir_inc={spec['tk'].prefix}/include")

        return args

    def install(self, spec, prefix):

        # The mkdir's fail if done in parallel
        make("CMD=installall", parallel=False)

        # cgt's makefiles install binaries into `[prefix]/bin_dp` and `[prefix]/bin_sp`
        # we need to "install" the right one based on the spec
        if "+dp" in self.spec:
            bin_suffix = "_dp"
            del_suffix = "_sp"
        else:
            del_suffix = "_dp"
            bin_suffix = "_sp"

        bin_dir = join_path(prefix, f"bin{bin_suffix}")

        # Sym link the correct bin_* to just bin
        symlink(bin_dir, join_path(prefix, "bin"))

        # Remove the other one for good measure
        # On 2nd thought... we need both for overgrid to be happy
        #shutil.rmtree(join_path(prefix, f"bin{del_suffix}"))

    def patch(self):
        """Find all occurrences of #!/bin/csh and replace them with
        #!/usr/bin/env csh."""
        for file in find(".", "*", recursive=True):
            if os.path.isfile(file):
                if os.path.relpath(file).startswith(".git"):
                    continue
                # NOTE: this removes the -f, which is not supported with #!/usr/bin/env csh
                filter_file("#!\s*/bin/csh(?:\s+-f)?", "#!/usr/bin/env csh", file)

    def setup_build_environment(self, env):
        spec = self.spec

        # These are needed to get overgrid compiling correctly
        env.set("TCLDIR_INC", f"{spec['tcl'].prefix}/include")
        env.set("TCLDIR_SO",  f"{spec['tcl'].prefix}/lib")
        env.set("TKDIR_INC",  f"{spec['tk'].prefix}/include")
        env.set("TKDIR_SO",   f"{spec['tk'].prefix}/lib")

    def setup_run_environment(self, env):
        spec = self.spec
        env.set("CGT_DIR", self.prefix)
        env.set("CGTBINDIR", self.prefix.bin)
        env.set("SCRIPTLIB", self.prefix.scriptlib)
        env.set("TCLDIR_SO",  f"{spec['tcl'].prefix}/lib")
        env.set("TKDIR_SO",   f"{spec['tk'].prefix}/lib")
        env.prepend_path("LD_LIBRARY_PATH",   f"{spec['tcl'].prefix}/lib")
        env.prepend_path("LD_LIBRARY_PATH",   f"{spec['tk'].prefix}/lib")
