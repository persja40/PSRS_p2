/* gasnet_config.h.  Generated from gasnet_config.h.in by configure.  */
/* gasnet_config.h.in.  Generated from configure.in by autoheader.  */
/*    $Source: bitbucket.org:berkeleylab/gasnet.git/acconfig.h $ */
/*  Description: GASNet acconfig.h (or config.h)                             */
/*  Copyright 2002, Dan Bonachea <bonachea@cs.berkeley.edu>                  */
/* Terms of use are as specified in license.txt */

#ifndef _INCLUDE_GASNET_CONFIG_H_
#define _INCLUDE_GASNET_CONFIG_H_
#if !defined(_IN_GASNETEX_H) && !defined(_IN_GASNET_TOOLS_H)
  #error This file is not meant to be included directly- clients should include gasnetex.h or gasnet_tools.h
#endif


#define GASNETI_BUILD_ID "Sun Apr 29 08:07:31 CEST 2018 ernest"
#define GASNETI_CONFIGURE_ARGS "'--enable-debug' '--disable-psm' '--disable-mxm' '--disable-portals4' '--disable-ofi' '--disable-parsync'"
#define GASNETI_SYSTEM_TUPLE "x86_64-unknown-linux-gnu"
#define GASNETI_SYSTEM_NAME "ernest-GP60-2PF-Leopard-Pro"
/* #undef GASNETI_CROSS_COMPILING */

/* version identifiers */
#define GASNET_RELEASE_VERSION_MAJOR 2017
#define GASNET_RELEASE_VERSION_MINOR 12
#define GASNET_RELEASE_VERSION_PATCH 0
#define GASNETI_RELEASE_VERSION 2017.12.0
#define GASNETI_SPEC_VERSION_MAJOR 1
#define GASNETI_SPEC_VERSION_MINOR 8
#define GASNETI_TOOLS_SPEC_VERSION_MAJOR 1
#define GASNETI_TOOLS_SPEC_VERSION_MINOR 11
#define GASNETI_EX_SPEC_VERSION_MAJOR 0
#define GASNETI_EX_SPEC_VERSION_MINOR 3

/* configure-detected conduits */
#define GASNETI_CONDUITS " smp udp mpi"

/* CC attributes support */
#define GASNETI_HAVE_CC_ATTRIBUTE 1
#define GASNETI_HAVE_CC_ATTRIBUTE_ALWAYSINLINE 1
#define GASNETI_HAVE_CC_ATTRIBUTE_NOINLINE 1
#define GASNETI_HAVE_CC_ATTRIBUTE_MALLOC 1
#define GASNETI_HAVE_CC_ATTRIBUTE_WARNUNUSEDRESULT 1
#define GASNETI_HAVE_CC_ATTRIBUTE_USED 1
#define GASNETI_HAVE_CC_ATTRIBUTE_MAYALIAS 1
#define GASNETI_HAVE_CC_ATTRIBUTE_NORETURN 1
#define GASNETI_HAVE_CC_ATTRIBUTE_PURE 1
#define GASNETI_HAVE_CC_ATTRIBUTE_CONST 1
#define GASNETI_HAVE_CC_ATTRIBUTE_HOT 1
#define GASNETI_HAVE_CC_ATTRIBUTE_COLD 1
#define GASNETI_HAVE_CC_ATTRIBUTE_DEPRECATED 1
#define GASNETI_HAVE_CC_ATTRIBUTE_FORMAT 1
#define GASNETI_HAVE_CC_ATTRIBUTE_FORMAT_FUNCPTR 1
#define GASNETI_HAVE_CC_ATTRIBUTE_FORMAT_FUNCPTR_ARG 1
#define GASNETI_HAVE_CC_PRAGMA_GCC_DIAGNOSTIC 1

