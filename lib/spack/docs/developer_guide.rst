.. Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
   Spack Project Developers. See the top-level COPYRIGHT file for details.

   SPDX-License-Identifier: (Apache-2.0 OR MIT)

.. _developer_guide:

===============
Developer Guide
===============

This guide is intended for people who want to work on Spack itself.
If you just want to develop packages, see the :ref:`packaging-guide`.

It is assumed that you've read the :ref:`basic-usage` and
:ref:`packaging-guide` sections, and that you're familiar with the
concepts discussed there.  If you're not, we recommend reading those
first.

--------
Overview
--------

Spack is designed with three separate roles in mind:

#. **Users**, who need to install software *without* knowing all the
   details about how it is built.
#. **Packagers** who know how a particular software package is
   built and encode this information in package files.
#. **Developers** who work on Spack, add new features, and try to
   make the jobs of packagers and users easier.

Users could be end users installing software in their home directory,
or administrators installing software to a shared directory on a
shared machine.  Packagers could be administrators who want to
automate software builds, or application developers who want to make
their software more accessible to users.

As you might expect, there are many types of users with different
levels of sophistication, and Spack is designed to accommodate both
simple and complex use cases for packages.  A user who only knows that
he needs a certain package should be able to type something simple,
like ``spack install <package name>``, and get the package that he
wants.  If a user wants to ask for a specific version, use particular
compilers, or build several versions with different configurations,
then that should be possible with a minimal amount of additional
specification.

This gets us to the two key concepts in Spack's software design:

#. **Specs**: expressions for describing builds of software, and
#. **Packages**: Python modules that build software according to a
   spec.

A package is a template for building particular software, and a spec
as a descriptor for one or more instances of that template.  Users
express the configuration they want using a spec, and a package turns
the spec into a complete build.

The obvious difficulty with this design is that users under-specify
what they want.  To build a software package, the package object needs
a *complete* specification.  In Spack, if a spec describes only one
instance of a package, then we say it is **concrete**.  If a spec
could describes many instances, (i.e. it is under-specified in one way
or another), then we say it is **abstract**.

Spack's job is to take an *abstract* spec from the user, find a
*concrete* spec that satisfies the constraints, and hand the task of
building the software off to the package object.  The rest of this
document describes all the pieces that come together to make that
happen.

-------------------
Directory Structure
-------------------

So that you can familiarize yourself with the project, we'll start
with a high level view of Spack's directory structure:

.. code-block:: none

   spack/                  <- installation root
      bin/
         spack             <- main spack executable

      etc/
         spack/            <- Spack config files.
                              Can be overridden by files in ~/.spack.

      var/
         spack/            <- build & stage directories
             repos/            <- contains package repositories
                builtin/       <- pkg repository that comes with Spack
                   repo.yaml   <- descriptor for the builtin repository
                   packages/   <- directories under here contain packages
             cache/        <- saves resources downloaded during installs

      opt/
         spack/            <- packages are installed here

      lib/
         spack/
            docs/          <- source for this documentation
            env/           <- compiler wrappers for build environment

            external/      <- external libs included in Spack distro
            llnl/          <- some general-use libraries

            spack/                <- spack module; contains Python code
               analyzers/         <- modules to run analysis on installed packages
               build_systems/     <- modules for different build systems 
               cmd/               <- each file in here is a spack subcommand
               compilers/         <- compiler description files          
               container/         <- module for spack containerize
               hooks/             <- hook modules to run at different points
               modules/           <- modules for lmod, tcl, etc.
               operating_systems/ <- operating system modules
               platforms/         <- different spack platforms
               reporters/         <- reporters like cdash, junit
               schema/            <- schemas to validate data structures
               solver/            <- the spack solver
               test/              <- unit test modules
               util/              <- common code

Spack is designed so that it could live within a `standard UNIX
directory hierarchy <http://linux.die.net/man/7/hier>`_, so ``lib``,
``var``, and ``opt`` all contain a ``spack`` subdirectory in case
Spack is installed alongside other software.  Most of the interesting
parts of Spack live in ``lib/spack``.

Spack has *one* directory layout and there is no install process.
Most Python programs don't look like this (they use distutils, ``setup.py``,
etc.) but we wanted to make Spack *very* easy to use.  The simple layout
spares users from the need to install Spack into a Python environment.
Many users don't have write access to a Python installation, and installing
an entire new instance of Python to bootstrap Spack would be very complicated.
Users should not have to install a big, complicated package to
use the thing that's supposed to spare them from the details of big,
complicated packages.  The end result is that Spack works out of the
box: clone it and add ``bin`` to your PATH and you're ready to go.

--------------
Code Structure
--------------

This section gives an overview of the various Python modules in Spack,
grouped by functionality.

^^^^^^^^^^^^^^^^^^^^^^^
Package-related modules
^^^^^^^^^^^^^^^^^^^^^^^

:mod:`spack.package`
  Contains the :class:`Package <spack.package.Package>` class, which
  is the superclass for all packages in Spack.  Methods on ``Package``
  implement all phases of the :ref:`package lifecycle
  <package-lifecycle>` and manage the build process.

:mod:`spack.packages`
  Contains all of the packages in Spack and methods for managing them.
  Functions like :func:`packages.get <spack.packages.get>` and
  :func:`class_name_for_package_name
  <packages.class_name_for_package_name>` handle mapping package module
  names to class names and dynamically instantiating packages by name
  from module files.

