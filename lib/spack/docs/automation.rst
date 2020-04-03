Spack and the Effects of Automation
===================================

Spack systemetizes and automates the process of installing software on
HPC systems, resulting in huge efficiency gains.  Software
environments that would previously have taken 2-4 weeks of labor to
install by hand can now be built in 4 hours or less, with even less
(human) labor involved --- a gain of 1-2 orders of magnitude in human
effort.

Invariably, efficiency gains of such a magnitude result in a
restructuring of our work.  By way of comparison, ponder the
wide-ranging changes that took place as metropolitan transportation
transitioned from streetcar to automobile --- in response to not even
1 order of magnitude speed gain.  At first, people used automobiles to
navigate their existing environment more efficiently.  But since the
automobile made transportation so much cheaper (in time), people began
to find new ways to improve their lives in exchanged for increased
transportation use; and new ways to build their environment to
accommodate these changes.  Eventually, this process completely
transformed the ways we live, work and play.

Like the automobile, automated builders like Spack also bring large
gains in efficiency.  And as with the early automobile, many users
currently use Spack as a way to save time on their existing workflows.
But we fail to realize the full potential of Spack if we use it merely
as a drop-in replacement for manual labor.  Ultimately, Spack should
challenge our asusmptions about how we build HPC software and
restructure the way we work in this realm.  The new ways of working
will almost certainly involve more software building than before and
maybe more hard disk space taken up by software binaries.  But that is
OK.  It makes sense to "waste" cheap resources --- hard disk space,
CPU cycles --- in order to save expensive resources, i.e. human labor.

In service to that end, this article goes into detail about how we can
get the most out of Spack if we allow it to fundamentally change the
way we work.  First, it goes into detail about how software has
traditionally been installed; and then describes the workflow I use to
build customized per-project software environments.

Manual Software Installation
----------------------------

Before Spack, software was installed manually.  This was a difficult,
tedious and labor-intensive process with the following features:

* Without automation, software builds were largely unrepeatable.  Any
  "gotchas" encountered installing a particular package would have to
  be remembered if installing the same package later.

* Work was structured to avoid building software as much as possible.
  This meant building on top of as many system-provided packages as
  possible.  This has many drawbacks:

  1. Since system packages cannot depend on packages you built, it
     only works for lower levels of the DAG.  As soon as you must
     manually build a package, everything that depends on it must also
     be manually built.

  1. Forced system upgrades due to IT/security issues can break the
     application stack and force a rebuild at inopportune times.

  1. Complications are introduced if the system libraries one is
     trying to use are the wrong version, or are built with a
     different compiler than is required for the application stack.

* Software was built bottom-up; meaning, low-level dependencies were
  built before higher-level packages.  It was the job of many
  sysadmins to install multiple versions of packages that users
  *might* need: compilers, MPI, NetCDF, for example, and to provide
  environment modules to load them.  And then users were left on their
  own to finish building their software stacks on top of those
  low-level packages.  This *bottom-up thinking* was pervasive.

* Many sysadmin-provided packages were built without RPATH, requiring
  specific ``LD_LIBRARY_PATH`` settings to work properly.  Sometimes
  this was even true of compilers and the runtime environment they
  produce, causing numerous downstream headaches.

* Environment modules ended up with increasing inter-module
  dependencies, reflecting the underlying software dependencies.  This
  produced


Manual Software Installation with Spack
---------------------------------------

The introduction of Spack challenges numerous long-held assumptions of
software installation.  Ways we need to change thinking include:

1. **It is OK to install multiple versions of software.** Spack is
   very good at installing software, and hard drive space is cheap.
   We should allow Spack to re-install software as needed, as long as
   doing so requires less of our time.

1. **It is OK to rebuild your entire software stack from time to
   time.** Spack is very good at installing software.  We should aim
   to set things up so Spack can re-install our software stack in a
   repeatable fashion.  The process of producing a working Spack
   environment is therefore akin to writing code and compiling it,
   rather than manually exploring our way through the space.

