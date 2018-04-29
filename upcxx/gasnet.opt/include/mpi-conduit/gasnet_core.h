/*   $Source: bitbucket.org:berkeleylab/gasnet.git/mpi-conduit/gasnet_core.h $
 * Description: GASNet header for MPI conduit core
 * Copyright 2002, Dan Bonachea <bonachea@cs.berkeley.edu>
 * Terms of use are as specified in license.txt
 */

#ifndef _IN_GASNETEX_H
  #error This file is not meant to be included directly- clients should include gasnetex.h
#endif

#ifndef _GASNET_CORE_H
#define _GASNET_CORE_H

#include <ammpi.h>

#include <gasnet_core_help.h>

/*  TODO enhance AMMPI to support thread-safe MPI libraries */
/*  TODO add MPI bypass to loopback messages */

/* ------------------------------------------------------------------------------------ */
/*
  Initialization
  ==============
*/

extern void gasnetc_exit(int exitcode) GASNETI_NORETURN;
GASNETI_NORETURNP(gasnetc_exit)
#define gasnet_exit gasnetc_exit

/* Some conduits permit gasnet_init(NULL,NULL).
   Define to 1 if this conduit supports this extension, or to 0 otherwise.  */
#if (GASNETI_MPI_VERSION >= 2)
  #define GASNET_NULL_ARGV_OK 1
#else
  #define GASNET_NULL_ARGV_OK 0
#endif
/* ------------------------------------------------------------------------------------ */
extern int gasnetc_Client_Init(
                gex_Client_t           *client_p,
                gex_EP_t               *ep_p,
                gex_TM_t               *tm_p,
                const char             *clientName,
                int                    *argc,
                char                   ***argv,
                gex_Flags_t            flags);
// gasnetex.h handles name-shifting of gex_Client_Init()

extern int gasnetc_Segment_Attach(
                gex_Segment_t          *segment_p,
                gex_TM_t               tm,
                uintptr_t              length);
#define gex_Segment_Attach gasnetc_Segment_Attach

extern int gasnetc_EP_Create(
                gex_EP_t                *ep_p,
                gex_Client_t            client,
                gex_Flags_t             flags);
#define gex_EP_Create gasnetc_EP_Create

extern int gasnetc_EP_RegisterHandlers(
                gex_EP_t                ep,
                gex_AM_Entry_t          *table,
                size_t                  numentries);
#define gex_EP_RegisterHandlers gasnetc_EP_RegisterHandlers
/* ------------------------------------------------------------------------------------ */
/*
  Handler-safe locks
  ==================
*/
#if GASNETC_HSL_ERRCHECK
  /* "magic" tag bit patterns that let us probabilistically detect
     the attempted use of uninitialized locks, or re-initialization of locks
   */
  #define GASNETC_HSL_ERRCHECK_TAGINIT ((uint64_t)0x5C9B5F7E9272EBA5ULL)
  #define GASNETC_HSL_ERRCHECK_TAGDYN  ((uint64_t)0xB82F6C0DE19C8F3DULL)
#endif

typedef struct gasneti_hsl_s {
  gasneti_mutex_t lock;

  #if GASNETI_STATS_OR_TRACE
    gasneti_tick_t acquiretime;
  #endif

  #if GASNETC_HSL_ERRCHECK
    uint64_t tag;
    int islocked;
    gasneti_tick_t timestamp;
    struct gasneti_hsl_s *next;
  #endif
} gex_HSL_t;

#if GASNETI_STATS_OR_TRACE
  #define GASNETC_LOCK_STAT_INIT ,0 
#else
  #define GASNETC_LOCK_STAT_INIT  
#endif

#if GASNETC_HSL_ERRCHECK
  #define GASNETC_LOCK_ERRCHECK_INIT , GASNETC_HSL_ERRCHECK_TAGINIT, 0, 0, NULL
#else
  #define GASNETC_LOCK_ERRCHECK_INIT 
#endif

#define GEX_HSL_INITIALIZER { \
  GASNETI_MUTEX_INITIALIZER      \
  GASNETC_LOCK_STAT_INIT         \
  GASNETC_LOCK_ERRCHECK_INIT     \
  }

