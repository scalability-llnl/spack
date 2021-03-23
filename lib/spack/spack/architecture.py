# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""
This module contains all the elements that are required to create an
architecture object. These include, the target processor, the operating system,
and the architecture platform (i.e. cray, darwin, linux, etc) classes.

On a multiple architecture machine, the architecture spec field can be set to
build a package against any target and operating system that is present on the
platform. On Cray platforms or any other architecture that has different front
and back end environments, the operating system will determine the method of
compiler
detection.

There are two different types of compiler detection:
    1. Through the $PATH env variable (front-end detection)
    2. Through the tcl module system. (back-end detection)

Depending on which operating system is specified, the compiler will be detected
using one of those methods.

For platforms such as linux and darwin, the operating system is autodetected
and the target is set to be x86_64.

The command line syntax for specifying an architecture is as follows:

    target=<Target name> os=<OperatingSystem name>

If the user wishes to use the defaults, either target or os can be left out of
the command line and Spack will concretize using the default. These defaults
are set in the 'platforms/' directory which contains the different subclasses
for platforms. If the machine has multiple architectures, the user can
also enter front-end, or fe or back-end or be. These settings will concretize
to their respective front-end and back-end targets and operating systems.
Additional platforms can be added by creating a subclass of Platform
and adding it inside the platform directory.

Platforms are an abstract class that are extended by subclasses. If the user
wants to add a new type of platform (such as cray_xe), they can create a
subclass and set all the class attributes such as priority, front_target,
back_target, front_os, back_os. Platforms also contain a priority class
attribute. A lower number signifies higher priority. These numbers are
arbitrarily set and can be changed though often there isn't much need unless a
new platform is added and the user wants that to be detected first.

Targets are created inside the platform subclasses. Most architecture
(like linux, and darwin) will have only one target (x86_64) but in the case of
Cray machines, there is both a frontend and backend processor. The user can
specify which targets are present on front-end and back-end architecture