1. **We need to think top-down, not bottom-up.** When we install
   software manually, we are used to reading through the requirements,
   trying to install each requirement, and then installing the final
   package.  But with Spack, we need to start with what we want
   installed; and let Spack figure out what its requirements are.
   Appropriate use of Spack Environments helps facilitate this
   approach.

   One of the most common requests / questions from new Spack users is:

   .. quote::

      I installed package *X* needed by *Y*; but now that I'm
      installing *Y*, Spack decided to rebuild *X*.  Spack should
      really re-use existing dependencies if they are already built.

    While the feature being requested is not *wrong per se*, it is
    based on some assumptions that no longer hold in a Spack universe:

    1. Spack is good at building packages, so rebuilding packages
       isn't a particularly bad thing that's worth much effort to be
       avoided.

    1. Most of the effort in building a package with Spack goes into
       getting recipe right.  If the user had to tweak the recipe to
       get *X* to build by hand; then

   That said, it is important that Spack have features (part of Spack
   Environments) that allow the user to manually explore / install
   parts of the DAG for debuggin purposes.  For this to work, the user
   must be able to attempt to install a sub-package of a DAG with the
   options and dependencies as the way Spack would do it.

1. **The role of a sysadmin needs to change to be top-down, not
   bottom-up.** In a Spack universe, having sysadmins install 32 versions
   of MPI for different compiler / MPI combinations is not so useful
   as it used to be, for many reasons:

   1. For users who don't want to use Spack, sysadmins can easily
      install combinations on-demand as needed.

   1. Users can install the package on their own, if given the right
      Spack recipes.  The ideal sysadmin would maintain such spack
      recipes appropriate for the given HPC system.

   1. For the Spack user, large amounts of time are wasted trying to
      make use of pre-built external dependencies.

   Instead of installing a pre-built set of packages with modules, in
   a Spack universe sysadmins could better spend their time on the
   following tasks:

   1. Assembling, building and QA-testing Spack Environments that
      support the needs of particular project groups.  In effect, each
      project gets is *own custom set* of software customized to its
      own needs.  Users don't need to use Spack to use these pre-built
      environments.

   1. To support users comfortable with Spack, sysadmins can also
      focus on maintaining a stable Spack fork with recipes and Spack
      Environment definitions that work in the local environment.
      Sysadmins can periodically upgrade to newer versions of Spack as
      needed, rebuilding and QA-testing group environments when they
      do so.

1. **Environment Modules are Not So Useful.** They seem like a good
   idea, in that they allow the user to load, unload and recombine
   individual software packages at will.  The problem here is that
   very few modules are truly independent, usually depending on other
   modules to work properly; and the user is not well suited to
   determine what depends on what.

   This problem has been partially addressed by "new" module systems
   such as *Lmod*, which allow for dependencies between modules and
   auto-loading of those dependencies when needed.  And some module
   systems require the user to load modules bottom-up; only showing a
   module as available to be loaded once all its dependencies are
   loaded.

   None of these approaches provide what users really need.  We need
   an environment tailored to our project, and a single shell script
   used to load / set up that environment en mass.  We don't want to
   have to get into the details of the individual packages in the
   environment.  Spack-generated environment modules that load/unload
   an entire Spack Environment would be useful for this purpose;
   Environment modules that load/unload a single node in the DAG are
   not.


Spack Environments, Step by Step
================================

Spack Environments are a key technology to unlock the transformative
automation power of Spack:

* They are a succinct and (mostly) portable description of a software
  stack that can be ported between HPC systems and installed as
  needed.

* They are the *only* way in Spack to accomplish the simple task of
  building a package and then reliably loading it.  Note that ``spack
  load`` is nondeterministic.

Therefore, Spack Environments form the cornerstone of how sysadmin
could operate in assisting project groups.  This section is a tutorial
outlining the the steps required to build and maintain one or more
Spack Environment, based on real-world examples.


Site Branch
-----------

It can be useful to maintain your own branch of Spack, for the following reasons:

