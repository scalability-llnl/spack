# ======================================================================
#  pythia6 main build file
#
#  setup cmake
#  cd .../path/to/build/directory
#  cmake [-DCMAKE_INSTALL_PREFIX=/install/path]
#        [-DCMAKE_BUILD_TYPE=<RelWithDebInfo|Debug|Release|MinSizeRel> ]
#        [-Drun_long_tests:BOOL=ON]
#        .../path/to/pythia/source
#  make
#  make test
#  make install
# ======================================================================

# use cmake 2.6 or later
cmake_minimum_required (VERSION 2.6)

project(pythia6 C Fortran)
message(STATUS "pythia version is ${PYTHIA6_VERSION}")

enable_testing()

#build all libraries in a single directory to enable testing
set(LIBRARY_OUTPUT_PATH ${PROJECT_BINARY_DIR}/lib)

# set compiler flags
# default GNU compiler flags:
# DEBUG           -g
# RELEASE         -O3 -DNDEBUG
# MINSIZEREL      -Os -DNDEBUG
# RELWITHDEBINFO  -O2 -g
set( CMAKE_C_FLAGS_DEBUG "-g -O0" )
set( CMAKE_C_FLAGS_RELWITHDEBINFO "-O3 -g -DNDEBUG -fno-omit-frame-pointer" )
set( CMAKE_C_FLAGS_RELEASE "-O3 -DNDEBUG" )
set( CMAKE_Fortran_FLAGS_DEBUG "-g -O0 -fno-second-underscore" )
set( CMAKE_Fortran_FLAGS_RELWITHDEBINFO "-O3 -g -DNDEBUG -fno-omit-frame-pointer -fno-second-underscore" )
set( CMAKE_Fortran_FLAGS_RELEASE "-O3 -DNDEBUG -fno-second-underscore" )

message(STATUS "CMAKE_Fortran_COMPILER_INIT = ${CMAKE_Fortran_COMPILER_INIT}")
message(STATUS "CMAKE_Fortran_COMPILER_FULLPATH = ${CMAKE_Fortran_COMPILER_FULLPATH}")
message(STATUS "CMAKE_Fortran_COMPILER = ${CMAKE_Fortran_COMPILER}")

if(NOT CMAKE_BUILD_TYPE)
  set(CMAKE_BUILD_TYPE RelWithDebInfo CACHE STRING "" FORCE)
endif()
message(STATUS "cmake build type set to ${CMAKE_BUILD_TYPE}")

message("ENV_FLAGS = $ENV{FFLAGS}")
string(TOUPPER ${CMAKE_BUILD_TYPE} BTYPE_UC )
if( ${BTYPE_UC} MATCHES "DEBUG")
  set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS_DEBUG}")
  set(CMAKE_Fortran_FLAGS "${CMAKE_Fortran_FLAGS_DEBUG}")
elseif( ${BTYPE_UC} MATCHES "RELEASE")
  set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS_RELEASE}")
  set(CMAKE_Fortran_FLAGS "${CMAKE_Fortran_FLAGS_RELEASE}")
elseif( ${BTYPE_UC} MATCHES "RELWITHDEBINFO")
  set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS_RELWITHDEBINFO}")
  set(CMAKE_Fortran_FLAGS "${CMAKE_Fortran_FLAGS_RELWITHDEBINFO}")
endif()
set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} $ENV{CFLAGS}")
set(CMAKE_Fortran_FLAGS "${CMAKE_Fortran_FLAGS} $ENV{FFLAGS}")
message("CMAKE_C_FLAGS = ${CMAKE_C_FLAGS}")
message("CMAKE_Fortran_FLAGS = ${CMAKE_Fortran_FLAGS}")

# source
# shared library
file(GLOB src_files *.c *.F *.f)
add_library(Pythia6 SHARED ${src_files})

# Installation:
# Library.
install(TARGETS Pythia6 DESTINATION lib)

# Include-able file.
install( FILES example/main60.f
         DESTINATION include )

# Documentation.
install(DIRECTORY doc DESTINATION .)

# Examples
install(DIRECTORY example DESTINATION .)

# tests
macro( pythia_test testname )
  set ( package_library_list ${PROJECT_BINARY_DIR}/lib/${CMAKE_STATIC_LIBRARY_PREFIX}CLHEP-${PACKAGE}-${VERSION}${CMAKE_STATIC_LIBRARY_SUFFIX} )
  link_libraries( Pythia6 )
  message( STATUS "building ${testname} from ${CMAKE_CURRENT_SOURCE_DIR}/example in ${CMAKE_CURRENT_BINARY_DIR}" )
  add_executable(${testname} example/${testname}.f)
  add_test( ${testname} ${CMAKE_CURRENT_BINARY_DIR}/${testname} )
endmacro( pythia_test )

pythia_test( main61 )
pythia_test( main63 )
pythia_test( main66 )
pythia_test( main67 )
pythia_test( main68 )
pythia_test( main69 )
pythia_test( main71 )
pythia_test( main72 )
pythia_test( main73 )
pythia_test( main75 )
pythia_test( main77 )
pythia_test( main78 )

# these examples take a while to run
if( run_long_tests )
  pythia_test( main62 )
  pythia_test( main64 )
  pythia_test( main65 )
  pythia_test( main70 )
  pythia_test( main74 )
  pythia_test( main79 )
endif( run_long_tests )