/* CXX attributes support */
#define GASNETI_HAVE_CXX_ATTRIBUTE 1
#define GASNETI_HAVE_CXX_ATTRIBUTE_ALWAYSINLINE 1
#define GASNETI_HAVE_CXX_ATTRIBUTE_NOINLINE 1
#define GASNETI_HAVE_CXX_ATTRIBUTE_MALLOC 1
#define GASNETI_HAVE_CXX_ATTRIBUTE_WARNUNUSEDRESULT 1
#define GASNETI_HAVE_CXX_ATTRIBUTE_USED 1
#define GASNETI_HAVE_CXX_ATTRIBUTE_MAYALIAS 1
#define GASNETI_HAVE_CXX_ATTRIBUTE_NORETURN 1
#define GASNETI_HAVE_CXX_ATTRIBUTE_PURE 1
#define GASNETI_HAVE_CXX_ATTRIBUTE_CONST 1
#define GASNETI_HAVE_CXX_ATTRIBUTE_HOT 1
#define GASNETI_HAVE_CXX_ATTRIBUTE_COLD 1
#define GASNETI_HAVE_CXX_ATTRIBUTE_DEPRECATED 1
#define GASNETI_HAVE_CXX_ATTRIBUTE_FORMAT 1
#define GASNETI_HAVE_CXX_ATTRIBUTE_FORMAT_FUNCPTR 1
#define GASNETI_HAVE_CXX_ATTRIBUTE_FORMAT_FUNCPTR_ARG 1
#define GASNETI_HAVE_CXX_PRAGMA_GCC_DIAGNOSTIC 1

/* MPI_CC attributes support */
#define GASNETI_HAVE_MPI_CC_ATTRIBUTE 1
#define GASNETI_HAVE_MPI_CC_ATTRIBUTE_ALWAYSINLINE 1
#define GASNETI_HAVE_MPI_CC_ATTRIBUTE_NOINLINE 1
#define GASNETI_HAVE_MPI_CC_ATTRIBUTE_MALLOC 1
#define GASNETI_HAVE_MPI_CC_ATTRIBUTE_WARNUNUSEDRESULT 1
#define GASNETI_HAVE_MPI_CC_ATTRIBUTE_USED 1
#define GASNETI_HAVE_MPI_CC_ATTRIBUTE_MAYALIAS 1
#define GASNETI_HAVE_MPI_CC_ATTRIBUTE_NORETURN 1
#define GASNETI_HAVE_MPI_CC_ATTRIBUTE_PURE 1
#define GASNETI_HAVE_MPI_CC_ATTRIBUTE_CONST 1
#define GASNETI_HAVE_MPI_CC_ATTRIBUTE_HOT 1
#define GASNETI_HAVE_MPI_CC_ATTRIBUTE_COLD 1
#define GASNETI_HAVE_MPI_CC_ATTRIBUTE_DEPRECATED 1
#define GASNETI_HAVE_MPI_CC_ATTRIBUTE_FORMAT 1
#define GASNETI_HAVE_MPI_CC_ATTRIBUTE_FORMAT_FUNCPTR 1
#define GASNETI_HAVE_MPI_CC_ATTRIBUTE_FORMAT_FUNCPTR_ARG 1
#define GASNETI_HAVE_MPI_CC_PRAGMA_GCC_DIAGNOSTIC 1

/* identification of the C compiler used at configure time */
#define GASNETI_PLATFORM_COMPILER_IDSTR "|COMPILER_FAMILY:GNU|COMPILER_VERSION:5.4.0|COMPILER_FAMILYID:1|STD:__STDC__,__STDC_VERSION__=201112L|misc:5.4.0 20160609|"
#define GASNETI_PLATFORM_COMPILER_FAMILYID 1
#define GASNETI_PLATFORM_COMPILER_ID 1
#define GASNETI_PLATFORM_COMPILER_VERSION 328704

/* identification of the C++ compiler used at configure time */
#define GASNETI_PLATFORM_CXX_IDSTR "|COMPILER_FAMILY:GNU|COMPILER_VERSION:5.4.0|COMPILER_FAMILYID:1|STD:__STDC__,__cplusplus=199711L|misc:5.4.0 20160609|"
#define GASNETI_PLATFORM_CXX_FAMILYID 1
#define GASNETI_PLATFORM_CXX_ID 10001
#define GASNETI_PLATFORM_CXX_VERSION 328704

/* identification of the MPI C compiler used at configure time */
#define GASNETI_PLATFORM_MPI_CC_IDSTR "|COMPILER_FAMILY:GNU|COMPILER_VERSION:5.4.0|COMPILER_FAMILYID:1|STD:__STDC__,__STDC_VERSION__=201112L|misc:5.4.0 20160609|"
#define GASNETI_PLATFORM_MPI_CC_FAMILYID 1
#define GASNETI_PLATFORM_MPI_CC_ID 1
#define GASNETI_PLATFORM_MPI_CC_VERSION 328704
#define GASNETI_MPI_VERSION 3
#define HAVE_MPI_INIT_THREAD 1
#define HAVE_MPI_QUERY_THREAD 1