1. If there are any problems in Spack that interfere with your software
   stack, you can fix them immediately; and then submit them to the
   main Spack repo as pull requests once your environment is working.

1. It allows you to maintain Spack Environment specifications for the
   Spack Environments maintained at your site.  Spack users can
   therefore simply clone your Spack branch and get everything they
   need in one place.

1. It gives you complete control over "forced upgrades" as Spack
   evolves over time.  You can choose when and how to upgrade your
   Spack recipes; and then rebuild and QA-test all relevant Spack
   environments on your system to make sure they still work.

Your own Spack branch is created as follows:

1. Go to the main `Spack Repository <https://github.com/spack/spack/>`_.

1. Press the *Fork* button in the upper-right, and follow the instructions.

1. The result is a copy of the Spack repo.  In this case, that copy is
   found `here <https://github.com/citibeth/spack>`_.

Once the repo is forked, create a new branch on it at the head of
*develop*:

.. code-block:: bash

   cd spack
   git checkout develop
   git checkout -b mybranch
   git push

See `here
<https://git-scm.com/book/en/v2/Git-Basics-Working-with-Remotes>`_ for
more information on how to keep your fork synchronized with the main
Spack repo.

Compilers
---------

Set up your *compilers.yaml* file as detailed in compiler-config_.


.. note::

   Unfortunately, this setup is not included in the Spack respoitory
and therefore cannot be checked into git.  If possible, this should be
moved into the Spack Envrionment, along with other compiler-specific
files.


External Modules
----------------

Create a blank environment:

.. code-block:: bash

   spack env create myenv

This creates an environment directory in
``spack/.../environments/myenv``.

.. note:

   Spack environemnts are generally tailored for a single HPC system.
   If you want to create an environment to run on multiple systems, it
   is probably best to include the system name in your environment
   name; for example, ``myenv-lolly``, if your HPC system is named
   *lolly*.  When you are ready to build the environment on another
   machine, you can start with ``myenv-lolly`` and make edits as
   appropriate.

Now consider which environment
modules will need to be loaded in order to make this environment work.
Typically this will be system-provided modules for your compiler, MPI,
etc.  For example:

.. code-block:: bash

   compiler/icc/2018.5.274-GCC-5.4.0-2.26
   compiler/ifort/2018.5.274-GCC-5.4.0-2.26
   openmpi/intel/3.1.4

Put these together into an initial file called ``load-x`` inside your
``myenv`` environment directory:

.. code-block:: bash

   module purge
   module load compiler/icc/2018.5.274-GCC-5.4.0-2.26
   module load compiler/ifort/2018.5.274-GCC-5.4.0-2.26
   module load openmpi/intel/3.1.4

Now ``source loads-x`` in your shell, so you have these modules
available when building your environment.


Specification
-------------

The blank environment above may now be modified by editing the file
``spack/var/spack/environments/myenv/spack.yaml``.  At this point, add
top-level packages you want to be included in the envrionment.  This
can be done using ``spack env add`` or by editing the YAML file
directly.  For example:

.. code-block:: yaml

   spack:
     view: False
     concretize_together: True
     specs:
     - spec: cmake
     - spec: netcdf-fortran
     - spec: ncview
     - spec: nco
     - spec: git
     - spec: py-giss
     - spec: py-ply
     - spec: py-psutil
     - spec: py-sphinx