:mod:`spack.relations`
  *Relations* are relationships between packages, like
  :func:`depends_on <spack.relations.depends_on>` and :func:`provides
  <spack.relations.provides>`.  See :ref:`dependencies` and
  :ref:`virtual-dependencies`.

:mod:`spack.multimethod`
  Implementation of the :func:`@when <spack.multimethod.when>`
  decorator, which allows :ref:`multimethods <multimethods>` in
  packages.

^^^^^^^^^^^^^^^^^^^^
Spec-related modules
^^^^^^^^^^^^^^^^^^^^

:mod:`spack.spec`
  Contains :class:`Spec <spack.spec.Spec>` and :class:`SpecParser
  <spack.spec.SpecParser>`. Also implements most of the logic for
  normalization and concretization of specs.

:mod:`spack.parse`
  Contains some base classes for implementing simple recursive descent
  parsers: :class:`Parser <spack.parse.Parser>` and :class:`Lexer
  <spack.parse.Lexer>`.  Used by :class:`SpecParser
  <spack.spec.SpecParser>`.

:mod:`spack.concretize`
  Contains :class:`DefaultConcretizer
  <spack.concretize.DefaultConcretizer>` implementation, which allows
  site administrators to change Spack's :ref:`concretization-policies`.

:mod:`spack.version`
  Implements a simple :class:`Version <spack.version.Version>` class
  with simple comparison semantics.  Also implements
  :class:`VersionRange <spack.version.VersionRange>` and
  :class:`VersionList <spack.version.VersionList>`.  All three are
  comparable with each other and offer union and intersection
  operations.  Spack uses these classes to compare versions and to
  manage version constraints on specs.  Comparison semantics are
  similar to the ``LooseVersion`` class in ``distutils`` and to the
  way RPM compares version strings.

:mod:`spack.compilers`
  Submodules contains descriptors for all valid compilers in Spack.
  This is used by the build system to set up the build environment.

  .. warning::

     Not yet implemented.  Currently has two compiler descriptions,
     but compilers aren't fully integrated with the build process
     yet.

:mod:`spack.architecture`
  :func:`architecture.sys_type <spack.architecture.sys_type>` is used
  to determine the host architecture while building.

  .. warning::

     Not yet implemented.  Should eventually have architecture
     descriptions for cross-compiling.

^^^^^^^^^^^^^^^^^
Build environment
^^^^^^^^^^^^^^^^^

:mod:`spack.stage`
  Handles creating temporary directories for builds.

:mod:`spack.compilation`
  This contains utility functions used by the compiler wrapper script,
  ``cc``.

:mod:`spack.directory_layout`
  Classes that control the way an installation directory is laid out.
  Create more implementations of this to change the hierarchy and
  naming scheme in ``$spack_prefix/opt``

^^^^^^^^^^^^^^^^^
Spack Subcommands
^^^^^^^^^^^^^^^^^

:mod:`spack.cmd`
  Each module in this package implements a Spack subcommand.  See
  :ref:`writing commands <writing-commands>` for details.

^^^^^^^^^^
Unit tests
^^^^^^^^^^

:mod:`spack.test`
  Implements Spack's test suite.  Add a module and put its name in
  the test suite in ``__init__.py`` to add more unit tests.

:mod:`spack.test.mock_packages`
  This is a fake package hierarchy used to mock up packages for
  Spack's test suite.

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Research and Monitoring Modules
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

:mod:`spack.monitor`
  Contains :class:`SpackMonitor <spack.monitor.SpackMonitor>`. This is accessed
  from the ``spack install`` and ``spack analyze`` commands to send build
  and package metadada up to a `Spack Monitor <https://github.com/spack/spack-monitor>`_ server. 


:mod:`spack.analyzers`
  A module folder with a :class:`AnalyzerBase <spack.analyzers.analyzer_base.AnalyzerBase>`
  that provides base functions to run, save, and (optionally) upload analysis
  results to a `Spack Monitor <https://github.com/spack/spack-monitor>`_ server.


^^^^^^^^^^^^^
Other Modules
^^^^^^^^^^^^^

:mod:`spack.url`
  URL parsing, for deducing names and versions of packages from
  tarball URLs.

:mod:`spack.error`
  :class:`SpackError <spack.error.SpackError>`, the base class for
  Spack's exception hierarchy.

:mod:`llnl.util.tty`
  Basic output functions for all of the messages Spack writes to the
  terminal.

:mod:`llnl.util.tty.color`
  Implements a color formatting syntax used by ``spack.tty``.

:mod:`llnl.util`
  In this package are a number of utility modules for the rest of
  Spack.

------------
Spec objects
------------

---------------
Package objects
---------------

Most spack commands look something like this:

#. Parse an abstract spec (or specs) from the command line,
#. *Normalize* the spec based on information in package files,
#. *Concretize* the spec according to some customizable policies,
#. Instantiate a package based on the spec, and
#. Call methods (e.g., ``install()``) on the package object.

The information in Package files is used at all stages in this
process.

Conceptually, packages are overloaded.  They contain:

-------------
Stage objects
-------------


.. _writing-analyzers:

-----------------
Writing analyzers
-----------------

To write an analyzer, you should add a new python file to the
analyzers module directory at ``lib/spack/spack/analyzers`` .
Your analyzer should be a subclass of the :class:`AnalyzerBase <spack.analyzers.analyzer_base.AnalyzerBase>`. For example, if you want
to add an analyzer class ``Myanalyzer`` you woul write to 
``spack/analyzers/myanalyzer.py`` and import and 
use the base as follows:

.. code-block:: python

    from .analyzer_base import AnalyzerBase

    class Myanalyzer(AnalyzerBase):