/* Defined to be the inline function modifier supported by the C
   compilers (if supported), prefixed by 'static' (if permitted) */
#define GASNETI_CC_INLINE_MODIFIER static inline
#define GASNETI_MPI_CC_INLINE_MODIFIER static inline

/* C, C++ and MPI_CC compilers 'restrict' keywords (or empty) */
#define GASNETI_CC_RESTRICT __restrict__
#define GASNETI_CXX_RESTRICT __restrict__
#define GASNETI_MPI_CC_RESTRICT __restrict__

/* C, C++ and MPI_CC compilers misc builtins */

/* has __assume */
/* #undef GASNETI_HAVE_CC_ASSUME */
/* #undef GASNETI_HAVE_CXX_ASSUME */
/* #undef GASNETI_HAVE_MPI_CC_ASSUME */

/* has __builtin_assume */
/* #undef GASNETI_HAVE_CC_BUILTIN_ASSUME */
/* #undef GASNETI_HAVE_CXX_BUILTIN_ASSUME */
/* #undef GASNETI_HAVE_MPI_CC_BUILTIN_ASSUME */

/* has __builtin_unreachable */
#define GASNETI_HAVE_CC_BUILTIN_UNREACHABLE 1
#define GASNETI_HAVE_CXX_BUILTIN_UNREACHABLE 1
#define GASNETI_HAVE_MPI_CC_BUILTIN_UNREACHABLE 1

/* has __builtin_expect */
#define GASNETI_HAVE_CC_BUILTIN_EXPECT 1
#define GASNETI_HAVE_CXX_BUILTIN_EXPECT 1
#define GASNETI_HAVE_MPI_CC_BUILTIN_EXPECT 1

/* has __builtin_constant_p */
#define GASNETI_HAVE_CC_BUILTIN_CONSTANT_P 1
#define GASNETI_HAVE_CXX_BUILTIN_CONSTANT_P 1
#define GASNETI_HAVE_MPI_CC_BUILTIN_CONSTANT_P 1

/* has __builtin_prefetch */
#define GASNETI_HAVE_CC_BUILTIN_PREFETCH 1
#define GASNETI_HAVE_CXX_BUILTIN_PREFETCH 1
#define GASNETI_HAVE_MPI_CC_BUILTIN_PREFETCH 1

/* Which inline asm style(s) are supported - these are defined only
   where we use configure to determine what a compiler supports */
/* #undef GASNETI_HAVE_CC_XLC_ASM */
/* #undef GASNETI_HAVE_CXX_XLC_ASM */
/* #undef GASNETI_HAVE_MPI_CC_XLC_ASM */
/* #undef GASNETI_HAVE_CC_GCC_ASM */
/* #undef GASNETI_HAVE_CXX_GCC_ASM */
/* #undef GASNETI_HAVE_MPI_CC_GCC_ASM */

/* Which non-native atomics are available */
#define GASNETI_HAVE_CC_SYNC_ATOMICS_32 1
#define GASNETI_HAVE_CXX_SYNC_ATOMICS_32 1
#define GASNETI_HAVE_MPI_CC_SYNC_ATOMICS_32 1
#define GASNETI_HAVE_CC_SYNC_ATOMICS_64 1
#define GASNETI_HAVE_CXX_SYNC_ATOMICS_64 1
#define GASNETI_HAVE_MPI_CC_SYNC_ATOMICS_64 1

/* Does CXX support C99 __VA_ARGS__ */
#define GASNETI_CXX_HAS_VA_ARGS 1

/* Defined if __PIC__ defined at configure time */
/* #undef GASNETI_CONFIGURED_PIC */

/* true iff GASNETI_RESTRICT may be applied to types which are not pointer types until after typedef expansion */
#define GASNETI_CC_RESTRICT_MAY_QUALIFY_TYPEDEFS 1
#define GASNETI_CXX_RESTRICT_MAY_QUALIFY_TYPEDEFS 1
#define GASNETI_MPI_CC_RESTRICT_MAY_QUALIFY_TYPEDEFS 1

/* have mmap() */
#define HAVE_MMAP 1

/* mmap supporting flags */
#define HAVE_MAP_NORESERVE 1
#define HAVE_MAP_ANON 1
#define HAVE_MAP_ANONYMOUS 1

/* avoid mmap()-after-munmap() failures */
/* #undef GASNETI_BUG3480_WORKAROUND */

/* --with-segment-mmap-max value (if given) */
/* #undef GASNETI_MMAP_MAX_SIZE */

