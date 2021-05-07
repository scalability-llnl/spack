.. Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
   Spack Project Developers. See the top-level COPYRIGHT file for details.

   SPDX-License-Identifier: (Apache-2.0 OR MIT)

.. _pythonpackage:

-------------
PythonPackage
-------------

Python packages and modules have their own special build system.

^^^^^^
Phases
^^^^^^

The ``PythonPackage`` base class provides the following phases that
can be overridden:

* ``build``
* ``build_py``
* ``build_ext``
* ``build_clib``
* ``build_scripts``
* ``install``
* ``install_lib``
* ``install_headers``
* ``install_scripts``
* ``install_data``

These are all standard ``setup.py`` commands and can be found by running:

.. code-block:: console

   $ python setup.py --help-commands


By default, only the ``build`` and ``install`` phases are run:

#. ``build`` - build everything needed to install
#. ``install`` - install everything from build directory

If for whatever reason you need to run more phases, simply modify your
``phases`` list like so:

.. code-block:: python

   phases = ['build_ext', 'install']


Each phase provides a function ``<phase>`` that runs:

.. code-block:: console

   $ python -s setup.py --no-user-cfg <phase>


Each phase also has a ``<phase_args>`` function that can pass arguments to
this call. All of these functions are empty except for the ``install_args``
function, which passes ``--prefix=/path/to/installation/prefix``. There is
also some additional logic specific to setuptools and eggs.

If you need to run a phase that is not a standard ``setup.py`` command,
you'll need to define a function for it like so:

.. code-block:: python

   phases = ['configure', 'build', 'install']

   def configure(self, spec, prefix):
       self.setup_py('configure')


^^^^^^
Wheels
^^^^^^

Some Python packages are closed-source and distributed as wheels.
Instead of using the ``PythonPackage`` base class, you should extend
the ``Package`` base class and implement the following custom installation
procedure:

.. code-block:: python

   def install(self, spec, prefix):
       pip = which('pip')
       pip('install', self.stage.archive_file, '--prefix={0}'.format(prefix))


This will require a dependency on pip, as mentioned below.

^^^^^^^^^^^^^^^
Important files
^^^^^^^^^^^^^^^

Python packages can be identified by the presence of a ``setup.py`` file.
This file is used by package managers like ``pip`` to determine a
package's dependencies and the version of dependencies required, so if
the ``setup.py`` file is not accurate, the package will not build properly.
For this reason, the ``setup.py`` file should be fairly reliable. If the
documentation and ``setup.py`` disagree on something, the ``setup.py``
file should be considered to be the truth. As dependencies are added or
removed, the documentation is much more likely to become outdated than
the ``setup.py``.

The Python ecosystem has evolved significantly over the years. Before
setuptools became popular, most packages listed their dependencies in a
``requirements.txt`` file. Once setuptools took over, these dependencies
were listed directly in the ``setup.py``. Newer PEPs introduced additional
files, like ``setup.cfg`` and ``pyproject.toml``. You should look out for
all of these files, as they may all contain important information about
package dependencies.

Some Python packages are closed-source and are distributed as Python
wheels. For example, ``py-azureml-sdk`` downloads a ``.whl`` file. This
file is simply a zip file, and can be extracted using:

.. code-block:: console

   $ unzip *.whl


The zip file will not contain a ``setup.py``, but it will contain a
``METADATA`` file which contains all the information you need to
write a ``package.py`` build recipe.

^^^^
PyPI
^^^^

The vast majority of Python packages are hosted on PyPI - The Python
Package Index. ``pip`` only supports packages hosted on PyPI, making
it the only option for developers who want a simple installation.
Search for "PyPI <package-name>" to find the download page. Note that
some pages are versioned, and the first result may not be the newest
version. Click on the "Latest Version" button to the top right to see
if a newer version is available. The download page is usually at::

   https://pypi.org/project/<package-name>


Since PyPI is so common, the ``PythonPackage`` base class has a
``pypi`` attribute that can be set. Once set, ``pypi`` will be used
to define the ``homepage``, ``url``, and ``list_url``. For example,
the following:

.. code-block:: python

   homepage = 'https://pypi.org/project/setuptools/'
   url      = 'https://pypi.org/packages/source/s/setuptools/setuptools-49.2.0.zip'
   list_url = 'https://pypi.org/simple/setuptools/'


is equivalent to:

.. code-block:: python

   pypi = 'setuptools/setuptools-49.2.0.zip'


^^^^^^^^^^^
Description
^^^^^^^^^^^