Note that the class name is your module file name, all lowercase
except for the first capital letter. You can  look at other analyzers in 
that analyzer directory for examples. The guide here will tell you about the basic functions needed.

^^^^^^^^^^^^^^^^^^^^^^^^^
Analyzer Output Directory
^^^^^^^^^^^^^^^^^^^^^^^^^

By default, when you run ``spack analyze run`` an analyzer output directory will
be created in your spack user directory in your ``$HOME``. The reason we output here
is because the install directory might not always be writable. 

.. code-block:: console

    ~/.spack/
      analyzers
      
Result files will be written here, organized in subfolders in the same structure
as the package, with each analyzer owning it's own subfolder. for example:


.. code-block:: console

    $ tree ~/.spack/analyzers/
    /home/spackuser/.spack/analyzers/
    └── linux-ubuntu20.04-skylake
        └── gcc-9.3.0
            └── zlib-1.2.11-sl7m27mzkbejtkrajigj3a3m37ygv4u2
                ├── environment_variables
                │   └── spack-analyzer-environment-variables.json
                ├── install_files
                │   └── spack-analyzer-install-files.json
                └── libabigail
                    └── lib
                        └── spack-analyzer-libabigail-libz.so.1.2.11.xml 


Notice that for the libabigail analyzer, since results are generated per object,
we honor the object's folder in case there are equivalently named files in 
different folders. The result files are typically written as json so they can be easily read and  uploaded in a future interaction with a monitor.


^^^^^^^^^^^^^^^^^
Analyzer Metadata
^^^^^^^^^^^^^^^^^

Your analyzer is required to have the class attributes ``name``, ``outfile``,
and ``description``. These are printed to the user with they use the subcommand
``spack analyze list-analyzers``.  Here is an example.
As we mentioned above, note that this analyzer would live in a module named
``libabigail.py`` in the analyzers folder so that the class can be discovered.


.. code-block:: python

    class Libabigail(AnalyzerBase):

        name = "libabigail"
        outfile = "spack-analyzer-libabigail.json"
        description = "Application Binary Interface (ABI) features for objects"


This means that the name and output file should be unique for your analyzer.
Note that "all" cannot be the name of an analyzer, as this key is used to indicate
that the user wants to run all analyzers.

.. _analyzer_run_function:


^^^^^^^^^^^^^^^^^^^^^^^^
An analyzer run Function
^^^^^^^^^^^^^^^^^^^^^^^^

The core of an analyzer is its ``run()`` function, which should accept no
arguments. You can assume your analyzer has the package spec of interest at ``self.spec``
and it's up to the run function to generate whatever analysis data you need,
and then return the object with a key as the analyzer name. The result data
should be a list of objects, each with a name, ``analyzer_name``, ``install_file``,
and one of ``value`` or ``binary_value``. The install file should be for a relative
path, and not the absolute path. For example, let's say we extract a metric called
``metric`` for ``bin/wget`` using our analyzer ``thebest-analyzer``. 
We might have data that looks like this:

.. code-block:: python

    result = {"name": "metric", "analyzer_name": "thebest-analyzer", "value": "1", "install_file": "bin/wget"}


We'd then return it as follows - note that they key is the analyzer name at ``self.name``.

.. code-block:: python

    return {self.name: result}

This will save the complete result to the analyzer metadata folder, as described
previously. If you want support for adding a different kind of metadata (e.g.,
not associated with an install file) then the monitor server would need to be updated
to support this first.


^^^^^^^^^^^^^^^^^^^^^^^^^
An analyzer init Function
^^^^^^^^^^^^^^^^^^^^^^^^^

If you don't need any extra dependencies or checks, you can skip defining an analyzer
init function, as the base class will handle it. Typically, it will accept
a spec, and an optional output directory (if the user does not want the default
metadata folder for analyzer results). The analyzer init function should call
it's parent init, and then do any extra checks or validation that are required to
work. For example:

.. code-block:: python

    def __init__(self, spec, dirname=None):
        super(Myanalyzer, self).__init__(spec, dirname)

        # install extra dependencies, do extra preparation and checks here


At the end of the init, you will have available to you:

 - **self.spec**: the spec object
 - **self.dirname**: an optional directory name the user as provided at init to save
 - **self.output_dir**: the analyzer metadata directory, where we save by default
 - **self.meta_dir**: the path to the package metadata directory (.spack) if you need it

And can proceed to write your analyzer.


^^^^^^^^^^^^^^^^^^^^^^^
Saving Analyzer Results
^^^^^^^^^^^^^^^^^^^^^^^

The analyzer will have ``save_result`` called, with the result object generated
to save it to the filesystem, and if the user has added the ``--monitor`` flag
to upload it to a monitor server. If your result follows an accepted result
format and you don't need to parse it further, you don't need to add this 
function to your class. However, if your result data is large or otherwise
needs additional parsing, you can define it. If you define the function, it
is useful to know about the ``output_dir`` property, which you can join
with your output file relative path of choice:

.. code-block:: python

    outfile = os.path.join(self.output_dir, "my-output-file.txt")


The directory will be provided by the ``output_dir`` property but it won't exist,
so you should create it:


.. code::block:: python

    # Create the output directory
    if not os.path.exists(self._output_dir):
        os.makedirs(self._output_dir)


