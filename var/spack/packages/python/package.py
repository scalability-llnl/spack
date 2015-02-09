from spack import *
import spack
import os
import re
from contextlib import closing


class Python(Package):
    """The Python programming language."""
    homepage = "http://www.python.org"
    url      = "http://www.python.org/ftp/python/2.7.8/Python-2.7.8.tar.xz"

    extendable = True

    version('2.7.8', 'd235bdfa75b8396942e360a70487ee00')

    depends_on("openssl")
    depends_on("bzip2")
    depends_on("readline")
    depends_on("ncurses")
    depends_on("sqlite")

    def install(self, spec, prefix):
        # Need this to allow python build to find the Python installation.
        env['PYTHONHOME'] = prefix

        # Rest of install is pretty standard.
        configure("--prefix=%s" % prefix,
                  "--with-threads",
                  "--enable-shared")
        make()
        make("install")


    # ========================================================================
    # Set up environment to make install easy for python extensions.
    # ========================================================================

    @property
    def python_lib_dir(self):
        return os.path.join('lib', 'python%d.%d' % self.version[:2])


    @property
    def site_packages_dir(self):
        return os.path.join(self.python_lib_dir, 'site-packages')


    def setup_extension_environment(self, module, spec, ext_spec):
        """Called before python modules' install() methods.

        In most cases, extensions will only need to have one line::

            python('setup.py', 'install', '--prefix=%s' % prefix)
        """
        # Python extension builds can have a global python executable function
        module.python = Executable(join_path(spec.prefix.bin, 'python'))

        # Add variables for lib/pythonX.Y and lib/pythonX.Y/site-packages dirs.
        module.python_lib_dir = os.path.join(ext_spec.prefix, self.python_lib_dir)
        module.site_packages_dir = os.path.join(ext_spec.prefix, self.site_packages_dir)

        # Add site packages directory to the PYTHONPATH
        os.environ['PYTHONPATH'] = module.site_packages_dir

        # Make the site packages directory if it does not exist already.
        mkdirp(module.site_packages_dir)


    # ========================================================================
    # Handle specifics of activating and deactivating python modules.
    # ========================================================================

    def python_ignore(self, ext_pkg, args):
        """Add some ignore files to activate/deactivate args."""
        orig_ignore = args.get('ignore', lambda f: False)

        def ignore(filename):
            # Always ignore easy-install.pth, as it needs to be merged.
            patterns = [r'easy-install\.pth$']

            # Ignore pieces of setuptools installed by other packages.
            if ext_pkg.name != 'py-setuptools':
                patterns.append(r'/site\.pyc?$')
                patterns.append(r'setuptools\.pth')
                patterns.append(r'bin/easy_install[^/]*$')
                patterns.append(r'setuptools.*egg$')

            return (any(re.search(p, filename) for p in patterns) or
                    orig_ignore(filename))

        return ignore


    def write_easy_install_pth(self, extensions):
        paths = []
        for ext in extensions:
            ext_site_packages = os.path.join(ext.prefix, self.site_packages_dir)
            easy_pth = "%s/easy-install.pth" % ext_site_packages

            if not os.path.isfile(easy_pth):
                continue

            with closing(open(easy_pth)) as f:
                for line in f:
                    line = line.rstrip()

                    # Skip lines matching these criteria
                    if not line: continue
                    if re.search(r'^(import|#)', line): continue
                    if (ext.name != 'py-setuptools' and
                        re.search(r'setuptools.*egg$', line)): continue

                    paths.append(line)

        site_packages = os.path.join(self.prefix, self.site_packages_dir)
        main_pth = "%s/easy-install.pth" % site_packages

        if not paths:
            if os.path.isfile(main_pth):
                os.remove(main_pth)

        else:
            with closing(open(main_pth, 'w')) as f:
                f.write("import sys; sys.__plen = len(sys.path)\n")
                for path in paths:
                    f.write("%s\n" % path)
                f.write("import sys; new=sys.path[sys.__plen:]; del sys.path[sys.__plen:]; "
                        "p=getattr(sys,'__egginsert',0); sys.path[p:p]=new; sys.__egginsert = p+len(new)\n")


    def activate(self, ext_pkg, **args):
        args.update(ignore=self.python_ignore(ext_pkg, args))
        super(Python, self).activate(ext_pkg, **args)

        extensions = set(spack.install_layout.get_extensions(self.spec))
        extensions.add(ext_pkg.spec)
        self.write_easy_install_pth(extensions)


    def deactivate(self, ext_pkg, **args):
        args.update(ignore=self.python_ignore(ext_pkg, args))
        super(Python, self).deactivate(ext_pkg, **args)

        extensions = set(spack.install_layout.get_extensions(self.spec))
        extensions.remove(ext_pkg.spec)
        self.write_easy_install_pth(extensions)
