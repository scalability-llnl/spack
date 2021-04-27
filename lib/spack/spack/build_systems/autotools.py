# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import inspect
import itertools
import os
import os.path
import stat
from subprocess import PIPE
from subprocess import check_call
from typing import List  # novm

import llnl.util.tty as tty
import llnl.util.filesystem as fs
from llnl.util.filesystem import working_dir, force_remove
from spack.package import PackageBase, run_after, run_before
from spack.util.executable import Executable


class AutotoolsPackage(PackageBase):
    """Specialized class for packages built using GNU Autotools.

    This class provides four phases that can be overridden:

        1. :py:meth:`~.AutotoolsPackage.autoreconf`
        2. :py:meth:`~.AutotoolsPackage.configure`
        3. :py:meth:`~.AutotoolsPackage.build`
        4. :py:meth:`~.AutotoolsPackage.install`

    They all have sensible defaults and for many packages the only thing
    necessary will be to override the helper method
    :py:meth:`~.AutotoolsPackage.configure_args`.
    For a finer tuning you may also override:

        +-----------------------------------------------+--------------------+
        | **Method**                                    | **Purpose**        |
        +===============================================+====================+
        | :py:attr:`~.AutotoolsPackage.build_targets`   | Specify ``make``   |
        |                                               | targets for the    |
        |                                               | build phase        |
        +-----------------------------------------------+--------------------+
        | :py:attr:`~.AutotoolsPackage.install_targets` | Specify ``make``   |
        |                                               | targets for the    |
        |                                               | install phase      |
        +-----------------------------------------------+--------------------+
        | :py:meth:`~.AutotoolsPackage.check`           | Run  build time    |
        |                                               | tests if required  |
        +-----------------------------------------------+--------------------+

    """
    #: Phases of a GNU Autotools package
    phases = ['autoreconf', 'configure', 'build', 'install']
    #: This attribute is used in UI queries that need to know the build
    #: system base class
    build_system_class = 'AutotoolsPackage'
    #: Whether or not to update ``config.guess`` and ``config.sub`` on old
    #: architectures
    patch_config_files = True
    #: Whether or not to update ``libtool``
    #: (currently only for Arm/Clang/Fujitsu compilers)
    patch_libtool = True

    #: Targets for ``make`` during the :py:meth:`~.AutotoolsPackage.build`
    #: phase
    build_targets = []  # type: List[str]
    #: Targets for ``make`` during the :py:meth:`~.AutotoolsPackage.install`
    #: phase
    install_targets = ['install']

    #: Callback names for build-time test
    build_time_test_callbacks = ['check']

    #: Callback names for install-time test
    install_time_test_callbacks = ['installcheck']

    #: Set to true to force the autoreconf step even if configure is present
    force_autoreconf = False
    #: Options to be passed to autoreconf when using the default implementation
    autoreconf_extra_args = []  # type: List[str]

    #: If False deletes all the .la files in the prefix folder
    #: after the installation. If True instead it installs them.
    install_libtool_archives = False

    @property
    def _removed_la_files_log(self):
        """File containing the list of remove libtool archives"""
        build_dir = self.build_directory
        if not os.path.isabs(self.build_directory):
            build_dir = os.path.join(self.stage.path, build_dir)
        return os.path.join(build_dir, 'removed_la_files.txt')

    @property
    def archive_files(self):
        """Files to archive for packages based on autotools"""
        files = [os.path.join(self.build_directory, 'config.log')]
        if not self.install_libtool_archives:
            files.append(self._removed_la_files_log)
        return files

    @run_after('autoreconf')
    def _do_patch_config_files(self):
        """Some packages ship with older config.guess/config.sub files and
        need to have these updated when installed on a newer architecture.
        In particular, config.guess fails for PPC64LE for version prior
        to a 2013-06-10 build date (automake 1.13.4) and for ARM (aarch64).
        """
        if not self.patch_config_files or (
                not self.spec.satisfies('target=ppc64le:') and
                not self.spec.satisfies('target=aarch64:')
        ):
            return

        # TODO: Expand this to select the 'config.sub'-compatible architecture
        # for each platform (e.g. 'config.sub' doesn't accept 'power9le', but
        # does accept 'ppc64le').
        if self.spec.satisfies('target=ppc64le:'):
            config_arch = 'ppc64le'
        elif self.spec.satisfies('target=aarch64:'):
            config_arch = 'aarch64'
        else:
            config_arch = 'local'

        def runs_ok(script_abs_path):
            # Construct the list of arguments for the call
            additional_args = {
                'config.sub': [config_arch]
            }
            script_name = os.path.basename(script_abs_path)
            args = [script_abs_path] + additional_args.get(script_name, [])

            try:
                check_call(args, stdout=PIPE, stderr=PIPE)
            except Exception as e:
                tty.debug(e)
                return False

            return True

        # Compute the list of files that needs to be patched
        search_dir = self.stage.path
        to_be_patched = fs.find(
            search_dir, files=['config.sub', 'config.guess'], recursive=True
        )
        to_be_patched = [f for f in to_be_patched if not runs_ok(f)]

        # If there are no files to be patched, return early
        if not to_be_patched:
            return

        # Directories where to search for files to be copied
        # over the failing ones
        good_file_dirs = ['/usr/share']
        if 'automake' in self.spec:
            good_file_dirs.insert(0, self.spec['automake'].prefix)

        # List of files to be found in the directories above
        to_be_found = list(set(os.path.basename(f) for f in to_be_patched))
        substitutes = {}
        for directory in good_file_dirs:
            candidates = fs.find(directory, files=to_be_found, recursive=True)
            candidates = [f for f in candidates if runs_ok(f)]
            for name, good_files in itertools.groupby(
                    candidates, key=os.path.basename
            ):
                substitutes[name] = next(good_files)
                to_be_found.remove(name)

        # Check that we found everything we needed
        if to_be_found:
            msg = 'Failed to find suitable substitutes for {0}'
            raise RuntimeError(msg.format(', '.join(to_be_found)))

        # Copy the good files over the bad ones
        for abs_path in to_be_patched:
            name = os.path.basename(abs_path)
            mode = os.stat(abs_path).st_mode
            os.chmod(abs_path, stat.S_IWUSR)
            fs.copy(substitutes[name], abs_path)
            os.chmod(abs_path, mode)

    @run_before('configure')
    def _set_autotools_environment_variables(self):
        """Many autotools builds use a version of mknod.m4 that fails when
        running as root unless FORCE_UNSAFE_CONFIGURE is set to 1.

        We set this to 1 and expect the user to take responsibility if
        they are running as root. They have to anyway, as this variable
        doesn't actually prevent configure from doing bad things as root.
        Without it, configure just fails halfway through, but it can
        still run things *before* this check. Forcing this just removes a
        nuisance -- this is not circumventing any real protection.

        """
        os.environ["FORCE_UNSAFE_CONFIGURE"] = "1"

    @run_after('configure')
    def _do_patch_libtool(self):
        """If configure generates a "libtool" script that does not correctly
        detect the compiler (and patch_libtool is set), patch in the correct
        flags for the Arm, Clang/Flang, and Fujitsu compilers."""

        # Exit early if we are required not to patch libtool
        if not self.patch_libtool:
            return

        for libtool_path in fs.find(
                self.build_directory, 'libtool', recursive=True):
            self._patch_libtool(libtool_path)

    def _patch_libtool(self, libtool_path):
        if self.spec.satisfies('%arm')\
                or self.spec.satisfies('%clang')\
                or self.spec.satisfies('%fj'):
            fs.filter_file('wl=""\n', 'wl="-Wl,"\n', libtool_path)
            fs.filter_file('pic_flag=""\n',
                           'pic_flag="{0}"\n'
                           .format(self.compiler.cc_pic_flag),
                           libtool_path)
        if self.spec.satisfies('%fj'):
            fs.filter_file('-nostdlib', '', libtool_path)
            rehead = r'/\S*/'
            objfile = ['fjhpctag.o', 'fjcrt0.o', 'fjlang08.o', 'fjomp.o',
                       'crti.o', 'crtbeginS.o', 'crtendS.o']
            for o in objfile:
                fs.filter_file(rehead + o, '', libtool_path)

    @property
    def configure_directory(self):
        """Returns the directory where 'configure' resides.

        :return: directory where to find configure
        """
        return self.stage.source_path

    @property
    def configure_abs_path(self):
        # Absolute path to configure
        configure_abs_path = os.path.join(
            os.path.abspath(self.configure_directory), 'configure'
        )
        return configure_abs_path

    @property
    def build_directory(self):
        """Override to provide another place to build the package"""
        return self.configure_directory

    @run_before('autoreconf')
    def delete_configure_to_force_update(self):
        if self.force_autoreconf:
            force_remove(self.configure_abs_path)

    def autoreconf(self, spec, prefix):
        """Not needed usually, configure should be already there"""
        # If configure exists nothing needs to be done
        if os.path.exists(self.configure_abs_path):
            return
        # Else try to regenerate it
        autotools = ['m4', 'autoconf', 'automake', 'libtool']
        missing = [x for x in autotools if x not in spec]
        if missing:
            msg = 'Cannot generate configure: missing dependencies {0}'
            raise RuntimeError(msg.format(missing))
        tty.msg('Configure script not found: trying to generate it')
        tty.warn('*********************************************************')
        tty.warn('* If the default procedure fails, consider implementing *')
        tty.warn('*        a custom AUTORECONF phase in the package       *')
        tty.warn('*********************************************************')
        with working_dir(self.configure_directory):
            m = inspect.getmodule(self)
            # This line is what is needed most of the time
            # --install, --verbose, --force
            autoreconf_args = ['-ivf']
            autoreconf_args += self.autoreconf_search_path_args
            autoreconf_args += self.autoreconf_extra_args
            m.autoreconf(*autoreconf_args)

    @property
    def autoreconf_search_path_args(self):
        """Arguments to autoreconf to modify the search paths"""
        search_path_args = []
        for dep in self.spec.dependencies(deptype='build'):
            if os.path.exists(dep.prefix.share.aclocal):
                search_path_args.extend(['-I', dep.prefix.share.aclocal])
        return search_path_args

    @run_after('autoreconf')
    def set_configure_or_die(self):
        """Checks the presence of a ``configure`` file after the
        autoreconf phase. If it is found sets a module attribute
        appropriately, otherwise raises an error.

        :raises RuntimeError: if a configure script is not found in
            :py:meth:`~AutotoolsPackage.configure_directory`
        """
        # Check if a configure script is there. If not raise a RuntimeError.
        if not os.path.exists(self.configure_abs_path):
            msg = 'configure script not found in {0}'
            raise RuntimeError(msg.format(self.configure_directory))

        # Monkey-patch the configure script in the corresponding module
        inspect.getmodule(self).configure = Executable(
            self.configure_abs_path
        )

    def configure_args(self):
        """Produces a list containing all the arguments that must be passed to
        configure, except ``--prefix`` which will be pre-pended to the list.

        :return: list of arguments for configure
        """
        return []

    def flags_to_build_system_args(self, flags):
        """Produces a list of all command line arguments to pass specified
        compiler flags to configure."""
        # Has to be dynamic attribute due to caching.
        setattr(self, 'configure_flag_args', [])
        for flag, values in flags.items():
            if values:
                values_str = '{0}={1}'.format(flag.upper(), ' '.join(values))
                self.configure_flag_args.append(values_str)
        # Spack's fflags are meant for both F77 and FC, therefore we
        # additionaly set FCFLAGS if required.
        values = flags.get('fflags', None)
        if values:
            values_str = 'FCFLAGS={0}'.format(' '.join(values))
            self.configure_flag_args.append(values_str)

    def configure(self, spec, prefix):
        """Runs configure with the arguments specified in
        :py:meth:`~.AutotoolsPackage.configure_args`
        and an appropriately set prefix.
        """
        options = getattr(self, 'configure_flag_args', [])
        options += ['--prefix={0}'.format(prefix)]
        options += self.configure_args()

        with working_dir(self.build_directory, create=True):
            inspect.getmodule(self).configure(*options)

    def build(self, spec, prefix):
        """Makes the build targets specified by
        :py:attr:``~.AutotoolsPackage.build_targets``
        """
        with working_dir(self.build_directory):
            inspect.getmodule(self).make(*self.build_targets)

    def install(self, spec, prefix):
        """Makes the install targets specified by
        :py:attr:``~.AutotoolsPackage.install_targets``
        """
        with working_dir(self.build_directory):
            inspect.getmodule(self).make(*self.install_targets)

    run_after('build')(PackageBase._run_default_build_time_test_callbacks)

    def check(self):
        """Searches the Makefile for targets ``test`` and ``check``
        and runs them if found.
        """
        with working_dir(self.build_directory):
            self._if_make_target_execute('test')
            self._if_make_target_execute('check')

    def _activate_or_not(
            self,
            name,
            activation_word,
            deactivation_word,
            activation_value=None
    ):
        """This function contains the current implementation details of
        :py:meth:`~.AutotoolsPackage.with_or_without` and
        :py:meth:`~.AutotoolsPackage.enable_or_disable`.

        Args:
            name (str): name of the variant that is being processed
            activation_word (str): the default activation word ('with' in the
                case of ``with_or_without``)
            deactivation_word (str): the default deactivation word ('without'
                in the case of ``with_or_without``)
            activation_value (callable): callable that accepts a single
                value. This value is either one of the allowed values for a
                multi-valued variant or the name of a bool-valued variant.
                Returns the parameter to be used when the value is activated.

                The special value 'prefix' can also be assigned and will return
                ``spec[name].prefix`` as activation parameter.

        Examples:

            Given a package with:

            .. code-block:: python

                variant('foo', values=('x', 'y'), description='')
                variant('bar', default=True, description='')

            calling this function like:

            .. code-block:: python

                _activate_or_not(
                    'foo', 'with', 'without', activation_value='prefix'
                )
                _activate_or_not('bar', 'with', 'without')

            will generate the following configuration options:

            .. code-block:: console

                --with-x=<prefix-to-x> --without-y --with-bar

            for ``<spec-name> foo=x +bar``

        Returns:
            list of strings that corresponds to the activation/deactivation
            of the variant that has been processed

        Raises:
            KeyError: if name is not among known variants
        """
        spec = self.spec
        args = []

        if activation_value == 'prefix':
            activation_value = lambda x: spec[x].prefix

        # Defensively look that the name passed as argument is among
        # variants
        if name not in self.variants:
            msg = '"{0}" is not a variant of "{1}"'
            raise KeyError(msg.format(name, self.name))

        # Create a list of pairs. Each pair includes a configuration
        # option and whether or not that option is activated
        if set(self.variants[name].values) == set((True, False)):
            # BoolValuedVariant carry information about a single option.
            # Nonetheless, for uniformity of treatment we'll package them
            # in an iterable of one element.
            condition = '+{name}'.format(name=name)
            options = [(name, condition in spec)]
        else:
            condition = '{name}={value}'
            # "feature_values" is used to track values which correspond to
            # features which can be enabled or disabled as understood by the
            # package's build system. It excludes values which have special
            # meanings and do not correspond to features (e.g. "none")
            feature_values = getattr(
                self.variants[name].values, 'feature_values', None
            ) or self.variants[name].values

            options = [
                (value, condition.format(name=name, value=value) in spec)
                for value in feature_values
            ]

        # For each allowed value in the list of values
        for option_value, activated in options:
            # Search for an override in the package for this value
            override_name = '{0}_or_{1}_{2}'.format(
                activation_word, deactivation_word, option_value
            )
            line_generator = getattr(self, override_name, None)
            # If not available use a sensible default
            if line_generator is None:
                def _default_generator(is_activated):
                    if is_activated:
                        line = '--{0}-{1}'.format(
                            activation_word, option_value
                        )
                        if activation_value is not None and activation_value(option_value):  # NOQA=ignore=E501
                            line += '={0}'.format(
                                activation_value(option_value)
                            )
                        return line
                    return '--{0}-{1}'.format(deactivation_word, option_value)
                line_generator = _default_generator
            args.append(line_generator(activated))
        return args

    def with_or_without(self, name, activation_value=None):
        """Inspects a variant and returns the arguments that activate
        or deactivate the selected feature(s) for the configure options.

        This function works on all type of variants. For bool-valued variants
        it will return by default ``--with-{name}`` or ``--without-{name}``.
        For other kinds of variants it will cycle over the allowed values and
        return either ``--with-{value}`` or ``--without-{value}``.

        If activation_value is given, then for each possible value of the
        variant, the option ``--with-{value}=activation_value(value)`` or
        ``--without-{value}`` will be added depending on whether or not
        ``variant=value`` is in the spec.

        Args:
            name (str): name of a valid multi-valued variant
            activation_value (callable): callable that accepts a single
                value and returns the parameter to be used leading to an entry
                of the type ``--with-{name}={parameter}``.

                The special value 'prefix' can also be assigned and will return
                ``spec[name].prefix`` as activation parameter.

        Returns:
            list of arguments to configure
        """
        return self._activate_or_not(name, 'with', 'without', activation_value)

    def enable_or_disable(self, name, activation_value=None):
        """Same as :py:meth:`~.AutotoolsPackage.with_or_without` but substitute
        ``with`` with ``enable`` and ``without`` with ``disable``.

        Args:
            name (str): name of a valid multi-valued variant
            activation_value (callable): if present accepts a single value
                and returns the parameter to be used leading to an entry of the
                type ``--enable-{name}={parameter}``

                The special value 'prefix' can also be assigned and will return
                ``spec[name].prefix`` as activation parameter.

        Returns:
            list of arguments to configure
        """
        return self._activate_or_not(
            name, 'enable', 'disable', activation_value
        )

    run_after('install')(PackageBase._run_default_install_time_test_callbacks)

    def installcheck(self):
        """Searches the Makefile for an ``installcheck`` target
        and runs it if found.
        """
        with working_dir(self.build_directory):
            self._if_make_target_execute('installcheck')

    # Check that self.prefix is there after installation
    run_after('install')(PackageBase.sanity_check_prefix)

    @run_after('install')
    def remove_libtool_archives(self):
        """Remove all .la files in prefix sub-folders if the package sets
        ``install_libtool_archives`` to be False.
        """
        # If .la files are to be installed there's nothing to do
        if self.install_libtool_archives:
            return

        # Remove the files and create a log of what was removed
        libtool_files = fs.find(str(self.prefix), '*.la', recursive=True)
        with fs.safe_remove(*libtool_files):
            fs.mkdirp(os.path.dirname(self._removed_la_files_log))
            with open(self._removed_la_files_log, mode='w') as f:
                f.write('\n'.join(libtool_files))