If you are generating results that match to specific files in the package
install directory, you should try to maintain those paths in the case that
there are equivalently named files in different directories that would
overwrite one another. As an example of an analyzer with a custom save,
the Libabigail analyzer saves ``*.xml`` files to the analyzer metadata
folder in ``run()``, as they are either binaries, or as xml (text) would
usually be too big to pass in one request. For this reason, the files
are saved during ``run()`` and the filenames added to the result object,
and then when the result object is passed back into ``save_result()``,
we skip saving to the filesystem, and instead read the file and send
each one (separately) to the monitor:


.. code-block:: python

    def save_result(self, result, monitor=None, overwrite=False):
        """ABI results are saved to individual files, so each one needs to be
        read and uploaded. Result here should be the lookup generated in run(),
        the key is the analyzer name, and each value is the result file.
        We currently upload the entire xml as text because libabigail can't
        easily read gzipped xml, but this will be updated when it can.
        """
        if not monitor:
            return

        name = self.spec.package.name

        for obj, filename in result.get(self.name, {}).items():

            # Don't include the prefix
            rel_path = obj.replace(self.spec.prefix + os.path.sep, "")

            # We've already saved the results to file during run
            content = spack.monitor.read_file(filename)

            # A result needs an analyzer, value or binary_value, and name
            data = {"value": content, "install_file": rel_path, "name": "abidw-xml"}
            tty.info("Sending result for %s %s to monitor." % (name, rel_path))
            monitor.send_analyze_metadata(self.spec.package, {"libabigail": [data]})