/* decide whether we have "real" HSL's */
#if GASNETI_THREADS ||                           /* need for safety */ \
    GASNET_DEBUG || GASNETI_STATS_OR_TRACE       /* or debug/tracing */
  #ifdef GASNETC_NULL_HSL 
    #error bad defn of GASNETC_NULL_HSL
  #endif
#else
  #define GASNETC_NULL_HSL 1
#endif

#if GASNETC_NULL_HSL
  /* HSL's unnecessary - compile away to nothing */
  #define gex_HSL_Init(hsl)
  #define gex_HSL_Destroy(hsl)
  #define gex_HSL_Lock(hsl)
  #define gex_HSL_Unlock(hsl)
  #define gex_HSL_Trylock(hsl)	GASNET_OK
#else
  extern void gasnetc_hsl_init   (gex_HSL_t *hsl);
  extern void gasnetc_hsl_destroy(gex_HSL_t *hsl);
  extern void gasnetc_hsl_lock   (gex_HSL_t *hsl);
  extern void gasnetc_hsl_unlock (gex_HSL_t *hsl);
  extern int  gasnetc_hsl_trylock(gex_HSL_t *hsl) GASNETI_WARN_UNUSED_RESULT;

  #define gex_HSL_Init    gasnetc_hsl_init
  #define gex_HSL_Destroy gasnetc_hsl_destroy
  #define gex_HSL_Lock    gasnetc_hsl_lock
  #define gex_HSL_Unlock  gasnetc_hsl_unlock
  #define gex_HSL_Trylock gasnetc_hsl_trylock
#endif

#if GASNET_PSHM && GASNETC_HSL_ERRCHECK && !GASNETC_NULL_HSL
  extern void gasnetc_enteringHandler_hook_hsl(int cat, int isReq, int handlerId, gex_Token_t token,
                                               void *buf, size_t nbytes, int numargs,
                                               gex_AM_Arg_t *args);
  extern void gasnetc_leavingHandler_hook_hsl(int cat, int isReq);

  #define GASNETC_ENTERING_HANDLER_HOOK gasnetc_enteringHandler_hook_hsl
  #define GASNETC_LEAVING_HANDLER_HOOK  gasnetc_leavingHandler_hook_hsl
#endif


/* ------------------------------------------------------------------------------------ */
/*
  Active Message Size Limits
  ==========================
*/

#define gex_AM_MaxArgs()            ((unsigned int)AM_MaxShort())
#if GASNET_PSHM
  #define gex_AM_LUBRequestMedium() ((size_t)MIN(AM_MaxMedium(), GASNETI_MAX_MEDIUM_PSHM))
  #define gex_AM_LUBReplyMedium()   ((size_t)MIN(AM_MaxMedium(), GASNETI_MAX_MEDIUM_PSHM))
#else
  #define gex_AM_LUBRequestMedium() ((size_t)AM_MaxMedium())
  #define gex_AM_LUBReplyMedium()   ((size_t)AM_MaxMedium())
#endif
#define gex_AM_LUBRequestLong()     ((size_t)AM_MaxLong())
#define gex_AM_LUBReplyLong()       ((size_t)AM_MaxLong())

  // TODO-EX: Can these be improved upon, at least for PSHM case
#define gex_AM_MaxRequestMedium(tm,rank,lc_opt,flags,nargs) gex_AM_LUBRequestMedium()
#define gex_AM_MaxReplyMedium(tm,rank,lc_opt,flags,nargs)   gex_AM_LUBReplyMedium()
#define gex_AM_MaxRequestLong(tm,rank,lc_opt,flags,nargs)   gex_AM_LUBRequestLong()
#define gex_AM_MaxReplyLong(tm,rank,lc_opt,flags,nargs)     gex_AM_LUBReplyLong()

/* ------------------------------------------------------------------------------------ */
/*
  Misc. Active Message Functions
  ==============================
*/

#define GASNET_BLOCKUNTIL(cond) gasneti_polluntil(cond)

/* ------------------------------------------------------------------------------------ */

#endif

#include <gasnet_ammacros.h>