/* --with-max-threads value (if given) */
/* #undef GASNETI_MAX_THREADS_CONFIGURE */

/* has clock_gettime() */
#define HAVE_CLOCK_GETTIME 1

/* has usleep() */
#define HAVE_USLEEP 1

/* has nanosleep() */
#define HAVE_NANOSLEEP 1

/* has clock_nanosleep() */
#define HAVE_CLOCK_NANOSLEEP 1

/* has nsleep() */
/* #undef HAVE_NSLEEP */

/* has sched_yield() */
#define HAVE_SCHED_YIELD 1

/* have sysctl machdep.tsc_freq */
/* #undef GASNETI_HAVE_SYSCTL_MACHDEP_TSC_FREQ */

/* has Portable Linux Processor Affinity */
#define HAVE_PLPA 1

/* have ptmalloc's mallopt() options */
#define HAVE_PTMALLOC 1

/* have declarations/definitions */
#define HAVE_SETENV_DECL 1
#define HAVE_UNSETENV_DECL 1
#define HAVE_SNPRINTF_DECL 1
#define HAVE_VSNPRINTF_DECL 1
#define HAVE_ISBLANK_DECL 1
#define HAVE_ISASCII_DECL 1
#define HAVE_TOASCII_DECL 1

/* ctype.h needs wrappers */
/* #undef GASNETI_NEED_CTYPE_WRAPPERS */

/* Forbidden to use fork(), popen() and system()? */
/* #undef GASNETI_NO_FORK */

/* building Process SHared Memory support?  For which API? */
#define GASNETI_PSHM_ENABLED 1
#define GASNETI_PSHM_POSIX 1
/* #undef GASNETI_PSHM_SYSV */
/* #undef GASNETI_PSHM_FILE */
/* #undef GASNETI_PSHM_XPMEM */
/* #undef GASNETI_PSHM_GHEAP */

/* How many cores/node must we support (255 is default) */
#define GASNETI_CONFIG_PSHM_MAX_NODES 255

/* hugetlbfs support available */
/* #undef HAVE_HUGETLBFS */

/* hugetlbfs support enabled */
/* #undef GASNETI_USE_HUGETLBFS */

/* Have Mellanox FCA support?  Where? */
/* #undef GASNET_FCA_ENABLED */
/* #undef GASNETI_FCA_HOME */

/* BLCR support, path and features */
/* #undef GASNETI_BLCR_ENABLED */

/* support for backtracing */
#define HAVE_EXECINFO_H 1
#define HAVE_BACKTRACE 1
#define HAVE_BACKTRACE_SYMBOLS 1
/* #undef HAVE_PRINTSTACK */
#define ADDR2LINE_PATH "/usr/bin/addr2line"
#define GDB_PATH "/usr/bin/gdb"
/* #undef GSTACK_PATH */
/* #undef PSTACK_PATH */
/* #undef PGDBG_PATH */
/* #undef IDB_PATH */
/* #undef DBX_PATH */
/* #undef LLDB_PATH */

/* have pthread_setconcurrency */
#define HAVE_PTHREAD_SETCONCURRENCY 1

/* has pthread_kill() */
#define HAVE_PTHREAD_KILL 1

/* has pthread_kill_other_threads_np() */
/* #undef HAVE_PTHREAD_KILL_OTHER_THREADS_NP */

/* have pthread_setconcurrency */
#define HAVE_PTHREAD_SIGMASK 1

/* has pthread rwlock support */
#define GASNETI_HAVE_PTHREAD_RWLOCK 1

/* has __thread thread-local-storage support */
#define GASNETI_HAVE_TLS_SUPPORT 1

/* force threadinfo optimization ON or OFF */
/* #undef GASNETI_THREADINFO_OPT_CONFIGURE */

/* pause instruction, if any */
#define GASNETI_PAUSE_INSTRUCTION "pause"

/* How to name MIPS assembler temporary register in inline asm, if at all */
/* #undef GASNETI_HAVE_MIPS_REG_1 */
/* #undef GASNETI_HAVE_MIPS_REG_AT */

/* has ARM kernel-level support for cmpxchg */
/* #undef GASNETI_HAVE_ARM_CMPXCHG */

/* has ARM kernel-level support for membar */
/* #undef GASNETI_HAVE_ARM_MEMBAR */

/* has usable AARCH64 (ARMV8) system counter support */
/* #undef GASNETI_HAVE_AARCH64_CNTVCT_EL0 */