.. note::

   1. `python` is not included explicitly in this environment as a
      spec.  That is OK, since the Python-related packages will
      include it as well.

   1. At this point, you can choose to set ``concretize_together: True``.
      This will cause Spack to concretize the entire environment in one
      DAG, thereby ensuring *only one* version of each package.

      * ``concretize_together` is desirable for environments meant to
        support a single project and are linked together.  It is
        analogous to typical Linux distributions, with exactly one
        version of each package.

      * In some cases, ``concretize_together`` cannot be used because
        different top-level specs require different versions of the same
        dependency.  This is rare; but can happen if the top-level specs
        are fully linked executables, not libraries for a user's project.

      * Operationally, ``concretize_together`` can make it harder to
        debug environments with the ``spack -e myenv install mypackage``
        call.

Environment Configuration
-------------------------

In the ``spack.yaml`` file above, no explicit versions or variants
were used.  The most trouble-free way to include that information is
in the Spack configuration, rather in the specs themselves.  That
information can be placed directly into the ``spack.yaml`` file.  This
is where you choose specific versions of packages, the use of external
packages, and specific choices of virtual packages, for your project.
See config-yaml_ for more details.

Simple Versions and Variants
````````````````````````````

Specific versions and variants of packages are often required, due to
requirements of the project.  Here are some examples:

.. code-block:: yaml

   spack:
       packages:
           # --------- Base Libraries
           parallel-netcdf:
               variants: [~cxx]
           eigen:
               # See http://eigen.tuxfamily.org/bz/show_bug.cgi?id=1370
               version: [3.2.10]
               variants: [~suitesparse]
           netcdf:
               version: [4.4.0]
               variants: [+mpi]
           netcdf-cxx4:
               version: [4.3.0]    # 4.3.1 does NOT work, undefined nc_def_var_filter
           # Required for NetCDF 4.4.0
           # See https://github.com/spack/spack/issues/3056
           hdf5:
               version: [1.8.18]
           # Required for PETSc; you might have to hack openmpi/package.py to make this stick
           openmpi:
               version: [3.1.0]


External Packages
`````````````````

If there are any externally compiled packages used in your project,
they are also included in the Environment Configuration.  Here is an
example for system-supplied MKL and MPI:

.. code-block:: yaml

   spack:
       packages:
           openmpi:
             paths:
               openmpi@3.1.4: /opt/scyld/openmpi/3.1.4/intel
             version: [3.1.4]   # Choose externally built version
             buildable: false
             providers: {}
             modules: {}
             compiler: []

           intel-mkl:
               paths:
                   intel-mkl@2018.4.274: /usr/local/.../mkl/lib
               version: [2018.4.274]
               buildable: False


.. note:

   1. The use of externally built software *almost always* requires
      more human effort than just letting Spack build it.  It is
      advisable only where it is not practical for Spack to build the
      package.  For example, with system or vendor-supplied libraries
      for MPI, MKL, etc.

   1. It might be necessary to add the version of your system's
      pre-installed packages to the packages' ``package.py`` recipe
      files.


