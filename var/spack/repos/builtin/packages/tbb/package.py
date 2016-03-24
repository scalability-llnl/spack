from spack import *
import os
import glob

class Tbb(Package):
    """Widely used C++ template library for task parallelism.
    Intel Threading Building Blocks (Intel TBB) lets you easily write parallel
    C++ programs that take full advantage of multicore performance, that are
    portable and composable, and that have future-proof scalability.
    """
    homepage = "http://www.threadingbuildingblocks.org/"

    # Only version-specific URL's work for TBB
    version('4.4.3', '80707e277f69d9b20eeebdd7a5f5331137868ce1', url='https://www.threadingbuildingblocks.org/sites/default/files/software_releases/source/tbb44_20160128oss_src_0.tgz')

    def coerce_to_spack(self,tbb_build_subdir):
        for compiler in ["icc","gcc","clang"]:
              fs = glob.glob(join_path(tbb_build_subdir,"*.%s.inc" % compiler ))
              for f in fs:
                  lines = open(f).readlines()
                  of = open(f,"w")
                  for l in lines:
                      if l.strip().startswith("CPLUS ="):
                        of.write("# coerced to spack\n")
                        of.write("CPLUS = $(CXX)\n")
                      elif l.strip().startswith("CPLUS ="):
                        of.write("# coerced to spack\n")
                        of.write("CONLY = $(CC)\n")
                      else:
                        of.write(l);

    def install(self, spec, prefix):
        #
        # we need to follow TBB's compiler selection logic to get the proper build + link flags
        # but we still need to use spack's compiler wrappers
        # to accomplish this, we do two things:
        #
        # * Look at the spack spec to determine which compiler we should pass to tbb's Makefile
        #
        # * patch tbb's build system to use the compiler wrappers (CC, CXX) for
        #    icc, gcc, clang
        #    (see coerce_to_spack())
        #
        self.coerce_to_spack("build")

        if spec.satisfies('%clang'):
            tbb_compiler = "clang"
        elif spec.satisfies('%intel'):
            tbb_compiler = "icc"
        else:
            tbb_compiler = "gcc"


        mkdirp(prefix)
        mkdirp(prefix.lib)

        #
        # tbb does not have a configure script or make install target
        # we simply call make, and try to put the pieces together
        #
        make("compiler=%s"  %(tbb_compiler))

        # install headers to {prefix}/include
        install_tree('include',prefix.include)

        # install libs to {prefix}/lib
        tbb_lib_names = ["libtbb",
                         "libtbbmalloc",
                         "libtbbmalloc_proxy"]

        for lib_name in tbb_lib_names:
            # install release libs
            fs = glob.glob(join_path("build","*release",lib_name + ".*"))
            for f in fs:
                install(f, prefix.lib)
            # install debug libs if they exist
            fs = glob.glob(join_path("build","*debug",lib_name + "_debug.*"))
            for f in fs:
                install(f, prefix.lib)