/* has x86 EBX register (not reserved for GOT) */
/* #undef GASNETI_HAVE_X86_EBX */

/* has support (toolchain and cpu) for ia64 cmp8xchg16 instruction */
/* #undef GASNETI_HAVE_IA64_CMP8XCHG16 */

/* has support (toolchain and cpu) for x86_64 cmpxchg16b instruction */
#define GASNETI_HAVE_X86_CMPXCHG16B 1

/* gcc support for "U" and "h" register classes on SPARC32 */
/* #undef GASNETI_HAVE_SPARC32_64BIT_ASM */

/* has _builtin_ctz */
#define HAVE_BUILTIN_CTZ 1

/* has __func__ function name defined */
#define HAVE_FUNC 1

/* portable inttypes support */
#define HAVE_INTTYPES_H 1
#define HAVE_STDINT_H 1
#define HAVE_SYS_TYPES_H 1
#define COMPLETE_INTTYPES_H 1
#define COMPLETE_STDINT_H 1
/* #undef COMPLETE_SYS_TYPES_H */

/* Linux prctl() support */
#define HAVE_PR_SET_PDEATHSIG 1
#define HAVE_PR_SET_PTRACER 1

/* forcing use of "non-native" implementations: */
/* #undef GASNETI_FORCE_GENERIC_ATOMICOPS */
/* #undef GASNETI_FORCE_OS_ATOMICOPS */
/* #undef GASNETI_FORCE_COMPILER_ATOMICOPS */
/* #undef GASNETI_FORCE_TRUE_WEAKATOMICS */
/* #undef GASNETI_FORCE_GENERIC_SEMAPHORES */
/* #undef GASNETI_FORCE_YIELD_MEMBARS */
/* #undef GASNETI_FORCE_SLOW_MEMBARS */
/* #undef GASNETI_FORCE_GETTIMEOFDAY */
/* #undef GASNETI_FORCE_POSIX_REALTIME */

/* forcing UP build, even if build platform is a multi-processor */
/* #undef GASNETI_UNI_BUILD */

/* force memory barriers on GASNet local (loopback) puts and gets */
/* #undef GASNETI_MEMSYNC_ON_LOOPBACK */

/* throttle polling threads in multi-threaded configurations to reduce contention */
/* #undef GASNETI_THROTTLE_FEATURE_ENABLED */

/* auto-detected mmap data page size */
#define GASNETI_PAGESIZE 4096
#define GASNETI_PAGESHIFT 12

/* auto-detected shared data cache line size */
#define GASNETI_CACHE_LINE_BYTES 64
#define GASNETI_CACHE_LINE_SHIFT 6

/* udp-conduit default custom spawn command */
/* #undef GASNET_CSPAWN_CMD */

/* compiler is Sun's "gccfss" variant of GCC */
/* #undef GASNETI_GCC_GCCFSS */

/* compiler is Apple's variant of GCC */
/* #undef GASNETI_GCC_APPLE */

/* platform is an SGI Altix multiprocessor */
/* #undef GASNETI_ARCH_ALTIX */
/* #undef GASNETI_USE_MMTIMER */

/* platform is a Linux cluster running IBM PE software */
/* #undef GASNETI_ARCH_IBMPE */

/* platform is an IBM BlueGene/Q multiprocessor */
/* #undef GASNETI_ARCH_BGQ */

/* platform is Microsoft Windows Subsystem for Linux */
/* #undef GASNETI_ARCH_WSL */

/* have (potentially buggy) MIPS R10000 multiprocessor */
/* #undef GASNETI_ARCH_SGI_IP27 */

/* have working UltraSPARC ISA (lacks an associated builtin preprocessor macro) */
/* #undef GASNETI_ARCH_ULTRASPARC */

/* Have working PPC64 ISA (lacks an associated builtin preprocessor macro) */
/* #undef GASNETI_ARCH_PPC64 */

/* Type to use as socklen_t */
#define GASNET_SOCKLEN_T socklen_t

/* GASNet build configuration */
#define GASNET_DEBUG 1
/* #undef GASNET_NDEBUG */
#define GASNET_TRACE 1
#define GASNET_STATS 1
#define GASNET_DEBUGMALLOC 1
/* #undef GASNET_SRCLINES */
/* #undef GASNET_DEBUG_VERBOSE */

/* GASNet segment definition */
#define GASNET_SEGMENT_FAST 1
/* #undef GASNET_SEGMENT_LARGE */
/* #undef GASNET_SEGMENT_EVERYTHING */