The top of the PyPI downloads page contains a description of the
package. The first line is usually a short description, while there
may be a several line "Project Description" that follows. Choose whichever
is more useful. You can also get these descriptions on the command-line
using:

.. code-block:: console

   $ python setup.py --description
   $ python setup.py --long-description


^^^^^^^^
Homepage
^^^^^^^^

Package developers use ``setup.py`` to upload new versions to PyPI.
The ``setup`` method often passes metadata like ``homepage`` to PyPI.
This metadata is displayed on the left side of the download page.
Search for the text "Homepage" under "Project links" to find it. You
should use this page instead of the PyPI page if they differ. You can
also get the homepage on the command-line by running:

.. code-block:: console

   $ python setup.py --url


^^^
URL
^^^

If ``pypi`` is set as mentioned above, ``url`` and ``list_url`` will
be automatically set for you. If both ``.tar.gz`` and ``.zip`` versions
are available, ``.tar.gz`` is preferred. If some releases offer both
``.tar.gz`` and ``.zip`` versions, but some only offer ``.zip`` versions,
use ``.zip``.

Some Python packages are closed-source and do not ship ``.tar.gz`` or ``.zip``
files on either PyPI or GitHub. If this is the case, you can still download
and install a Python wheel. For example, ``py-azureml-sdk`` is closed source
and can be downloaded from::

   https://pypi.io/packages/py3/a/azureml_sdk/azureml_sdk-1.11.0-py3-none-any.whl


You may see Python-specific or OS-specific URLs. Note that when you add a
``.whl`` URL, you should add ``expand=False`` to ensure that Spack doesn't
try to extract the wheel:

.. code-block:: python

   version('1.11.0', sha256='d8c9d24ea90457214d798b0d922489863dad518adde3638e08ef62de28fb183a', expand=False)


"""""""""""""""
PyPI vs. GitHub
"""""""""""""""

Many packages are hosted on PyPI, but are developed on GitHub or another
version control systems. The tarball can be downloaded from either
location, but PyPI is preferred for the following reasons:

#. PyPI contains the bare minimum number of files needed to install the package.

   You may notice that the tarball you download from PyPI does not
   have the same checksum as the tarball you download from GitHub.
   When a developer uploads a new release to PyPI, it doesn't contain
   every file in the repository, only the files necessary to install
   the package. PyPI tarballs are therefore smaller.

#. PyPI is the official source for package managers like ``pip``.

   Let's be honest, ``pip`` is much more popular than Spack. If the
   GitHub tarball contains a file not present in the PyPI tarball that
   causes a bug, the developers may not realize this for quite some
   time. If the bug was in a file contained in the PyPI tarball, users
   would notice the bug much more quickly.

#. GitHub release may be a beta version.

   When a developer releases a new version of a package on GitHub,
   it may not be intended for most users. Until that release also
   makes its way to PyPI, it should be assumed that the release is
   not yet ready for general use.

#. The checksum for a GitHub release may change.

   Unfortunately, some developers have a habit of patching releases
   without incrementing the version number. This results in a change
   in tarball checksum. Package managers like Spack that use checksums
   to verify the integrity of a download tarball grind to a halt when
   the checksum for a known version changes. Most of the time, the
   change is intentional, and contains a needed bug fix. However,
   sometimes the change indicates a download source that has been
   compromised, and a tarball that contains a virus. If this happens,
   you must contact the developers to determine which is the case.
   PyPI is nice because it makes it physically impossible to
   re-release the same version of a package with a different checksum.

^^^^^^^^^^^^^^^^^^^^^^^^^
Build system dependencies
^^^^^^^^^^^^^^^^^^^^^^^^^

There are a few dependencies common to the ``PythonPackage`` build system.

""""""
Python
""""""

Obviously, every ``PythonPackage`` needs Python at build-time to run
``python setup.py build && python setup.py install``. Python is also
needed at run-time if you want to import the module. Due to backwards
incompatible changes between Python 2 and 3, it is very important to
specify which versions of Python are supported. If the documentation
mentions that Python 3 is required, this can be specified as:

.. code-block:: python

   depends_on('python@3:', type=('build', 'run'))


If Python 2 is required, this would look like:

.. code-block:: python

   depends_on('python@:2', type=('build', 'run'))


If Python 2.7 is the only version that works, you can use:

.. code-block:: python

   depends_on('python@2.7:2.8', type=('build', 'run'))