Notice that this function, if you define it, requires a result object (generated by
``run()``, a monitor (if you want to send), and a boolean ``overwrite`` to be used
to check if a result exists first, and not write to it if the result exists and 
overwrite is False. Also notice that since we already saved these files to the analyzer metadata folder, we return early if a monitor isn't defined, because this function serves to send  results to the monitor. If you haven't saved anything to the analyzer metadata folder
yet, you might want to do that here. You should also use ``tty.info`` to give
the user a message of "Writing result to $DIRNAME."


.. _writing-commands:

----------------
Writing commands
----------------

Adding a new command to Spack is easy. Simply add a ``<name>.py`` file to
``lib/spack/spack/cmd/``, where ``<name>`` is the name of the subcommand.
At the bare minimum, two functions are required in this file:

^^^^^^^^^^^^^^^^^^
``setup_parser()``
^^^^^^^^^^^^^^^^^^

Unless your command doesn't accept any arguments, a ``setup_parser()``
function is required to define what arguments and flags your command takes.
See the `Argparse documentation <https://docs.python.org/2.7/library/argparse.html>`_
for more details on how to add arguments.

Some commands have a set of subcommands, like ``spack compiler find`` or
``spack module lmod refresh``. You can add subparsers to your parser to handle
this. Check out ``spack edit --command compiler`` for an example of this.

A lot of commands take the same arguments and flags. These arguments should
be defined in ``lib/spack/spack/cmd/common/arguments.py`` so that they don't
need to be redefined in multiple commands.

^^^^^^^^^^^^
``<name>()``
^^^^^^^^^^^^

In order to run your command, Spack searches for a function with the same
name as your command in ``<name>.py``. This is the main method for your
command, and can call other helper methods to handle common tasks.

Remember, before adding a new command, think to yourself whether or not this
new command is actually necessary. Sometimes, the functionality you desire
can be added to an existing command. Also remember to add unit tests for
your command. If it isn't used very frequently, changes to the rest of
Spack can cause your command to break without sufficient unit tests to
prevent this from happening.

Whenever you add/remove/rename a command or flags for an existing command,
make sure to update Spack's `Bash tab completion script
<https://github.com/adamjstewart/spack/blob/develop/share/spack/spack-completion.bash>`_.


-------------
Writing Hooks
-------------

A hook is a callback that makes it easy to design functions that run
for different events. We do this by way of defining hook types, and then
inserting them at different places in the spack code base. Whenever a hook
type triggers by way of a function call, we find all the hooks of that type,
and run them.

Spack defines hooks by way of a module at ``lib/spack/spack/hooks`` where we can define
types of hooks in the ``__init__.py``, and then python files in that folder
can use hook functions. The files are automatically parsed, so if you write
a new file for some integration (e.g., ``lib/spack/spack/hooks/myintegration.py``
you can then write hook functions in that file that will be automatically detected,
and run whenever your hook is called. This section will cover the basic kind 
of hooks, and how to write them.

^^^^^^^^^^^^^^
Types of Hooks
^^^^^^^^^^^^^^

The following hooks are currently implemented to make it easy for you,
the developer, to add hooks at different stages of a spack install or similar. 
If there is a hook that you would like and is missing, you can propose to add a new one.

"""""""""""""""""""""
``pre_install(spec)``
"""""""""""""""""""""

A ``pre_install`` hook is run within an install subprocess, directly before
the install starts. It expects a single argument of a spec, and is run in 
a multiprocessing subprocess. Note that if you see ``pre_install`` functions associated with packages these are not hooks
as we have defined them here, but rather callback functions associated with 
a package install.


""""""""""""""""""""""
``post_install(spec)``
""""""""""""""""""""""

A ``post_install`` hook is run within an install subprocess, directly after
the install finishes, but before the build stage is removed. If you
write one of these hooks, you should expect it to accept a spec as the only
argument. This is run in a multiprocessing subprocess. This ``post_install`` is
also seen in packages, but in this context not related to the hooks described
here.


""""""""""""""""""""""""""
``on_install_start(spec)``
""""""""""""""""""""""""""

This hook is run at the beginning of ``lib/spack/spack/installer.py``,
in the install function of a ``PackageInstaller``,
and importantly is not part of a build process, but before it. This is when
we have just newly grabbed the task, and are preparing to install. If you 
write a hook of this type, you should provide the spec to it.

.. code-block:: python

    def on_install_start(spec):
        """On start of an install, we want to...
        """
        print('on_install_start')
    

""""""""""""""""""""""""""""
``on_install_success(spec)``
""""""""""""""""""""""""""""

This hook is run on a successful install, and is also run inside the build
process, akin to ``post_install``. The main difference is that this hook
is run outside of the context of the stage directory, meaning after the
build stage has been removed and the user is alerted that the install was
successful. If you need to write a hook that is run on success of a particular
phase, you should use ``on_phase_success``.

""""""""""""""""""""""""""""
``on_install_failure(spec)``
""""""""""""""""""""""""""""

This hook is run given an install failure that happens outside of the build
subprocess, but somewhere in ``installer.py`` when something else goes wrong.
If you need to write a hook that is relevant to a failure within a build
process, you would want to instead use ``on_phase_failure``.


"""""""""""""""""""""""""""""""""""""""""""""""
``on_phase_success(pkg, phase_name, log_file)``
"""""""""""""""""""""""""""""""""""""""""""""""

This hook is run within the install subprocess, and specifically when a phase
successfully finishes. Since we are interested in the package, the name of
the phase, and any output from it, we require:

 - **pkg**: the package variable, which also has the attached spec at ``pkg.spec``
 - **phase_name**: the name of the phase that was successful (e.g., configure)
 - **log_file**: the path to the file with output, in case you need to inspect or otherwise interact with it.

"""""""""""""""""""""""""""""""""""""""""""""
``on_phase_error(pkg, phase_name, log_file)``
"""""""""""""""""""""""""""""""""""""""""""""

In the case of an error during a phase, we might want to trigger some event
with a hook, and this is the purpose of this particular hook. Akin to
``on_phase_success`` we require the same variables - the package that failed,
the name of the phase, and the log file where we might find errors.

"""""""""""""""""""""""""""""""""
``on_analyzer_save(pkg, result)``
"""""""""""""""""""""""""""""""""

After an analyzer has saved some result for a package, this hook is called,
and it provides the package that we just ran the analysis for, along with
the loaded result. Typically, a result is structured to have the name
of the analyzer as key, and the result object that is defined in detail in
:ref:`analyzer_run_function`.

.. code-block:: python

    def on_analyzer_save(pkg, result):
        """given a package and a result...
        """
        print('Do something extra with a package analysis result here')


^^^^^^^^^^^^^^^^^^^^^^
Adding a New Hook Type
^^^^^^^^^^^^^^^^^^^^^^

Adding a new hook type is very simple!  In ``lib/spack/spack/hooks/__init__.py``
you can simply create a new ``HookRunner`` that is named to match your new hook.
For example, let's say you want to add a new hook called ``post_log_write``
to trigger after anything is written to a logger. You would add it as follows:

.. code-block:: python

    # pre/post install and run by the install subprocess
    pre_install = HookRunner('pre_install')
    post_install = HookRunner('post_install')

    # hooks related to logging
    post_log_write = HookRunner('post_log_write') # <- here is my new hook! 
    

You then need to decide what arguments my hook would expect. Since this is
related to logging, let's say that you want a message and level. That means
that when you add a python file to the ``lib/spack/spack/hooks``
folder with one or more callbacks intended to be triggered by this hook. You might
use my new hook as follows:

.. code-block:: python

    def post_log_write(message, level):
        """Do something custom with the messsage and level every time we write
        to the log
        """
        print('running post_log_write!')


To use the hook, we would call it as follows somewhere in the logic to do logging.
In this example, we use it outside of a logger that is already defined:

.. code-block:: python

    import spack.hooks

    # We do something here to generate a logger and message
    spack.hooks.post_log_write(message, logger.level)


This is not to say that this would be the best way to implement an integration
with the logger (you'd probably want to write a custom logger, or you could
have the hook defined within the logger) but serves as an example of writing a hook. 

----------
Unit tests
----------

------------
Unit testing
------------

------------------
Developer commands
------------------

.. _cmd-spack-doc:

^^^^^^^^^^^^^
``spack doc``
^^^^^^^^^^^^^

^^^^^^^^^^^^^^^^^^^
``spack unit-test``
^^^^^^^^^^^^^^^^^^^

See the :ref:`contributor guide section <cmd-spack-unit-test>` on
``spack unit-test``.

.. _cmd-spack-python:

^^^^^^^^^^^^^^^^
``spack python``
^^^^^^^^^^^^^^^^

``spack python`` is a command that lets you import and debug things as if
you were in a Spack interactive shell. Without any arguments, it is similar
to a normal interactive Python shell, except you can import spack and any
other Spack modules:

.. code-block:: console

   $ spack python
   Spack version 0.10.0
   Python 2.7.13, Linux x86_64
   >>> from spack.version import Version
   >>> a = Version('1.2.3')
   >>> b = Version('1_2_3')
   >>> a == b
   True
   >>> c = Version('1.2.3b')
   >>> c > a
   True
   >>>

If you prefer using an IPython interpreter, given that IPython is installed
you can specify the interpreter with ``-i``:

.. code-block:: console

   $ spack python -i ipython
   Python 3.8.3 (default, May 19 2020, 18:47:26)
   Type 'copyright', 'credits' or 'license' for more information
   IPython 7.17.0 -- An enhanced Interactive Python. Type '?' for help.


   Spack version 0.16.0
   Python 3.8.3, Linux x86_64

   In [1]:


With either interpreter you can run a single command:

.. code-block:: console

   $ spack python -c 'import distro; distro.linux_distribution()'
   ('Ubuntu', '18.04', 'Bionic Beaver')

   $ spack python -i ipython -c 'import distro; distro.linux_distribution()'
   Out[1]: ('Ubuntu', '18.04', 'Bionic Beaver')

or a file:

.. code-block:: console

   $ spack python ~/test_fetching.py
   $ spack python -i ipython ~/test_fetching.py

just like you would with the normal ``python`` command.


.. _cmd-spack-url:

^^^^^^^^^^^^^
``spack url``
^^^^^^^^^^^^^

A package containing a single URL can be used to download several different
versions of the package. If you've ever wondered how this works, all of the
magic is in :mod:`spack.url`. This module contains methods for extracting
the name and version of a package from its URL. The name is used by
``spack create`` to guess the name of the package. By determining the version
from the URL, Spack can replace it with other versions to determine where to
download them from.

The regular expressions in ``parse_name_offset`` and ``parse_version_offset``
are used to extract the name and version, but they aren't perfect. In order
to debug Spack's URL parsing support, the ``spack url`` command can be used.

"""""""""""""""""""
``spack url parse``
"""""""""""""""""""

If you need to debug a single URL, you can use the following command:

.. command-output:: spack url parse http://cache.ruby-lang.org/pub/ruby/2.2/ruby-2.2.0.tar.gz

You'll notice that the name and version of this URL are correctly detected,
and you can even see which regular expressions it was matched to. However,
you'll notice that when it substitutes the version number in, it doesn't
replace the ``2.2`` with ``9.9`` where we would expect ``9.9.9b`` to live.
This particular package may require a ``list_url`` or ``url_for_version``
function.

This command also accepts a ``--spider`` flag. If provided, Spack searches
for other versions of the package and prints the matching URLs.

""""""""""""""""""
``spack url list``
""""""""""""""""""

This command lists every URL in every package in Spack. If given the
``--color`` and ``--extrapolation`` flags, it also colors the part of
the string that it detected to be the name and version. The
``--incorrect-name`` and ``--incorrect-version`` flags can be used to
print URLs that were not being parsed correctly.

"""""""""""""""""""""
``spack url summary``
"""""""""""""""""""""

This command attempts to parse every URL for every package in Spack
and prints a summary of how many of them are being correctly parsed.
It also prints a histogram showing which regular expressions are being
matched and how frequently:

.. command-output:: spack url summary

This command is essential for anyone adding or changing the regular
expressions that parse names and versions. By running this command
before and after the change, you can make sure that your regular
expression fixes more packages than it breaks.

---------
Profiling
---------

Spack has some limited built-in support for profiling, and can report
statistics using standard Python timing tools.  To use this feature,
supply ``--profile`` to Spack on the command line, before any subcommands.

.. _spack-p:

^^^^^^^^^^^^^^^^^^^
``spack --profile``
^^^^^^^^^^^^^^^^^^^

``spack --profile`` output looks like this:

.. command-output:: spack --profile graph hdf5
   :ellipsis: 25

The bottom of the output shows the top most time consuming functions,
slowest on top.  The profiling support is from Python's built-in tool,
`cProfile
<https://docs.python.org/2/library/profile.html#module-cProfile>`_.

.. _releases:

--------
Releases
--------

This section documents Spack's release process. It is intended for
project maintainers, as the tasks described here require maintainer
privileges on the Spack repository. For others, we hope this section at
least provides some insight into how the Spack project works.

.. _release-branches:

^^^^^^^^^^^^^^^^
Release branches
^^^^^^^^^^^^^^^^

There are currently two types of Spack releases: :ref:`major releases
<major-releases>` (``0.13.0``, ``0.14.0``, etc.) and :ref:`point releases
<point-releases>` (``0.13.1``, ``0.13.2``, ``0.13.3``, etc.). Here is a
diagram of how Spack release branches work::

    o    branch: develop  (latest version)
    |
    o    merge v0.14.1 into develop
    |\
    | o  branch: releases/v0.14, tag: v0.14.1
    o |  merge v0.14.0 into develop
    |\|
    | o  tag: v0.14.0
    |/
    o    merge v0.13.2 into develop
    |\
    | o  branch: releases/v0.13, tag: v0.13.2
    o |  merge v0.13.1 into develop
    |\|
    | o  tag: v0.13.1
    o |  merge v0.13.0 into develop
    |\|
    | o  tag: v0.13.0
    o |
    | o
    |/
    o

The ``develop`` branch has the latest contributions, and nearly all pull
requests target ``develop``.

Each Spack release series also has a corresponding branch, e.g.
``releases/v0.14`` has ``0.14.x`` versions of Spack, and
``releases/v0.13`` has ``0.13.x`` versions. A major release is the first
tagged version on a release branch. Minor releases are back-ported from
develop onto release branches. This is typically done by cherry-picking
bugfix commits off of ``develop``.

To avoid version churn for users of a release series, minor releases
**should not** make changes that would change the concretization of
packages. They should generally only contain fixes to the Spack core.
However, sometimes priorities are such that new functionality needs to
be added to a minor release.

Both major and minor releases are tagged. After each release, we merge
the release branch back into ``develop`` so that the version bump and any
other release-specific changes are visible in the mainline. As a
convenience, we also tag the latest release as ``releases/latest``,
so that users can easily check it out to get the latest
stable version. See :ref:`merging-releases` for more details.

^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Scheduling work for releases
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

We schedule work for releases by creating `GitHub projects
<https://github.com/spack/spack/projects>`_. At any time, there may be
several open release projects. For example, below are two releases (from
some past version of the page linked above):

.. image:: images/projects.png

This image shows one release in progress for ``0.15.1`` and another for
``0.16.0``. Each of these releases has a project board containing issues
and pull requests. GitHub shows a status bar with completed work in
green, work in progress in purple, and work not started yet in gray, so
it's fairly easy to see progress.

Spack's project boards are not firm commitments so we move work between
releases frequently. If we need to make a release and some tasks are not
yet done, we will simply move them to the next minor or major release, rather
than delaying the release to complete them.

For more on using GitHub project boards, see `GitHub's documentation
<https://docs.github.com/en/github/managing-your-work-on-github/about-project-boards>`_.


.. _major-releases:

^^^^^^^^^^^^^^^^^^^^^
Making major releases
^^^^^^^^^^^^^^^^^^^^^

Assuming a project board has already been created and all required work
completed, the steps to make the major release are:

#. Create two new project boards:

   * One for the next major release
   * One for the next point release

#. Move any optional tasks that are not done to one of the new project boards.

   In general, small bugfixes should go to the next point release. Major
   features, refactors, and changes that could affect concretization should
   go in the next major release.

#. Create a branch for the release, based on ``develop``:

   .. code-block:: console

      $ git checkout -b releases/v0.15 develop

   For a version ``vX.Y.Z``, the branch's name should be
   ``releases/vX.Y``. That is, you should create a ``releases/vX.Y``
   branch if you are preparing the ``X.Y.0`` release.

#. Bump the version in ``lib/spack/spack/__init__.py``.

   See `this example from 0.13.0
   <https://github.com/spack/spack/commit/8eeb64096c98b8a43d1c587f13ece743c864fba9>`_

#. Update ``CHANGELOG.md`` with major highlights in bullet form.

   Use proper markdown formatting, like `this example from 0.15.0
   <https://github.com/spack/spack/commit/d4bf70d9882fcfe88507e9cb444331d7dd7ba71c>`_.

#. Push the release branch to GitHub.

#. Make sure CI passes on the release branch, including:

   * Regular unit tests
   * Build tests
   * The E4S pipeline at `gitlab.spack.io <https://gitlab.spack.io>`_

   If CI is not passing, submit pull requests to ``develop`` as normal
   and keep rebasing the release branch on ``develop`` until CI passes.

#. Follow the steps in :ref:`publishing-releases`.

#. Follow the steps in :ref:`merging-releases`.

#. Follow the steps in :ref:`announcing-releases`.


.. _point-releases:

^^^^^^^^^^^^^^^^^^^^^
Making point releases
^^^^^^^^^^^^^^^^^^^^^

Assuming a project board has already been created and all required work
completed, the steps to make the point release are:

#. Create a new project board for the next point release.

#. Move any optional tasks that are not done to the next project board.

#. Check out the release branch (it should already exist).

    For the ``X.Y.Z`` release, the release branch is called ``releases/vX.Y``.
    For ``v0.15.1``, you would check out ``releases/v0.15``:

   .. code-block:: console

      $ git checkout releases/v0.15

#. Cherry-pick each pull request in the ``Done`` column of the release
   project board onto the release branch.

   This is **usually** fairly simple since we squash the commits from the
   vast majority of pull requests. That means there is only one commit
   per pull request to cherry-pick. For example, `this pull request
   <https://github.com/spack/spack/pull/15777>`_ has three commits, but
   they were squashed into a single commit on merge. You can see the
   commit that was created here:

   .. image:: images/pr-commit.png

   You can easily cherry pick it like this (assuming you already have the
   release branch checked out):

   .. code-block:: console

      $ git cherry-pick 7e46da7

   For pull requests that were rebased (or not squashed), you'll need to
   cherry-pick each associated commit individually.

   .. warning::

      It is important to cherry-pick commits in the order they happened,
      otherwise you can get conflicts while cherry-picking. When
      cherry-picking onto a point release, look at the merge date,
      **not** the number of the pull request or the date it was opened.

      Sometimes you may **still** get merge conflicts even if you have
      cherry-picked all the commits in order. This generally means there
      is some other intervening pull request that the one you're trying
      to pick depends on. In these cases, you'll need to make a judgment
      call regarding those pull requests.  Consider the number of affected
      files and or the resulting differences.

      1. If the dependency changes are small, you might just cherry-pick it,
         too. If you do this, add the task to the release board.

      2. If the changes are large, then you may decide that this fix is not
         worth including in a point release, in which case you should remove
         the task from the release project.

      3. You can always decide to manually back-port the fix to the release
         branch if neither of the above options makes sense, but this can
         require a lot of work. It's seldom the right choice.

#. Bump the version in ``lib/spack/spack/__init__.py``.

   See `this example from 0.14.1
   <https://github.com/spack/spack/commit/ff0abb9838121522321df2a054d18e54b566b44a>`_.

#. Update ``CHANGELOG.md`` with a list of the changes.

   This is typically a summary of the commits you cherry-picked onto the
   release branch. See `the changelog from 0.14.1
   <https://github.com/spack/spack/commit/ff0abb9838121522321df2a054d18e54b566b44a>`_.

#. Push the release branch to GitHub.

#. Make sure CI passes on the release branch, including:

   * Regular unit tests
   * Build tests
   * The E4S pipeline at `gitlab.spack.io <https://gitlab.spack.io>`_

   If CI does not pass, you'll need to figure out why, and make changes
   to the release branch until it does. You can make more commits, modify
   or remove cherry-picked commits, or cherry-pick **more** from
   ``develop`` to make this happen.

#. Follow the steps in :ref:`publishing-releases`.

#. Follow the steps in :ref:`merging-releases`.

#. Follow the steps in :ref:`announcing-releases`.


.. _publishing-releases:

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Publishing a release on GitHub
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

#. Create the release in GitHub.

   * Go to 
     `github.com/spack/spack/releases <https://github.com/spack/spack/releases>`_
     and click ``Draft a new release``.

   * Set ``Tag version`` to the name of the tag that will be created.

     The name should start with ``v`` and contain *all three*
     parts of the version (e.g. ``v0.15.0`` or ``v0.15.1``).

   * Set ``Target`` to the ``releases/vX.Y`` branch (e.g., ``releases/v0.15``).

   * Set ``Release title`` to ``vX.Y.Z`` to match the tag (e.g., ``v0.15.1``).

   * Paste the latest release markdown from your ``CHANGELOG.md`` file as the text.

   * Save the draft so you can keep coming back to it as you prepare the release.

#. When you are ready to finalize the release, click ``Publish release``.

#. Immediately after publishing, go back to
   `github.com/spack/spack/releases
   <https://github.com/spack/spack/releases>`_ and download the
   auto-generated ``.tar.gz`` file for the release. It's the ``Source
   code (tar.gz)`` link.

#. Click ``Edit`` on the release you just made and attach the downloaded
   release tarball as a binary. This does two things:

   #. Makes sure that the hash of our releases does not change over time.

      GitHub sometimes annoyingly changes the way they generate tarballs
      that can result in the hashes changing if you rely on the
      auto-generated tarball links.

   #. Gets download counts on releases visible through the GitHub API.

      GitHub tracks downloads of artifacts, but *not* the source
      links. See the `releases
      page <https://api.github.com/repos/spack/spack/releases>`_ and search
      for ``download_count`` to see this.

#. Go to `readthedocs.org <https://readthedocs.org/projects/spack>`_ and
   activate the release tag.

   This builds the documentation and makes the released version
   selectable in the versions menu.


.. _merging-releases:

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Updating `releases/latest` and `develop`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If the new release is the **highest** Spack release yet, you should
also tag it as ``releases/latest``. For example, suppose the highest
release is currently ``0.15.3``:

* If you are releasing ``0.15.4`` or ``0.16.0``, then you should tag
  it with ``releases/latest``, as these are higher than ``0.15.3``.

* If you are making a new release of an **older** major version of
  Spack, e.g. ``0.14.4``, then you should not tag it as
  ``releases/latest`` (as there are newer major versions).

To tag ``releases/latest``, do this:

.. code-block:: console

   $ git checkout releases/vX.Y     # vX.Y is the new release's branch
   $ git tag --force releases/latest
   $ git push --force --tags

The ``--force`` argument to ``git tag`` makes ``git`` overwrite the existing
``releases/latest`` tag with the new one.

We also merge each release that we tag as ``releases/latest`` into ``develop``.
Make sure to do this with a merge commit:

.. code-block:: console

   $ git checkout develop
   $ git merge --no-ff -s ours vX.Y.Z  # vX.Y.Z is the new release's tag
   $ git push

We merge back to ``develop`` because it:

  * updates the version and ``CHANGELOG.md`` on ``develop``; and
  * ensures that your release tag is reachable from the head of
    ``develop``.

We *must* use a real merge commit (via the ``--no-ff`` option) to
ensure that the release tag is reachable from the tip of ``develop``.
This is necessary for ``spack -V`` to work properly -- it uses ``git
describe --tags`` to find the last reachable tag in the repository and
reports how far we are from it. For example:

.. code-block:: console

   $ spack -V
   0.14.2-1486-b80d5e74e5

This says that we are at commit ``b80d5e74e5``, which is 1,486 commits
ahead of the ``0.14.2`` release.

We put this step last in the process because it's best to do it only once
the release is complete and tagged. If you do it before you've tagged the
release and later decide you want to tag some later commit, you'll need
to merge again.


.. _announcing-releases:

^^^^^^^^^^^^^^^^^^^^
Announcing a release
^^^^^^^^^^^^^^^^^^^^

We announce releases in all of the major Spack communication channels.
Publishing the release takes care of GitHub. The remaining channels are
Twitter, Slack, and the mailing list. Here are the steps:

#. Announce the release on Twitter.

   * Compose the tweet on the ``@spackpm`` account per the
     ``spack-twitter`` slack channel.

   * Be sure to include a link to the release's page on GitHub.

     You can base the tweet on `this
     example <https://twitter.com/spackpm/status/1231761858182307840>`_.

#. Announce the release on Slack.

   * Compose a message in the ``#general`` Slack channel
     (`spackpm.slack.com <https://spackpm.slack.com>`_).

   * Preface the message with ``@channel`` to notify even those
     people not currently logged in.

   * Be sure to include a link to the tweet above.

   The tweet will be shown inline so that you do not have to retype
   your release announcement.

#. Announce the release on the Spack mailing list.

   * Compose an email to the Spack mailing list.

   * Be sure to include a link to the release's page on GitHub.

   * It is also helpful to include some information directly in the
     email.

   You can base your announcement on this `example
   email <https://groups.google.com/forum/#!topic/spack/WT4CT9i_X4s>`_.

Once you've completed the above steps, congratulations, you're done!
You've finished making the release!