/* Override to disable default segment alignment */
#define GASNETI_DISABLE_ALIGNED_SEGMENTS 1

/* GASNet smp-conduit */
#define GASNETC_HAVE_O_ASYNC 1
#define GASNETC_USE_SOCKETPAIR 1

/* GASNet {gemini,aries}-conduit settings */
/* #undef GASNETC_GNI_MAX_MEDIUM */
/* #undef GASNETC_GNI_MULTI_DOMAIN */
/* #undef GASNETC_GNI_UDREG */

/* GASNet ofi-conduit settings */
/* #undef GASNETC_OFI_MAX_MEDIUM */
/* #undef GASNETC_OFI_NUM_COMPLETIONS */
/* #undef GASNETC_OFI_HAS_MR_SCALABLE */
/* #undef GASNETC_OFI_USE_THREAD_DOMAIN */

/* GASNet ibv-conduit features and bug work-arounds */
/* #undef HAVE_IBV_SRQ */
/* #undef HAVE_IBV_TRANSPORT_TYPE */
/* #undef GASNETC_IBV_RCV_THREAD */
/* #undef GASNETC_IBV_CONN_THREAD */
/* #undef GASNETC_IBV_MAX_HCAS */
/* #undef GASNETC_IBV_PHYSMEM_MAX_CONFIGURE */
/* #undef GASNETC_IBV_PHYSMEM_PROBE_CONFIGURE */

/* GASNet mxm-conduit settings */
/* #undef GASNETC_MXM_PHYSMEM_MAX_CONFIGURE */
/* #undef GASNETC_MXM_PHYSMEM_PROBE_CONFIGURE */

/* GASNet pami-conduit settings */
/* #undef GASNETI_SIZEOF_PAMI_TASK_T */

/* GASNet bug1389 detection/work-around */
/* #undef GASNETI_BUG1389_WORKAROUND */

/* Defaults for GASNET_SSH_* env vars */
#define GASNETI_DEFAULT_SSH_CMD "ssh"
#define GASNETI_DEFAULT_SSH_OPTIONS ""
#define GASNETI_DEFAULT_SSH_NODEFILE ""
#define GASNETI_DEFAULT_SSH_OUT_DEGREE 32

/* Support for pmi-spawner */
#define HAVE_PMI_H 1
/* #undef HAVE_PMI2_H */
/* #undef GASNETI_PMI2_FENCE_IS_BARRIER */


/* Define to one of `_getb67', `GETB67', `getb67' for Cray-2 and Cray-YMP
   systems. This function is required for `alloca.c' support on those systems.
   */
/* #undef CRAY_STACKSEG_END */

/* Define to 1 if using `alloca.c'. */
/* #undef C_ALLOCA */

/* Log base 2 of the maximum size in bytes of a memory descriptor. Set to 0 if
   MD can bind all of memory. */
/* #undef GASNETC_PORTALS4_MAX_MD_SIZE */

/* Log base 2 of the maximum size in bytes of the user virtual address space.
   Set to 0 if MD can bind all of memory. */
/* #undef GASNETC_PORTALS4_MAX_VA_SIZE */

/* define to 1 if PMI2_KVS_fence() provides barrier functionality */
/* #undef GASNETI_PMI2_FENCE_IS_BARRIER */

/* Define to 1 if you have `alloca', as a function or macro. */
#define HAVE_ALLOCA 1

/* Define to 1 if you have <alloca.h> and it should be used (not on Ultrix).
   */
#define HAVE_ALLOCA_H 1

/* Define to 1 if you have the `backtrace' function. */
#define HAVE_BACKTRACE 1

/* Define to 1 if you have the `backtrace_symbols' function. */
#define HAVE_BACKTRACE_SYMBOLS 1

/* Define to 1 if you have the <execinfo.h> header file. */
#define HAVE_EXECINFO_H 1

/* Define to 1 if you have the <features.h> header file. */
#define HAVE_FEATURES_H 1

/* Define to 1 if you have the `fopen64' function. */
#define HAVE_FOPEN64 1

/* Define to 1 if you have the `fork' function. */
#define HAVE_FORK 1

/* Define to 1 if you have the `gethostid' function. */
#define HAVE_GETHOSTID 1

/* Define to 1 if you have the `getifaddrs' function. */
#define HAVE_GETIFADDRS 1

/* Define to 1 if you have the `getrlimit' function. */
#define HAVE_GETRLIMIT 1

