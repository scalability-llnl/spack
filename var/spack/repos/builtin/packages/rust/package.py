from spack import *
import os


def get_submodules():
    git = which('git')
    git('submodule', 'update', '--init', '--recursive')


class Rust(Package):
    """The rust programming language toolchain"""
    homepage = "http://www.rust-lang.org"
    url = "https://github.com/rust-lang/rust"

    version('1.8.0', tag='1.8.0', git="https://github.com/rust-lang/rust")

    resource(name='cargo',
             git="https://github.com/rust-lang/cargo.git",
             tag='0.10.0',
             destination='cargo')

    extendable = True

    # Rust
    depends_on("llvm")
    depends_on("curl")
    depends_on("git")
    depends_on("cmake")
    depends_on("python@2.0.0:2.999")

    # Cargo
    depends_on("openssl")

    def install(self, spec, prefix):
        configure('--prefix=%s' % prefix,
                  '--llvm-root=' + spec['llvm'].prefix)

        make()
        make("install")

        # Install cargo, rust package manager
        with working_dir(os.path.join('cargo', 'cargo')):
            get_submodules()
            configure('--prefix=' + prefix,
                      '--local-rust-root=' + prefix)

            make()
            make("install")

    def setup_dependent_package(self, module, ext_spec):
        """
        Called before python modules' install() methods.

        In most cases, extensions will only need to have one or two lines::

            cargo('build')
            cargo('install', '--root', prefix)

        or

            cargo('install', '--root', prefix)
        """
        # Rust extension builds can have a global cargo executable function
        module.cargo = Executable(join_path(self.spec.prefix.bin, 'cargo'))