Depending on the platform, operating systems are either auto-detected or are
set. The user can set the front-end and back-end operating setting by the class
attributes front_os and back_os. The operating system as described earlier,
will be responsible for compiler detection.
"""
import contextlib
import functools
import inspect
import warnings

import archspec.cpu
import six

import llnl.util.tty as tty
from llnl.util.lang import memoized, list_modules, key_ordering

import spack.compiler
import spack.compilers
import spack.config
import spack.paths
import spack.error as serr
import spack.util.executable
import spack.version
from spack.util.naming import mod_to_class
from spack.util.spack_yaml import syaml_dict


class NoPlatformError(serr.SpackError):
    def __init__(self):
        super(NoPlatformError, self).__init__(
            "Could not determine a platform for this machine.")


def _ensure_other_is_target(method):
    """Decorator to be used in dunder methods taking a single argument to
    ensure that the argument is an instance of ``Target`` too.
    """
    @functools.wraps(method)
    def _impl(self, other):
        if isinstance(other, six.string_types):
            other = Target(other)

        if not isinstance(other, Target):
            return NotImplemented

        return method(self, other)

    return _impl


class Target(object):
    def __init__(self, name, module_name=None):
        """Target models microarchitectures and their compatibility.

        Args:
            name (str or Microarchitecture):micro-architecture of the
                target
            module_name (str): optional module name to get access to the
                current target. This is typically used on machines
                like Cray (e.g. craype-compiler)
        """
        if not isinstance(name, archspec.cpu.Microarchitecture):
            name = archspec.cpu.TARGETS.get(
                name, archspec.cpu.generic_microarchitecture(name)
            )
        self.microarchitecture = name
        self.module_name = module_name

    @property
    def name(self):
        return self.microarchitecture.name

    @_ensure_other_is_target
    def __eq__(self, other):
        return self.microarchitecture == other.microarchitecture and \
            self.module_name == other.module_name

    def __ne__(self, other):
        # This method is necessary as long as we support Python 2. In Python 3
        # __ne__ defaults to the implementation below
        return not self == other

    @_ensure_other_is_target
    def __lt__(self, other):
        # TODO: In the future it would be convenient to say
        # TODO: `spec.architecture.target < other.architecture.target`
        # TODO: and change the semantic of the comparison operators

        # This is needed to sort deterministically specs in a list.
        # It doesn't implement a total ordering semantic.
        return self.microarchitecture.name < other.microarchitecture.name

    def __hash__(self):
        return hash((self.name, self.module_name))

    @staticmethod
    def from_dict_or_value(dict_or_value):
        # A string here represents a generic target (like x86_64 or ppc64) or
        # a custom micro-architecture
        if isinstance(dict_or_value, six.string_types):
            return Target(dict_or_value)

        # TODO: From a dict we actually retrieve much more information than
        # TODO: just the name. We can use that information to reconstruct an
        # TODO: "old" micro-architecture or check the current definition.
        target_info = dict_or_value
        return Target(target_info['name'])

    def to_dict_or_value(self):
        """Returns a dict or a value representing the current target.

        String values are used to keep backward compatibility with generic
        targets, like e.g. x86_64 or ppc64. More specific micro-architectures
        will return a dictionary which contains information on the name,
        features, vendor, generation and parents of the current target.
        """
        # Generic targets represent either an architecture
        # family (like x86_64) or a custom micro-architecture
        if self.microarchitecture.vendor == 'generic':
            return str(self)

        return syaml_dict(
            self.microarchitecture.to_dict(return_list_of_items=True)
        )

    def __repr__(self):
        cls_name = self.__class__.__name__
        fmt = cls_name + '({0}, {1})'
        return fmt.format(repr(self.microarchitecture),
                          repr(self.module_name))

    def __str__(self):
        return str(self.microarchitecture)

    def __contains__(self, cpu_flag):
        return cpu_flag in self.microarchitecture

    def optimization_flags(self, compiler):
        """Returns the flags needed to optimize for this target using
        the compiler passed as argument.

        Args:
            compiler (CompilerSpec or Compiler): object that contains both the
                name and the version of the compiler we want to use
        """
        # Mixed toolchains are not supported yet
        import spack.compilers
        if isinstance(compiler, spack.compiler.Compiler):
            if spack.compilers.is_mixed_toolchain(compiler):
                msg = ('microarchitecture specific optimizations are not '
                       'supported yet on mixed compiler toolchains [check'
                       ' {0.name}@{0.version} for further details]')
                warnings.warn(msg.format(compiler))
                return ''

        # Try to check if the current compiler comes with a version number or
        # has an unexpected suffix. If so, treat it as a compiler with a
        # custom spec.
        compiler_version = compiler.version
        version_number, suffix = archspec.cpu.version_components(
            compiler.version
        )
        if not version_number or suffix not in ('', 'apple'):
            # Try to deduce the underlying version of the compiler, regardless
            # of its name in compilers.yaml. Depending on where this function
            # is called we might get either a CompilerSpec or a fully fledged
            # compiler object.
            import spack.spec
            if isinstance(compiler, spack.spec.CompilerSpec):
                compiler = spack.compilers.compilers_for_spec(compiler).pop()
            try:
                compiler_version = compiler.real_version
            except spack.util.executable.ProcessError as e:
                # log this and just return compiler.version instead
                tty.debug(str(e))

        return self.microarchitecture.optimization_flags(
            compiler.name, str(compiler_version)
        )


@key_ordering
class Platform(object):
    """ Abstract class that each type of Platform will subclass.
        Will return a instance of it once it is returned.
    """

    # Subclass sets number. Controls detection order
    priority        = None   # type: int

    #: binary formats used on this platform; used by relocation logic
    binary_formats  = ['elf']

    front_end       = None   # type: str
    back_end        = None   # type: str
    default         = None   # type: str # The default back end target.

    front_os        = None   # type: str
    back_os         = None   # type: str
    default_os      = None   # type: str

    reserved_targets = ['default_target', 'frontend', 'fe', 'backend', 'be']
    reserved_oss = ['default_os', 'frontend', 'fe', 'backend', 'be']

    def __init__(self, name):
        self.targets = {}
        self.operating_sys = {}
        self.name = name

    def add_target(self, name, target):
        """Used by the platform specific subclass to list available targets.
        Raises an error if the platform specifies a name
        that is reserved by spack as an alias.
        """
        if name in Platform.reserved_targets:
            raise ValueError(
                "%s is a spack reserved alias "
                "and cannot be the name of a target" % name)
        self.targets[name] = target

    def target(self, name):
        """This is a getter method for the target dictionary
        that handles defaulting based on the values provided by default,
        front-end, and back-end. This can be overwritten
        by a subclass for which we want to provide further aliasing options.
        """
        # TODO: Check if we can avoid using strings here
        name = str(name)
        if name == 'default_target':
            name = self.default
        elif name == 'frontend' or name == 'fe':
            name = self.front_end
        elif name == 'backend' or name == 'be':
            name = self.back_end

        return self.targets.get(name, None)

    def add_operating_system(self, name, os_class):
        """ Add the operating_system class object into the
            platform.operating_sys dictionary
        """
        if name in Platform.reserved_oss:
            raise ValueError(
                "%s is a spack reserved alias "
                "and cannot be the name of an OS" % name)
        self.operating_sys[name] = os_class

    def operating_system(self, name):
        if name == 'default_os':
            name = self.default_os
        if name == 'frontend' or name == "fe":
            name = self.front_os
        if name == 'backend' or name == 'be':
            name = self.back_os

        return self.operating_sys.get(name, None)

    @classmethod
    def setup_platform_environment(cls, pkg, env):
        """ Subclass can override this method if it requires any
            platform-specific build environment modifications.
        """

    @classmethod
    def detect(cls):
        """ Subclass is responsible for implementing this method.
            Returns True if the Platform class detects that
            it is the current platform
            and False if it's not.
        """
        raise NotImplementedError()

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return self.name

    def _cmp_key(self):
        t_keys = ''.join(str(t._cmp_key()) for t in
                         sorted(self.targets.values()))
        o_keys = ''.join(str(o._cmp_key()) for o in
                         sorted(self.operating_sys.values()))
        return (self.name,
                self.default,
                self.front_end,
                self.back_end,
                self.default_os,
                self.front_os,
                self.back_os,
                t_keys,
                o_keys)


@key_ordering
class OperatingSystem(object):
    """ Operating System will be like a class similar to platform extended
        by subclasses for the specifics. Operating System will contain the
        compiler finding logic. Instead of calling two separate methods to
        find compilers we call find_compilers method for each operating system
    """

    def __init__(self, name, version):
        self.name = name.replace('-', '_')
        self.version = str(version).replace('-', '_')

    def __str__(self):
        return "%s%s" % (self.name, self.version)

    def __repr__(self):
        return self.__str__()

    def _cmp_key(self):
        return (self.name, self.version)

    def to_dict(self):
        return syaml_dict([
            ('name', self.name),
            ('version', self.version)
        ])


@key_ordering
class Arch(object):
    """Architecture is now a class to help with setting attributes.

    TODO: refactor so that we don't need this class.
    """

    def __init__(self, plat=None, os=None, target=None):
        self.platform = plat
        if plat and os:
            os = self.platform.operating_system(os)
        self.os = os
        if plat and target:
            target = self.platform.target(target)
        self.target = target

        # Hooks for parser to use when platform is set after target or os
        self.target_string = None
        self.os_string = None

    @property
    def concrete(self):
        return all((self.platform is not None,
                    isinstance(self.platform, Platform),
                    self.os is not None,
                    isinstance(self.os, OperatingSystem),
                    self.target is not None, isinstance(self.target, Target)))

    def __str__(self):
        if self.platform or self.os or self.target:
            if self.platform.name == 'darwin':
                os_name = self.os.name if self.os else "None"
            else:
                os_name = str(self.os)

            return (str(self.platform) + "-" +
                    os_name + "-" + str(self.target))
        else:
            return ''

    def __contains__(self, string):
        return string in str(self)

    # TODO: make this unnecessary: don't include an empty arch on *every* spec.
    def __nonzero__(self):
        return (self.platform is not None or
                self.os is not None or
                self.target is not None)
    __bool__ = __nonzero__

    def _cmp_key(self):
        if isinstance(self.platform, Platform):
            platform = self.platform.name
        else:
            platform = self.platform
        if isinstance(self.os, OperatingSystem):
            os = self.os.name
        else:
            os = self.os
        if isinstance(self.target, Target):
            target = self.target.microarchitecture
        else:
            target = self.target
        return (platform, os, target)

    def to_dict(self):
        str_or_none = lambda v: str(v) if v else None
        d = syaml_dict([
            ('platform', str_or_none(self.platform)),
            ('platform_os', str_or_none(self.os)),
            ('target', self.target.to_dict_or_value())])
        return syaml_dict([('arch', d)])

    def to_spec(self):
        """Convert this Arch to an anonymous Spec with architecture defined."""
        spec = spack.spec.Spec()
        spec.architecture = spack.spec.ArchSpec(str(self))
        return spec

    @staticmethod
    def from_dict(d):
        spec = spack.spec.ArchSpec.from_dict(d)
        return arch_for_spec(spec)


@memoized
def get_platform(platform_name):
    """Returns a platform object that corresponds to the given name."""
    platform_list = all_platforms()
    for p in platform_list:
        if platform_name.replace("_", "").lower() == p.__name__.lower():
            return p()


def verify_platform(platform_name):
    """ Determines whether or not the platform with the given name is supported
        in Spack.  For more information, see the 'spack.platforms' submodule.
    """
    platform_name = platform_name.replace("_", "").lower()
    platform_names = [p.__name__.lower() for p in all_platforms()]

    if platform_name not in platform_names:
        tty.die("%s is not a supported platform; supported platforms are %s" %
                (platform_name, platform_names))


def arch_for_spec(arch_spec):
    """Transforms the given architecture spec into an architecture object."""
    arch_spec = spack.spec.ArchSpec(arch_spec)
    assert arch_spec.concrete

    arch_plat = get_platform(arch_spec.platform)
    if not (arch_plat.operating_system(arch_spec.os) and
            arch_plat.target(arch_spec.target)):
        raise ValueError(
            "Can't recreate arch for spec %s on current arch %s; "
            "spec architecture is too different" % (arch_spec, sys_type()))

    return Arch(arch_plat, arch_spec.os, arch_spec.target)


@memoized
def _all_platforms():
    classes = []
    mod_path = spack.paths.platform_path
    parent_module = "spack.platforms"

    for name in list_modules(mod_path):
        mod_name = '%s.%s' % (parent_module, name)
        class_name = mod_to_class(name)
        mod = __import__(mod_name, fromlist=[class_name])
        if not hasattr(mod, class_name):
            tty.die('No class %s defined in %s' % (class_name, mod_name))
        cls = getattr(mod, class_name)
        if not inspect.isclass(cls):
            tty.die('%s.%s is not a class' % (mod_name, class_name))

        classes.append(cls)

    return classes


@memoized
def _platform():
    """Detects the platform for this machine.

    Gather a list of all available subclasses of platforms.
    Sorts the list according to their priority looking. Priority is
    an arbitrarily set number. Detects platform either using uname or
    a file path (/opt/cray...)
    """
    # Try to create a Platform object using the config file FIRST
    platform_list = _all_platforms()
    platform_list.sort(key=lambda a: a.priority)

    for platform_cls in platform_list:
        if platform_cls.detect():
            return platform_cls()


#: The "real" platform of the host running Spack. This should not be changed
#: by any method and is here as a convenient way to refer to the host platform.
real_platform = _platform

#: The current platform used by Spack. May be swapped by the use_platform
#: context manager.
platform = _platform

#: The list of all platform classes. May be swapped by the use_platform
#: context manager.
all_platforms = _all_platforms


@memoized
def default_arch():
    """Default ``Arch`` object for this machine.

    See ``sys_type()``.
    """
    return Arch(platform(), 'default_os', 'default_target')


def sys_type():
    """Print out the "default" platform-os-target tuple for this machine.

    On machines with only one target OS/target, prints out the
    platform-os-target for the frontend.  For machines with a frontend
    and a backend, prints the default backend.

    TODO: replace with use of more explicit methods to get *all* the
    backends, as client code should really be aware of cross-compiled
    architectures.

    """
    return str(default_arch())


@memoized
def compatible_sys_types():
    """Returns a list of all the systypes compatible with the current host."""
    compatible_archs = []
    current_host = archspec.cpu.host()
    compatible_targets = [current_host] + current_host.ancestors
    for target in compatible_targets:
        arch = Arch(platform(), 'default_os', target)
        compatible_archs.append(str(arch))
    return compatible_archs


class _PickleableCallable(object):
    """Class used to pickle a callable that may substitute either
    _platform or _all_platforms. Lambda or nested functions are
    not pickleable.
    """
    def __init__(self, return_value):
        self.return_value = return_value

    def __call__(self):
        return self.return_value


@contextlib.contextmanager
def use_platform(new_platform):
    global platform, all_platforms

    msg = '"{0}" must be an instance of Platform'
    assert isinstance(new_platform, Platform), msg.format(new_platform)

    original_platform_fn, original_all_platforms_fn = platform, all_platforms
    platform = _PickleableCallable(new_platform)
    all_platforms = _PickleableCallable([type(new_platform)])

    # Clear configuration and compiler caches
    spack.config.config.clear_caches()
    spack.compilers._cache_config_files = []

    yield new_platform

    platform, all_platforms = original_platform_fn, original_all_platforms_fn

    # Clear configuration and compiler caches
    spack.config.config.clear_caches()
    spack.compilers._cache_config_files = []