/* Define to 1 if you have the `getrlimit64' function. */
#define HAVE_GETRLIMIT64 1

/* Define to 1 if you have the <gni_pub.h> header file. */
/* #undef HAVE_GNI_PUB_H */

/* Define to 1 if you have the <hugetlbfs.h> header file. */
/* #undef HAVE_HUGETLBFS_H */

/* Define to 1 if you have the `hugetlbfs_unlinked_fd' function. */
/* #undef HAVE_HUGETLBFS_UNLINKED_FD */

/* Define to 1 if you have the `ibv_cmd_open_xrcd' function. */
/* #undef HAVE_IBV_CMD_OPEN_XRCD */

/* Define to 1 if you have the `ibv_open_xrc_domain' function. */
/* #undef HAVE_IBV_OPEN_XRC_DOMAIN */

/* Define to 1 if you have the <ifaddrs.h> header file. */
#define HAVE_IFADDRS_H 1

/* Define to 1 if you have the <inttypes.h> header file. */
#define HAVE_INTTYPES_H 1

/* Define to 1 if you have the `isascii' function. */
#define HAVE_ISASCII 1

/* Define to 1 if you have the `isblank' function. */
#define HAVE_ISBLANK 1

/* Define to 1 if you have the <linux/mmtimer.h> header file. */
#define HAVE_LINUX_MMTIMER_H 1

/* Define to 1 if you have the <malloc.h> header file. */
#define HAVE_MALLOC_H 1

/* Define to 1 if you have the <memory.h> header file. */
#define HAVE_MEMORY_H 1

/* Define to 1 if you have the <netinet/tcp.h> header file. */
#define HAVE_NETINET_TCP_H 1

/* Define to 1 if you have the `on_exit' function. */
#define HAVE_ON_EXIT 1

/* Define to 1 if you have the `PMI_Allgather' function. */
/* #undef HAVE_PMI_ALLGATHER */

/* Define to 1 if you have the `PMI_Bcast' function. */
/* #undef HAVE_PMI_BCAST */

/* Define to 1 if you have the <pmi_cray.h> header file. */
/* #undef HAVE_PMI_CRAY_H */

/* Define to 1 if you have the `popen' function. */
#define HAVE_POPEN 1

/* Define to 1 if you have the <pthread.h> header file. */
#define HAVE_PTHREAD_H 1

/* Define to 1 if you have the `putenv' function. */
#define HAVE_PUTENV 1

/* Define to 1 if you have the `setenv' function. */
#define HAVE_SETENV 1

/* Define to 1 if you have the `setpgid' function. */
#define HAVE_SETPGID 1

/* Define to 1 if you have the `setpgrp' function. */
#define HAVE_SETPGRP 1

/* Define to 1 if you have the `setrlimit' function. */
#define HAVE_SETRLIMIT 1

/* Define to 1 if you have the `setrlimit64' function. */
#define HAVE_SETRLIMIT64 1

/* Define to 1 if you have the <sgidefs.h> header file. */
/* #undef HAVE_SGIDEFS_H */

/* Define to 1 if you have the `shmem_longlong_cswap' function. */
/* #undef HAVE_SHMEM_LONGLONG_CSWAP */

/* Define to 1 if you have the `shmem_long_cswap' function. */
/* #undef HAVE_SHMEM_LONG_CSWAP */

/* Define to 1 if you have the `shmem_long_finc' function. */
/* #undef HAVE_SHMEM_LONG_FINC */

/* Define to 1 if you have the `sigprocmask' function. */
#define HAVE_SIGPROCMASK 1

/* Define to 1 if you have the <sn/mmtimer.h> header file. */
/* #undef HAVE_SN_MMTIMER_H */

/* Define to 1 if you have the <sn/xpmem.h> header file. */
/* #undef HAVE_SN_XPMEM_H */

/* Define to 1 if you have the `srand_deterministic' function. */
/* #undef HAVE_SRAND_DETERMINISTIC */

/* Define to 1 if you have the <stdint.h> header file. */
#define HAVE_STDINT_H 1

/* Define to 1 if you have the <stdlib.h> header file. */
#define HAVE_STDLIB_H 1

/* Define to 1 if you have the <strings.h> header file. */
#define HAVE_STRINGS_H 1

/* Define to 1 if you have the <string.h> header file. */
#define HAVE_STRING_H 1

/* Define to 1 if you have the `system' function. */
#define HAVE_SYSTEM 1

