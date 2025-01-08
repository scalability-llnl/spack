###########################################################
#ARCH    AMD Linux x86_64 #serial smpar dmpar dm+sm
# For optimized AMDFCFLAGS and AMDLDFLAGS, please reach out to toolchainsupport@amd.com
#

DESCRIPTION     =       AMD ($SFC/$SCC) :  AMD ZEN Architectures
DMPARALLEL      =       # 1
OMPCPP          =       # -D_OPENMP
OMP             =       # -fopenmp
OMPCC           =       # -fopenmp
SFC             =       flang
SCC             =       clang
CCOMP           =       clang
DM_FC           =       {MPIFC}
DM_CC           =       {MPICC}
FC              =       CONFIGURE_FC
CC              =       CONFIGURE_CC
LD              =       $(FC)
RWORDSIZE       =       CONFIGURE_RWORDSIZE

AMDMATHLIB      =       -fveclib=AMDLIBM
AMDLDFLAGS      =
AMDFCFLAGS      =       -mllvm -disable-loop-idiom-memset -mllvm -inline-threshold=3000 \
                        -mllvm -inlinehint-threshold=10000 -mllvm -enable-loop-distribute-adv \
                        -mllvm -vectorize-non-contiguous-memory-aggressively \
                        -mllvm -vectorizer-maximize-bandwidth=true \
                        -mllvm -enable-gather -mllvm -legalize-vector-library-calls  \
                        -finline-aggressive -finline-hint-functions

PROMOTION       =       #-fdefault-real-8
ARCH_LOCAL      =       -DNONSTANDARD_SYSTEM_SUBR {CTSM_SUBST}
CFLAGS_LOCAL    =       -w -c -m64 -Ofast
LDFLAGS_LOCAL   =       -m64 -Ofast -Mstack_arrays $(AMDLDFLAGS) $(AMDMATHLIB) -lamdlibm -lm
CPLUSPLUSLIB    =
ESMF_LDFLAG     =       $(CPLUSPLUSLIB)
FCOPTIM         =       -Ofast -Mstack_arrays -ftree-vectorize -funroll-loops -finline-aggressive \
                        -finline-hint-functions $(AMDMATHLIB) $(AMDFCFLAGS)
FCREDUCEDOPT    =       -O2 -Mstack_arrays -DFCREDUCEDOPT
FCNOOPT         =       -O0
FCDEBUG         =       # -g $(FCNOOPT)
FORMAT_FIXED    =       -ffixed-form
FORMAT_FREE     =       -ffree-form
FCSUFFIX        =
BYTESWAPIO      =       -Mbyteswapio
FCBASEOPTS_NO_G =       -w $(FORMAT_FREE) $(BYTESWAPIO)
FCBASEOPTS      =       $(FCBASEOPTS_NO_G) $(FCDEBUG)
MODULE_SRCH_FLAG=
TRADFLAG        =       CONFIGURE_TRADFLAG
CPP             =       /lib/cpp CONFIGURE_CPPFLAGS
AR              =       llvm-ar
ARFLAGS         =       ru
M4              =       m4
RANLIB          =       llvm-ranlib
RLFLAGS         =
CC_TOOLS        =       $(SCC)
NETCDFPAR_BUILD =       {NETCDFPAR_BUILD}

#insert new stanza here