The documentation may not always specify supported Python versions.
Another place to check is in the ``setup.py`` or ``setup.cfg`` file.
Look for a line containing ``python_requires``. An example from
`py-numpy <https://github.com/spack/spack/blob/develop/var/spack/repos/builtin/packages/py-numpy/package.py>`_
looks like:

.. code-block:: python

   python_requires='>=2.7,!=3.0.*,!=3.1.*,!=3.2.*,!=3.3.*'


You may also find a version check at the top of the ``setup.py``:

.. code-block:: python

   if sys.version_info[:2] < (2, 7) or (3, 0) <= sys.version_info[:2] < (3, 4):
       raise RuntimeError("Python version 2.7 or >= 3.4 required.")


This can be converted to Spack's spec notation like so:

.. code-block:: python

   depends_on('python@2.7:2.8,3.4:', type=('build', 'run'))


If you are writing a recipe for a package that only distributes
wheels, look for a section in the ``METADATA`` file that looks like::

   Requires-Python: >=3.5,<4


This would be translated to:

.. code-block:: python

   extends('python')
   depends_on('python@3.5:3.999', type=('build', 'run'))


Many ``setup.py`` or ``setup.cfg`` files also contain information like::

   Programming Language :: Python :: 2
   Programming Language :: Python :: 2.6
   Programming Language :: Python :: 2.7
   Programming Language :: Python :: 3
   Programming Language :: Python :: 3.3
   Programming Language :: Python :: 3.4
   Programming Language :: Python :: 3.5
   Programming Language :: Python :: 3.6


This is a list of versions of Python that the developer likely tests.
However, you should not use this to restrict the versions of Python
the package uses unless one of the two former methods (``python_requires``
or ``sys.version_info``) is used. There is no logic in setuptools
that prevents the package from building for Python versions not in
this list, and often new releases like Python 3.7 or 3.8 work just fine.

""""""""""
setuptools
""""""""""

Originally, the Python language had a single build system called
distutils, which is built into Python. Distutils provided a common
framework for package authors to describe their project and how it
should be built. However, distutils was not without limitations.
Most notably, there was no way to list a project's dependencies
with distutils. Along came setuptools, a non-builtin build system
designed to overcome the limitations of distutils. Both projects
use a similar API, making the transition easy while adding much
needed functionality. Today, setuptools is used in around 90% of
the Python packages in Spack.

Since setuptools isn't built-in to Python, you need to add it as a
dependency. To determine whether or not a package uses setuptools,
search the file for an import statement like:

.. code-block:: python

   import setuptools


or:

.. code-block:: python

   from setuptools import setup


Some packages are designed to work with both setuptools and distutils,
so you may find something like:

.. code-block:: python

   try:
       from setuptools import setup
   except ImportError:
       from distutils.core import setup


This uses setuptools if available, and falls back to distutils if not.
In this case, you would still want to add a setuptools dependency, as
it offers us more control over the installation.

Unless specified otherwise, setuptools is usually a build-only dependency.
That is, it is needed to install the software, but is not needed at
run-time. This can be specified as:

.. code-block:: python

   depends_on('py-setuptools', type='build')


"""
pip
"""

Packages distributed as Python wheels will require an extra dependency
on pip:

.. code-block:: python

   depends_on('py-pip', type='build')


We will use pip to install the actual wheel.

""""""
cython
""""""

Compared to compiled languages, interpreted languages like Python can
be quite a bit slower. To work around this, some Python developers
rewrite computationally demanding sections of code in C, a process
referred to as "cythonizing". In order to build these package, you
need to add a build dependency on cython:

.. code-block:: python

   depends_on('py-cython', type='build')


Look for references to "cython" in the ``setup.py`` to determine
whether or not this is necessary. Cython may be optional, but
even then you should list it as a required dependency. Spack is
designed to compile software, and is meant for HPC facilities
where speed is crucial. There is no reason why someone would not
want an optimized version of a library instead of the pure-Python
version.

Note that some release tarballs come pre-cythonized, and cython is
not needed as a dependency. However, this is becoming less common
as Python continues to evolve and developers discover that cythonized
sources are no longer compatible with newer versions of Python and
need to be re-cythonized.

^^^^^^^^^^^^^^^^^^^
Python dependencies
^^^^^^^^^^^^^^^^^^^

When you install a package with ``pip``, it reads the ``setup.py``
file in order to determine the dependencies of the package.
If the dependencies are not yet installed, ``pip`` downloads them
and installs them for you. This may sound convenient, but Spack
cannot rely on this behavior for two reasons:

#. Spack needs to be able to install packages on air-gapped networks.

   If there is no internet connection, ``pip`` can't download the
   package dependencies. By explicitly listing every dependency in
   the ``package.py``, Spack knows what to download ahead of time.

#. Duplicate installations of the same dependency may occur.

   Spack supports *activation* of Python extensions, which involves
   symlinking the package installation prefix to the Python installation
   prefix. If your package is missing a dependency, that dependency
   will be installed to the installation directory of the same package.
   If you try to activate the package + dependency, it may cause a
   problem if that package has already been activated.

For these reasons, you must always explicitly list all dependencies.
Although the documentation may list the package's dependencies,
often the developers assume people will use ``pip`` and won't have to
worry about it. Always check the ``setup.py`` to find the true
dependencies.

If the package relies on ``distutils``, it may not explicitly list its
dependencies. Check for statements like:

.. code-block:: python

   try:
       import numpy
   except ImportError:
       raise ImportError("numpy must be installed prior to installation")


Obviously, this means that ``py-numpy`` is a dependency.

If the package uses ``setuptools``, check for the following clues:

* ``python_requires``

  As mentioned above, this specifies which versions of Python are
  required.

* ``setup_requires``

  These packages are usually only needed at build-time, so you can
  add them with ``type='build'``.

* ``install_requires``

  These packages are required for building and installation. You can
  add them with ``type=('build', 'run')``.

* ``extra_requires``

  These packages are optional dependencies that enable additional
  functionality. You should add a variant that optionally adds these
  dependencies. This variant should be False by default.

* ``test_requires``

  These are packages that are required to run the unit tests for the
  package. These dependencies can be specified using the
  ``type='test'`` dependency type. However, the PyPI tarballs rarely
  contain unit tests, so there is usually no reason to add these.

In the root directory of the package, you may notice a
``requirements.txt`` file. It may look like this file contains a list
of all of the package's dependencies. Don't be fooled. This file is
used by tools like Travis to install the pre-requisites for the
package... and a whole bunch of other things. It often contains
dependencies only needed for unit tests, like:

* mock
* nose
* pytest

It can also contain dependencies for building the documentation, like
sphinx. If you can't find any information about the package's
dependencies, you can take a look in ``requirements.txt``, but be sure
not to add test or documentation dependencies.

Newer PEPs have added alternative ways to specify a package's dependencies.
If you don't see any dependencies listed in the ``setup.py``, look for a
``setup.cfg`` or ``pyproject.toml``. These files can be used to store the
same ``install_requires`` information that ``setup.py`` used to use.

If you are write a recipe for a package that only distributes wheels,
check the ``METADATA`` file for lines like::

   Requires-Dist: azureml-core (~=1.11.0)
   Requires-Dist: azureml-dataset-runtime[fuse] (~=1.11.0)
   Requires-Dist: azureml-train (~=1.11.0)
   Requires-Dist: azureml-train-automl-client (~=1.11.0)
   Requires-Dist: azureml-pipeline (~=1.11.0)
   Provides-Extra: accel-models
   Requires-Dist: azureml-accel-models (~=1.11.0); extra == 'accel-models'
   Provides-Extra: automl
   Requires-Dist: azureml-train-automl (~=1.11.0); extra == 'automl'


Lines that use ``Requires-Dist`` are similar to ``install_requires``.
Lines that use ``Provides-Extra`` are similar to ``extra_requires``,
and you can add a variant for those dependencies. The ``~=1.11.0``
syntax is equivalent to ``1.11.0:1.11.999``.

""""""""""
setuptools
""""""""""

Setuptools is a bit of a special case. If a package requires setuptools
at run-time, how do they express this? They could add it to
``install_requires``, but setuptools is imported long before this and is
needed to read this line. And since you can't install the package
without setuptools, the developers assume that setuptools will already
be there, so they never mention when it is required. We don't want to
add run-time dependencies if they aren't needed, so you need to
determine whether or not setuptools is needed. Grep the installation
directory for any files containing a reference to ``setuptools`` or
``pkg_resources``. Both modules come from ``py-setuptools``.
``pkg_resources`` is particularly common in scripts found in
``prefix/bin``.

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Passing arguments to setup.py
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The default build and install phases should be sufficient to install
most packages. However, you may want to pass additional flags to
either phase.

You can view the available options for a particular phase with:

.. code-block:: console

   $ python setup.py <phase> --help


Each phase provides a ``<phase_args>`` function that can be used to
pass arguments to that phase. For example,
`py-numpy <https://github.com/spack/spack/blob/develop/var/spack/repos/builtin/packages/py-numpy/package.py>`_
adds:

.. code-block:: python

   def build_args(self, spec, prefix):
       args = []

       # From NumPy 1.10.0 on it's possible to do a parallel build.
       if self.version >= Version('1.10.0'):
           # But Parallel build in Python 3.5+ is broken.  See:
           # https://github.com/spack/spack/issues/7927
           # https://github.com/scipy/scipy/issues/7112
           if spec['python'].version < Version('3.5'):
               args = ['-j', str(make_jobs)]

       return args


^^^^^^^
Testing
^^^^^^^

``PythonPackage`` provides a couple of options for testing packages
both during and after the installation process.

""""""""""""
Import tests
""""""""""""

Just because a package successfully built does not mean that it built
correctly. The most reliable test of whether or not the package was
correctly installed is to attempt to import all of the modules that
get installed. To get a list of modules, run the following command
in the source directory:

.. code-block:: console

   $ python
   >>> import setuptools
   >>> setuptools.find_packages()
   ['numpy', 'numpy._build_utils', 'numpy.compat', 'numpy.core', 'numpy.distutils', 'numpy.doc', 'numpy.f2py', 'numpy.fft', 'numpy.lib', 'numpy.linalg', 'numpy.ma', 'numpy.matrixlib', 'numpy.polynomial', 'numpy.random', 'numpy.testing', 'numpy.core.code_generators', 'numpy.distutils.command', 'numpy.distutils.fcompiler']


Large, complex packages like ``numpy`` will return a long list of
packages, while other packages like ``six`` will return an empty list.
``py-six`` installs a single ``six.py`` file. In Python packaging lingo,
a "package" is a directory containing files like:

.. code-block:: none

   foo/__init__.py
   foo/bar.py
   foo/baz.py


whereas a "module" is a single Python file.

The ``PythonPackage`` base class automatically detects these module
names for you. If, for whatever reason, the module names detected
are wrong, you can provide the names yourself by overriding
``import_modules`` like so:

.. code-block:: python

   import_modules = ['six']


Sometimes the list of module names to import depends on how the
package was built. For example, the ``py-pyyaml`` package has a
``+libyaml`` variant that enables the build of a faster optimized
version of the library. If the user chooses ``~libyaml``, only the
``yaml`` library will be importable. If the user chooses ``+libyaml``,
both the ``yaml`` and ``yaml.cyaml`` libraries will be available.
This can be expressed like so:

.. code-block:: python

   @property
   def import_modules(self):
       modules = ['yaml']

       if '+libyaml' in self.spec:
           modules.append('yaml.cyaml')

       return modules


These tests often catch missing dependencies and non-RPATHed
libraries. Make sure not to add modules/packages containing the word
"test", as these likely won't end up in the installation directory,
or may require test dependencies like pytest to be installed.

Import tests can be run during the installation using ``spack install
--test=root`` or at any time after the installation using
``spack test run``.

""""""""""
Unit tests
""""""""""

The package may have its own unit or regression tests. Spack can
run these tests during the installation by adding phase-appropriate
test methods.

For example, ``py-numpy`` adds the following as a check to run 
after the ``install`` phase:

.. code-block:: python

   @run_after('install')
   @on_package_attributes(run_tests=True)
   def install_test(self):
       with working_dir('spack-test', create=True):
           python('-c', 'import numpy; numpy.test("full", verbose=2)')


when testing is enabled during the installation (i.e., ``spack install
--test=root``).

.. note::

   Additional information is available on :ref:`install phase tests
   <install_phase-tests>`.

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Setup file in a sub-directory
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In order to be compatible with package managers like ``pip``, the package
is required to place its ``setup.py`` in the root of the tarball. However,
not every Python package cares about ``pip`` or PyPI. If you are installing
a package that is not hosted on PyPI, you may find that it places its
``setup.py`` in a sub-directory. To handle this, add the directory containing
``setup.py`` to the package like so:

.. code-block:: python

   build_directory = 'source'


^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Alternate names for setup.py
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

As previously mentioned, packages need to call their setup script ``setup.py``
in order to be compatible with package managers like ``pip``. However, some
packages like
`py-meep <https://github.com/spack/spack/blob/develop/var/spack/repos/builtin/packages/py-meep/package.py>`_  and
`py-adios <https://github.com/spack/spack/blob/develop/var/spack/repos/builtin/packages/py-adios/package.py>`_
come with multiple setup scripts, one for a serial build and another for a
parallel build. You can override the default name to use like so:

.. code-block:: python

   def setup_file(self):
       return 'setup-mpi.py' if '+mpi' in self.spec else 'setup.py'


^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
PythonPackage vs. packages that use Python
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

There are many packages that make use of Python, but packages that depend
on Python are not necessarily ``PythonPackage``'s.

"""""""""""""""""""""""
Choosing a build system
"""""""""""""""""""""""

First of all, you need to select a build system. ``spack create`` usually
does this for you, but if for whatever reason you need to do this manually,
choose ``PythonPackage`` if and only if the package contains a ``setup.py``
file.

"""""""""""""""""""""""
Choosing a package name
"""""""""""""""""""""""

Selecting the appropriate package name is a little more complicated
than choosing the build system. By default, ``spack create`` will
prepend ``py-`` to the beginning of the package name if it detects
that the package uses the ``PythonPackage`` build system. However, there
are occasionally packages that use ``PythonPackage`` that shouldn't
start with ``py-``. For example:

* awscli
* aws-parallelcluster
* busco
* easybuild
* httpie
* mercurial
* scons
* snakemake

The thing these packages have in common is that they are command-line
tools that just so happen to be written in Python. Someone who wants
to install ``mercurial`` with Spack isn't going to realize that it is
written in Python, and they certainly aren't going to assume the package
is called ``py-mercurial``. For this reason, we manually renamed the
package to ``mercurial``.

Likewise, there are occasionally packages that don't use the
``PythonPackage`` build system but should still be prepended with ``py-``.
For example:

* py-genders
* py-py2cairo
* py-pygobject
* py-pygtk
* py-pyqt
* py-pyserial
* py-sip
* py-xpyb

These packages are primarily used as Python libraries, not as
command-line tools. You may see C/C++ packages that have optional
Python language-bindings, such as:

* antlr
* cantera
* conduit
* pagmo
* vtk

Don't prepend these kind of packages with ``py-``. When in doubt,
think about how this package will be used. Is it primarily a Python
library that will be imported in other Python scripts? Or is it a
command-line tool, or C/C++/Fortran program with optional Python
modules? The former should be prepended with ``py-``, while the
latter should not.

""""""""""""""""""""""
extends vs. depends_on
""""""""""""""""""""""

This is very similar to the naming dilemma above, with a slight twist.
As mentioned in the :ref:`Packaging Guide <packaging_extensions>`,
``extends`` and ``depends_on`` are very similar, but ``extends`` adds
the ability to *activate* the package. Activation involves symlinking
everything in the installation prefix of the package to the installation
prefix of Python. This allows the user to import a Python module without
having to add that module to ``PYTHONPATH``.

When deciding between ``extends`` and ``depends_on``, the best rule of
thumb is to check the installation prefix. If Python libraries are
installed to ``prefix/lib/python2.7/site-packages`` (where 2.7 is the
MAJOR.MINOR version of Python you used to install the package), then
you should use ``extends``. If Python libraries are installed elsewhere
or the only files that get installed reside in ``prefix/bin``, then
don't use ``extends``, as symlinking the package wouldn't be useful.

^^^^^^^^^^^^^^^^^^^^^
Alternatives to Spack
^^^^^^^^^^^^^^^^^^^^^

PyPI has hundreds of thousands of packages that are not yet in Spack,
and ``pip`` may be a perfectly valid alternative to using Spack. The
main advantage of Spack over ``pip`` is its ability to compile
non-Python dependencies. It can also build cythonized versions of a
package or link to an optimized BLAS/LAPACK library like MKL,
resulting in calculations that run orders of magnitudes faster.
Spack does not offer a significant advantage over other python-management
systems for installing and using tools like flake8 and sphinx.
But if you need packages with non-Python dependencies like
numpy and scipy, Spack will be very valuable to you.

Anaconda is another great alternative to Spack, and comes with its own
``conda`` package manager. Like Spack, Anaconda is capable of compiling
non-Python dependencies. Anaconda contains many Python packages that
are not yet in Spack, and Spack contains many Python packages that are
not yet in Anaconda. The main advantage of Spack over Anaconda is its
ability to choose a specific compiler and BLAS/LAPACK or MPI library.
Spack also has better platform support for supercomputers, and can build
optimized binaries for your specific microarchitecture. On the other hand,
Anaconda offers Windows support.

^^^^^^^^^^^^^^^^^^^^^^
External documentation
^^^^^^^^^^^^^^^^^^^^^^

For more information on Python packaging, see:
https://packaging.python.org/