/* Define to 1 if you have the <sys/param.h> header file. */
#define HAVE_SYS_PARAM_H 1

/* Define to 1 if you have the <sys/resource.h> header file. */
#define HAVE_SYS_RESOURCE_H 1

/* Define to 1 if you have the <sys/socket.h> header file. */
#define HAVE_SYS_SOCKET_H 1

/* Define to 1 if you have the <sys/sockio.h> header file. */
/* #undef HAVE_SYS_SOCKIO_H */

/* Define to 1 if you have the <sys/stat.h> header file. */
#define HAVE_SYS_STAT_H 1

/* Define to 1 if you have the <sys/table.h> header file. */
/* #undef HAVE_SYS_TABLE_H */

/* Define to 1 if you have the <sys/types.h> header file. */
#define HAVE_SYS_TYPES_H 1

/* Define to 1 if you have the <sys/uio.h> header file. */
#define HAVE_SYS_UIO_H 1

/* Define to 1 if you have the `toascii' function. */
#define HAVE_TOASCII 1

/* Define to 1 if you have the <ucontext.h> header file. */
#define HAVE_UCONTEXT_H 1

/* Define to 1 if you have the <udreg_pub.h> header file. */
/* #undef HAVE_UDREG_PUB_H */

/* Define to 1 if you have the <unistd.h> header file. */
#define HAVE_UNISTD_H 1

/* Define to 1 if you have the `unsetenv' function. */
#define HAVE_UNSETENV 1

/* Define to 1 if you have the <xpmem.h> header file. */
/* #undef HAVE_XPMEM_H */

/* Define to 1 if you have the `xpmem_make_2' function. */
/* #undef HAVE_XPMEM_MAKE_2 */

/* Define to 1 if you have the </boot/kernel.h> header file. */
/* #undef HAVE__BOOT_KERNEL_H */

/* Define to the address where bug reports for this package should be sent. */

/* Define to the full name of this package. */

/* Define to the full name and version of this package. */

/* Define to the one symbol short name of this package. */

/* Define to the home page for this package. */

/* Define to the version of this package. */

/* The PLPA symbol prefix */
#define PLPA_SYM_PREFIX gasneti_plpa_

/* Define to 1 if the `setpgrp' function takes no argument. */
#define SETPGRP_VOID 1

/* The size of `char', as computed by sizeof. */
#define SIZEOF_CHAR 1

/* The size of `double', as computed by sizeof. */
#define SIZEOF_DOUBLE 8

/* The size of `float', as computed by sizeof. */
#define SIZEOF_FLOAT 4

/* The size of `float _Complex', as computed by sizeof. */
#define SIZEOF_FLOAT__COMPLEX 8

/* The size of `int', as computed by sizeof. */
#define SIZEOF_INT 4

/* The size of `long', as computed by sizeof. */
#define SIZEOF_LONG 8

/* The size of `long double', as computed by sizeof. */
#define SIZEOF_LONG_DOUBLE 16

/* The size of `long long', as computed by sizeof. */
#define SIZEOF_LONG_LONG 8

/* The size of `short', as computed by sizeof. */
#define SIZEOF_SHORT 2

/* The size of `void *', as computed by sizeof. */
#define SIZEOF_VOID_P 8

/* The size of `_Bool', as computed by sizeof. */
#define SIZEOF__BOOL 1

/* If using the C implementation of alloca, define if you know the
   direction of stack growth for your system; otherwise it will be
   automatically deduced at runtime.
	STACK_DIRECTION > 0 => grows toward higher addresses
	STACK_DIRECTION < 0 => grows toward lower addresses
	STACK_DIRECTION = 0 => direction of growth unknown */
/* #undef STACK_DIRECTION */

/* Define to 1 if you have the ANSI C header files. */
#define STDC_HEADERS 1

/* whether byteorder is bigendian */
/* #undef WORDS_BIGENDIAN */

/* Define to `unsigned int' if <sys/types.h> does not define. */
/* #undef size_t */

/* these get us 64-bit file declarations under several Unixen */
/* they must come before the first include of features.h (included by many system headers) */
/* define them even on platforms lacking features.h */
#define _LARGEFILE64_SOURCE 1
#define _LARGEFILE_SOURCE 1
#ifdef HAVE_FEATURES_H
 #if _FORTIFY_SOURCE > 0 && __OPTIMIZE__ <= 0 /* silence an annoying MPICH/Linux warning */
#undef _FORTIFY_SOURCE
 #endif
# include <features.h>
#endif

#endif