Providers
`````````

Many external packages satisfy one ore more Spack virtual
dependencies, and must be selected to ensure that Spack uses them.
For example, ``openmpi`` satisfies the virtual dependency ``mpi``.
These can be selected, along with your compiler (must be dfined in
``compilers.yaml``), as follows:

.. code-block:: yaml

   spack:
       packages:
           all:
               compiler: [intel@18.5.274]
               providers:
                   mpi: [openmpi]
                   blas: [intel-mkl]
                   lapack: [intel-mkl]
                   scalapack: [intel-mkl]
                   mkl: [intel-mkl]
                   fftw-api: [intel-mkl]

Concretization and Manual Reivew
--------------------------------

Once the environment is created, it can be concretized and checked for
errors.  Concretize with:

.. code-block:: bash

   spack -e myenv concretize -f | less

If it finishes with throwing a syntax or other error, this command
prints out the result of its concretization, including whether each
package is already installed or still needs to be installed.  Check
for common errors, such as:

* Do the things you think are already installed show up as installed?

* Do you see the expected versions of key packages you set in the
  Spack Environment Configuation above?  For example, ``python``,
  ``openmpi``, ``mkl``?

If anything looks wrong, fix the relevant file, re-concretize and try
again.  It is worth the time scrutinizing the concretization *before*
you build.

.. note::

   The concretization information is also available in the
   ``spack.lock`` file.


Build the Environment
---------------------

If everything looks good in the concretization step, it's time to build:

.. code-block:: bash

   spack -e myenv install

In theory, this should go off without a hitch.  In practice, any of a
number of problems can occur.  For example:

* **Version Compatibility Problems**: Upstream authors typically test
  their packages with recent versions of their dependencies at the
  time of release, using compilers available at the time of release.
  Version compatiblity problems frequently show up if you are
  combining packages of different vintages, an old ``hdf5`` with a new
  ``netcdf``.

  Similarly, compatibility problems can happen with a
  compiler of the wrong vintage.  Newer compilers can sometimes check
  for illegal constructs that older compilers let slide; or newer
  aggressive optimization techniques can uncover latent bugs in old
  software.

  In all cases, the solution is to look up the errors you are
  encountering on-line, see what others say about them, and then
  usually tweak version numbers on packages to fix them:

  * For package incompatibility problems, upgrading to the latest
    version of everything usually works.  Sometimes this means adding
    new versions to the Spack recipes.

  * If you need to use an old version of a particular package,
    sometimes *downgrading* other pacakges in the DAG can help.

  * For compiler incompatibility problems, sometimes an older version
    of the packages must be chosen if you are using an older compiler
    and don't have access to a new one.

* **Download Problems**: Sometimes Spack is unable to download a
  tarball because the website is down.  When that happens, it is often
  possible to find the tarball by hand in an alternate location; for
  example, in a popular Linux distribution.  Just put it in
  ``spack/var/spack/cache/<project>`` and Spack will take care of the
  rest.  You must **ensure that the checksums match** by not ingoring
  / bypassing checksum problems that Spack might find in your manually
  downloaded tarballs.

  .. note::

     If you have already built this environment elsewhere, it can be
     useful to *rsync* the ``var/spack/cache`` directory from that
     location to your current location, thereby eliminating a source
     of environment build failure.


Generate the Module List Script
-------------------------------

With the environment built, now is the time to set up for users to
load it.  The file ``spack/var/spack/environments/myenv/loads`` is
created with:

.. code-block:: bash

   cd spack/var/spack/environments/myenv
   spack -e myenv env loads -r
   sort loads | uniq >loads2  # Remove duplicates
   cp loads2 loads

This generates a file ``spack/.../myenv/loads`` with a set of *module
load* commands.  For example:

.. code-block:: bash

   module load antlr-2.7.7-intel-18.5.274-wwjsgt4
   module load blitz-1.0.2-intel-18.5.274-6vkohpy
   module load boost-1.69.0-intel-18.5.274-e4fjeos
   module load bzip2-1.0.6-intel-18.5.274-zlll3y6
   module load cgal-4.12-intel-18.5.274-zxog4q7
   module load eigen-3.2.10-intel-18.5.274-haa2whc
   module load everytrace-0.2.2-intel-18.5.274-s4yf74v
   module load expat-2.2.5-intel-18.5.274-3wgaeq3
   module load fftw-3.3.8-intel-18.5.274-p4ugro5
   module load gdbm-1.18.1-intel-18.5.274-cikplom

.. note::

   1. The ``spack env loads -r`` command currently generates more than
      one ``moeule load`` command for many packages.  The ``sort``,
      ``uniq`` and ``cp`` commands above address that problem.

   1. We do not recommended the use of Spack Environment views at this
      time.  Spack views are convenient, but they are also incomplete;
      because they do not come with accompanying environment variable
      settings needed to use the view.  It is often possible for users
      to guess the correct settings; such as ``PATH=<myview>/bin``,
      etc.  But some Spack-built modules set up unique environment
      variables that are not properly "guessed" by this approach.

Update the Environment Script
-----------------------------

Edit your ``loads-x`` file again.  Insert the following at the beginning:

.. code-block:: bash

   # Figure out where we are
   export SPACK_ENV=$(readlink -f $(dirname "${BASH_SOURCE[0]}"))
   export SPACK_ENV_NAME=$(basename $SPACK_ENV)
   export SPACK_ROOT=$(dirname $(dirname $(dirname $(dirname $SPACK_ENV))))

   # Minimal Spack setup without invoking Spack's setup_env.sh stuff
   export MODULEPATH=$MODULEPATH:$SPACK_ROOT/share/spack/modules/linux-centos6-x86_64

   export PATH=$PATH:SPACK_ROOT/bin


And append the following at the end:

.. code-block:: bash

   # Load Spack-generated modules
   # For some reason, one module unsets the prompt env var PS1:
   #        intel-mkl-2018.4.274-intel-18.5.274-doboyrw
   source $SPACK_ENV/loads


Congratulations, you now have created a customized, installed Spack
Environment that can be loaded simply by invoking ``source
.../myenv/loads-x``.  Users can put this in their *.bashrc* and not have to
worry about the fact that Spack was used to generate this environment.

.. note:

   1. You should add the ``loads-x`` file to your Spack fork and check
      it in.  Do not add ``loads`` because it is machine generated, it
      can change, and it is useless without the accompanying installed
      packages anyway.

   1. If the modules referenced in ``loads`` are deleted, then
      ``source loads-x`` will generate errors.  That is OK if you are
      in the process of rebuilding the Spack Environment.


Site-Specific Fixes
-------------------

Sometimes bugs in environment modules are most easily fixed by
adjusting ``loads-x`` appropriately, after the ``source loads``
command.  Real-world examples include:

.. code-block:: bash

   # A Spack-generated module for an externally built MPI package caused
   # the command prompt to disappear!
   # ==> Before the module load commands...
   PS1_SAVE="$PS1"    # Save command prompt; some modules destroy it
   # ===> After the module load commands...
   export PS1="$PS1_SAVE"

   # Part of fixing problems with system-provided MPI.  Don't ask...
   export LD_LIBRARY_PATH=$(echo $LD_LIBRARY_PATH | sed 's@/opt/scyld/openmpi/3.1.4@/home/eafischer2/om3.1.4@g')
   export PATH=$(echo $PATH | sed 's@/opt/scyld/openmpi/3.1.4@/home/eafischer2/om3.1.4@g')

   # Add system-provided MPI to PATH so builders can find it.
   export PATH=$PATH:/home/eafischer2/om3.1.4/intel/bin

   # The PISM_BIN variable is now wrong in harness-land; so unset it
   unset PISM_BIN

The nice thing about these fixups is they never have to be general.
If *you* need it *now* on *your system*, then it works!


Add Dynamic Source Code
-----------------------

In some cases, it can be useful to download source packages and patch
them directly into your environment without have to "officially"
install them.  For example, maybe you support an in-house library of
Python code that you want to make available and maintain for your
environment users, while making it easy to do "hot fixes".  It is
convenient to download these packages directly into your environment
and then fix the ``loads-x`` file accordingly.  For example:

.. code-block:: bash

   cd spack/.../environments/myenv
   git clone https://github.com/citibeth/modele-control.git

To use this "hot fix" code in your environment, you now need to add
appropraite code to your ``loads-x`` file:

.. code-block:: bash

   # Use environment-provided source code for a few of the modules
   export PATH=$SPACK_ENV/modele-control/bin:$PATH
   export PYTHONPATH=$SPACK_ENV/modele-control/lib:$PATH



Modularizing Your Envrionment
=============================

The above example shows how to generate a *single* environment on a
*single* HPC system.  Some parts of the above can be factored out on a
per-machine or per-environment basis.

Factoring ``spack.yaml``
------------------------

Environment configuration settings can often be factored by machine or
environemnt.

* Some environment configuration options are useful for *any*
  environment on a particular machine.  For example:

   .. code-block:: yaml

      spack:
          packages:
              openmpi:
                paths:
                  openmpi@3.1.4: /opt/scyld/openmpi/3.1.4/intel
                version: [3.1.4]   # Choose externally built version
                buildable: false
                providers: {}
                modules: {}
                compiler: []

* Some environment configuration opetions are useful for a *single* environment on *any* machine.  For example:

   .. code-block:: yaml

      spack:
          packages:
              # --------- Base Libraries
              parallel-netcdf:
                  variants: [~cxx]
              eigen:
                  # See http://eigen.tuxfamily.org/bz/show_bug.cgi?id=1370
                  version: [3.2.10]
                  variants: [~suitesparse]
              netcdf:
                  version: [4.4.0]
                  variants: [+mpi]
              netcdf-cxx4:
                  version: [4.3.0]    # 4.3.1 does NOT work, undefined nc_def_var_filter
              # Required for NetCDF 4.4.0
              # See https://github.com/spack/spack/issues/3056
              hdf5:
                  version: [1.8.18]

It can be useful to factor these configuration options into
per-machine or per-environment files, and include them in the final
``spack.yaml``.  For exmaple, ``spack.yaml`` for the environment
``tw-discover12`` starts with:

.. code-block:: yaml

   spack:
     include:
     - ../configs/twoway.yaml        # Highest precedence
     - ../configs/gissversions.yaml
     - ../configs/discover12.yaml

     packages:
   ...

Meanwhile, ``spack.yaml`` for the related environment ``tw-chinook``
(the *tw* environment on the *chinook* system) starts with:

.. code-block:: yaml

   spack:
     include:
     - ../configs/twoway.yaml        # Highest precedence
     - ../configs/gissversions.yaml
     - ../configs/chinook.yaml

     packages:
   ...

Only the specific package list needs to be repeated between machines.
That could probably also be put into an *include* file as well.

Factoring ``loads-x``
---------------------

The other opportunity for factoring comes in the ``loads-x`` file.
Many of the things this file needs to do are machine-specific, and
independent of the environment being loaded on that machine.  For
example, here is the ``chinook.sh`` file used for all environments on
``chinook``:

.. code-block:: bash

   # Standard stuff for any loads-x environment on chinook

   # https://stackoverflow.com/questions/3430569/globbing-pathname-expansion-with-colon-as-separator
   function join() {
       local IFS=$1
       shift
       echo "$*"
   }

   PS1_SAVE="$PS1"    # Save command prompt; some modules destroy it

   export SPACK_ENV_NAME=$(basename $SPACK_ENV)
   export SPACK_ROOT=$(dirname $(dirname $(dirname $(dirname $SPACK_ENV))))
   # This will be overwritten when the harness is created.

   # Minimal Spack setup without invoking Spack's setup_env.sh stuff
   export MODULEPATH=$MODULEPATH:$(join ':' $SPACK_ROOT/share/spack/modules/*)

   export PATH=$PATH:SPACK_ROOT/bin

   # Load the main environment
   module purge

   # icc also loads gcc-5.4.0
   # module load compiler/GCC/5.4.0-2.26
   module load compiler/icc/2018.5.274-GCC-5.4.0-2.26
   module load compiler/ifort/2018.5.274-GCC-5.4.0-2.26
   # Needed to get the right mpicc to link to the right libraries.
   # Without this, it links to /usr/lib64/libstdc++
   module load openmpi/intel/3.1.4
   # We will build our own intel-mkl with Spack

   # Load Spack-generated modules
   # For some reason, one module unsets the prompt env var PS1:
   #        intel-mkl-2018.4.274-intel-18.5.274-doboyrw
   source $SPACK_ENV/loads
   export PS1="$PS1_SAVE"

   # We will have to replace in it
   #     '/opt/scyld/openmpi/3.1.4' --> '/home/eafischer2/om3.1.4'
   export LD_LIBRARY_PATH=$(echo $LD_LIBRARY_PATH | sed 's@/opt/scyld/openmpi/3.1.4@/home/eafischer2/om3.1.4@g')
   export PATH=$(echo $PATH | sed 's@/opt/scyld/openmpi/3.1.4@/home/eafischer2/om3.1.4@g')

   # Make sure `ectl setup` (ModelE setup; see modele-control repo) can
   # find MPI, and that we can do mpirun when needed.
   export PATH=$PATH:/home/eafischer2/om3.1.4/intel/bin/

Any ``loads-x`` file for a *chinook* environment then looks like this:

.. code-block:: bash

   # Set up Spack and Modules
   # http://stackoverflow.com/questions/59895/can-a-bash-script-tell-which-directory-it-is-stored-in
   export SPACK_ENV=$(readlink -f $(dirname "${BASH_SOURCE[0]}"))
   export HARNESS=$SPACK_ENV

   # Stuff common to all environments on chinook
   source $SPACK_ENV/../machines/chinook.sh

   # Above the line is standard for any project on chinook
   # ---------------------------------------------------
   # Below the line: specific to the this project



Multi Environments
------------------

It is also possible to factor environments by function, and then load
multiple environments in a ``loads-x`` file.  For example, suppose
that *chinook* were an old machine with obsolete versions of many
common tools --- *git*, *ssh*, etc.  These are command line tools we
might want to add to *any* user's environment on *chinook*.  The
following could be added to ``chinook.sh`` in the appropraite place to
make this happen:

.. code-block:: bash

   # Bootstrap with Spack-built replacements of system tools
   source $SPACK_ENV/../tools-discover/loads

Real-Life Modularization
------------------------

See `here <https://github.com/citibeth/spack/tree/efischer/giss2>`_ to
examine a real-life set of environments that have been prepared to run
on multiple machines.  All files are checked into the Spack fork, of
course.


Desired Principles of Spack Environments
========================================

The purpose of Spack Environments is to create environment
specifications ("source code") that can be reliably and repeatedly
built on multiple systems.  They need the following properties:


1. Spack Environments specs should be portable, just like C code is
   portable: they can be built on any system without modification.  In
   reality, that has not turned out to be the case.  Spack
   Environments typically need tweaks to manage differences between
   HPC systems, including different preferred compilers and different
   versions of pre-installed low level packages (eg MPI).  These
   differences at the lowest level drive differences higher up the
   DAG, including different required versions of certain packages.
   Therefore, the goal needs to be to construct Spack Environments
   that are short enough to be copied over from one HPC system to the
   next, and easily customized for each system.

1. The ``spack.yaml`` file is akin to "source code", and should *never*
   be overwritten by machine.  Like source code in any language, it
   should only be edited by hand --- or machine-generated and then
   edited by hand.

1. With respect to environment *myenv*, there needs to be an easy way
   to debug the environment when things go wrong.  The persona
   assembling the environment should be able to:

   1. Try to install just package *X* (and dependencies thereof) that
      is part of the *myenv* DAG(s).

   1. Try to install any package *X* (and dependencies thereof) as if
   *X* were added to the environment; but *without actually adding it
   to the environment*.

   1. When trial-installing packages, that needs to be possible by any
      of the following means:

      1. Install, akin to `spack install`.

      1. Install from pre-downloaded source, akin to `spack diy`

      1. Start a shell with the environment used to install, and allow
         the user to manually build the package, akin to `spack
         build-env`.

  1. Trial installs need to work whether or not *myenv* is concretized
   as a single DAG or multiple DAGs.  If *myenv* is concretized as a
   single DAG, the trial install should use details of the concretized
   DAG to drive concretization of the new package in a separate DAG.
   This will not always result in *exactly* the same package being
   installed as if it were officially part of the environment; but
   it's pretty close.

1. When fully built, a Spack enviornment should provide a simple way
   to access it through a shell script that can be placed in a user's
   *.bashrc* file.  Users don't want to assemble individual
   environment modules by hand.

1. When creating a Spack Harness, it should be possible to dynamically
   adjust which packages are to be built as *setup*, without
   rebuilding the Spack Environment.

1. There needs to be more flexibility in how different configuration
   *yaml* files override each other.

1. There should be a way to re-read the ``spack.lock`` file and print
   out the concretization information as originally printed with the
   ``spack env concretize`` command.

1. Fix Spack Environment Views so they are as functional as using
   Spack Environments through modules.  That means, set up environment
   variables properly for the view by re-processing the modules.

1. Fix ``spack env loads -r`` to generate only one copy of each
   package, even if things are not all concretized together.

Outstanding Environemnt PRs
===========================

* Install entire environment in common prefix (useful for containers): `https://github.com/spack/spack/issues/11164`_

* Spack Setup
