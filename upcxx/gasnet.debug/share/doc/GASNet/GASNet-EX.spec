// This is *not* a final normative document.
// This is "beta documentation" for a beta release.
//
// It is a place for collection of agreed-upon APIs and for initial
// drafting of what may become the normative text.
//
// This document assumes a reasonable degree of familiarity with the current
// (aka GASNet-1) specification: http://gasnet.lbl.gov/dist/docs/gasnet.pdf
//
// Except where otherwise noted, all definitions in this document
// are provided by gasnetex.h.


//
// Specification and release versioning:
//

// Release version tuple
//
// This takes the form YEAR.MONTH.PATCH in GASNet-EX releases,
// providing a clear distinction from GASNet-1 with MAJOR==1.
#define GASNET_RELEASE_VERSION_MAJOR 2017
#define GASNET_RELEASE_VERSION_MINOR 12
#define GASNET_RELEASE_VERSION_PATCH 0

// Major and Minor versions of the GASNet-EX specification.
//
// This is currently a version number for *this* document.
#define GEX_SPEC_VERSION_MAJOR 0
#define GEX_SPEC_VERSION_MINOR 3

// Major and Minor versions of the GASNet-1 specification.
//
// This is the version to which the gasnet_* APIs adhere
// and which prevails for all matters which this document
// does not (yet) address.
#define GASNET_SPEC_VERSION_MAJOR 1
#define GASNET_SPEC_VERSION_MINOR 8

// Major and Minor versions of the GASNet-Tools specification.
//
// This is the spec version for the GASNet Tools
#define GASNETT_SPEC_VERSION_MAJOR 1
#define GASNETT_SPEC_VERSION_MINOR 11

//
// Relationship to GASNet-1 APIs:
//
// This release should continue to support nearly all GASNet-1 APIs,
// provided the client #includes <gasnet.h>, which implements the
// GASNet-1 APIs in terms of the new GASNet-EX interfaces.
// The following GASNet-1 APIs are the only ones known *not* to be
// supported in this release:
//   gasnet_memset()
//   gasnet_memset_nb()
//   gasnet_memset_nbi()
//
// Most gasnet_ APIs have gex_ counterparts that are either interoperable,
// or which provide a superset of the most closely-related gasnet_ APIs.
//
// Where a gex_/GEX_ identifier is interoperable or synonymous with
// a gasnet_/GASNET_ identifier, that is noted below.
//
// This document includes the annotation [UNIMPLEMENTED] in several places
// where we feel we have a suitable design ready for consideration, but
// have yet to provide a complete and/or correct implementation.
//
// This document includes the annotation [EXPERIMENTAL] in several places
// where we feel we have a suitable design and an implementation which is
// sufficiently complete to be used.  However, based on feedback received
// from early use, the design may change in non-trivial ways (to the degree
// that client code may need to change).


// Hybrid/transitional client support:
//
// To enable clients that mix GASNet-1 and GASNet-EX, the following API is
// provided to allow jobs that initialize GASNet using the legacy
// gasnet_init()/gasnet_attach() API to access the four key GASNet-EX objects
// created by those operations.  The types and usage of these objects are
// described below.  This call is defined in gasnet.h (not gasnetex.h).
//
// The arguments are all pointers to locations for outputs, each of which
// may be NULL if the caller does not need a particular value.
//
//     client_p: receives the gex_Client_t created implicitly by gasnet_init()
//   endpoint_p: receives the gex_EP_t created implicitly by gasnet_init()
//         tm_p: receives the gex_TM_t created implicitly by gasnet_init()
//    segment_p: receives the gex_Segment created implicitly by gasnet_attach()
//
extern void gasnet_QueryGexObjects(gex_Client_t      *client_p,
                                   gex_EP_t          *endpoint_p,
                                   gex_TM_t          *tm_p,
                                   gex_Segment_t     *segment_p);

//
// Basic types:
//

// Rank

// A "rank" is a position within a team
// Guaranteed to be an unsigned integer type
// This type is interoperable with gasnet_node_t
typedef [some unsigned integer type] gex_Rank_t;

// Pre-defined constant used to indicate "not a rank".
// Use may have different semantics in various contexts.
// Guaranteed to be larger than any valid rank.
// However, a specific value is NOT defined by specification.
// In particular, might NOT be equal to GASNET_MAXNODES
#define GEX_RANK_INVALID ((gex_Rank_t)???)

// "Job rank":
// In a non-resilient build this will be the same as the rank in the team
// constructed by gex_Client_Init() and will be identical across clients.
// This is semantically equivalent to gasnet_mynode().
//
// Semantics in a resilient build will be defined in a later release.
gex_Rank_t gex_System_QueryJobRank(void);

// "Job size":
// In a non-resilient build this will be the same as the size in the team
// constructed by gex_Client_Init() and will be identical across clients.
// This is semantically equivalent to gasnet_nodes().
//
// Semantics in a resilient build will be defined in a later release.
gex_Rank_t gex_System_QueryJobSize(void);


// Events

// An "Event" is an opaque scalar type, representing a handle
// to an asynchronous event that will be generated by a pending operation.
// Events are a generalization of GASNet-1 handles, in that 
// a single non-blocking operation may expose several events
// associated with its progress (eg local and remote completion).
// Initiation of a event-based (NB-suffix) non-blocking operation will
// usually generate one root event (representing the completion
// of the entire operation), and zero or more leaf events 
// (representing completion of intermediate steps).
// Root events must eventually be synchronized by passing them
// to an Wait or successful Test function, which recycles all the
// events associated with the operation in question.
// Leaf events may optionally be synchronized before that point.
// This type is interoperable with gasnet_handle_t
// - Sync operation: test/wait w/ one/all/some flavors
//   + Success consumes the event
typedef ... gex_Event_t;

// Pre-defined output values of type gex_Event_t
// - GEX_EVENT_INVALID
//   + result for already-completed operation
//   + synonymous with GASNET_INVALID_HANDLE
// - GEX_EVENT_NO_OP
//   + result for a failed communication attempt (eg immediate-mode
//     injection that encountered backpressure)
//   + Erroneous to pass this value to test/wait operations
#define GEX_EVENT_INVALID      ((gex_Event_t)(uintptr_t)0)
#define GEX_EVENT_NO_OP        ((gex_Event_t)(uintptr_t)???)

// Pre-defined input values of type gex_Event_t*
// These are passed to communication injection operations
// in place of a pointer to an actual gex_Event_t for certain leaf
// events, to forgo an independent leaf event and instead request
// specific predefined behavior:
// - GEX_EVENT_NOW
//   + Pass to require completion of the leaf event before returning
//     from the initiation call
// - GEX_EVENT_DEFER
//   + Pass to allow deferring completion of the leaf event to as late 
//     as completion of the root event
// - GEX_EVENT_GROUP
//   + Pass to NBI initiation calls to allow client to use NBI-based
//     calls to detect event completion (or to use an explicit event
//     returned/generated by gex_NBI_EndAccessRegion()).
#define GEX_EVENT_NOW    ((gex_Event_t*)(uintptr_t)???)
#define GEX_EVENT_DEFER  ((gex_Event_t*)(uintptr_t)???)
#define GEX_EVENT_GROUP  ((gex_Event_t*)(uintptr_t)???)


// Integer flag type used to pass hints/assertions/modifiers to various functions
// Flag value bits to a given API are guaranteed to be disjoint, although
// flag values used for unrelated functions might share bits.
typedef [some integer type] gex_Flags_t;

//
// Flags for point-to-point communication initiation
//
//
// IMMEDIATE
//
// This flag indicates that GASNet-EX *may* return without initiating
// any communication if the conduit could determine that it would
// need to block temporarily to obtain the necessary resources.  In
// this case calls with return type 'gex_Event_t' return
// GEX_EVENT_NO_OP while those with return type 'int' will
// return non-zero.
//
// Additionally, calls with this flag are not required to make any
// progress toward recovery of the "necessary resources".  Therefore,
// clients should not assume that repeated calls with this flag will
// eventually succeed.  In the presence of multiple threads, it is
// even possible that calls with this flag may never succeed due to
// racing for resources.
//
#define GEX_FLAG_IMMEDIATE ((gex_Flags_t)???)
//
// LC_COPY_{YES,NO}
//
// This mutually-exclusive pair of flags *may* override GASNet-EX's
// choice of whether or not to make a copy of a source payload (of a
// non-blocking Put or AM) for the purpose of accelerating local
// completion.  In the absence of these flags the conduit-specific
// logic will apply.
//
// NOTE: these need more thought w.r.t. the implementation and
// specification
#define GEX_FLAG_LC_COPY_YES ((gex_Flags_t)???) [UNIMPLEMENTED]
#define GEX_FLAG_LC_COPY_NO  ((gex_Flags_t)???) [UNIMPLEMENTED]

// SEGMENT DISPOSITION
//
// The following family of flags assert the segment disposition of 
// address ranges provided to communication initiation operations.
//
// The segment disposition flags come in two varieties:
//
// SELF - describes the segment disposition of addresses associated
//        with local memory and the initiating endpoint (ie the EP 
//        which is usually implicitly named by a gex_TM_t argument).
//        Eg in a Put operation this variety describes source locations,
//        and in a Get this variety describes destination locations.
//
// PEER - describes the segment disposition of addresses associated
//        with (potentially) remote memory and the peer endpoint(s)
//        (the EPs usually explicitly named by gex_Rank_t arguments)
//        Eg in a Put operation this variety describes destination locations,
//        and in a Get this variety describes source locations.
//
// The following flags are mutually exclusive within each variety -
// a given operation may specify at most one SELF flag and one PEER flag.
// Unless otherwise noted, the default behavior for each variety in the
// absence of an explicitly provided flag corresponds to:
//    GEX_FLAG_SELF_SEG_UNKNOWN, GEX_FLAG_PEER_SEG_BOUND
// which is backwards-compatible with GASNet-1 segment behavior.
// NOTE: the flags below are currently [UNIMPLEMENTED], and consequently
// these defaults are also the only supported settings for all APIs.
//
// Each explicit flag has a distinct bit pattern.
// Unless otherwise noted, the caller is responsible for ensuring the
// assertions expressed by these flags to a given call remain true for 
// the entire period of time that the described address sequences are "active" 
// with respect to the operation requested by the call. The definition of
// "active" varies based on call type, but generally extends from entry to
// the call accepting the assertions until completion is signalled for 
// all described address ranges.
//
// {SELF,PEER}_SEG_UNKNOWN
//
// These flag bits indicate that the corresponding address range(s)
// are not known by the caller to reside within current GASNet-EX segments.
// Example 1: the address ranges are known to lie partially or entirely
//   outside any segments in the process hosting the respective endpoint(s).
// Example 2: the caller lacks information about the segment disposition
//   of the address ranges, and passes this flag to reflect a lack of
//   such assertions and request maximally permissive behavior
//   (potentially incurring a performance cost).
#define GEX_FLAG_SELF_SEG_UNKNOWN ((gex_Flags_t)???) [UNIMPLEMENTED]
#define GEX_FLAG_PEER_SEG_UNKNOWN ((gex_Flags_t)???) [UNIMPLEMENTED]
//
// {SELF,PEER}_SEG_SOME
//
// These flag bits assert that the corresponding address range(s)
// are contained entirely within the union of current GASNet-EX segments
// created by any client in the process hosting the respective endpoint.
#define GEX_FLAG_SELF_SEG_SOME    ((gex_Flags_t)???) [UNIMPLEMENTED]
#define GEX_FLAG_PEER_SEG_SOME    ((gex_Flags_t)???) [UNIMPLEMENTED]
//
// {SELF,PEER}_SEG_BOUND
//
// These flag bits assert that the corresponding address range(s)
// are contained entirely within the segment bound to the respective endpoint.
// Implies that the respective endpoint has a bound segment.
#define GEX_FLAG_SELF_SEG_BOUND   ((gex_Flags_t)???) [UNIMPLEMENTED]
#define GEX_FLAG_PEER_SEG_BOUND   ((gex_Flags_t)???) [UNIMPLEMENTED]
//
// {SELF,PEER}_SEG_OFFSET
//
// These flag bits indicate that the corresponding address argument(s)
// are byte *offsets* relative to the bound segment base address.
// Implies that the respective endpoint has a bound segment, and
// that the specified range(s) are contained entirely within that segment.
#define GEX_FLAG_SELF_SEG_OFFSET  ((gex_Flags_t)???) [UNIMPLEMENTED]
#define GEX_FLAG_PEER_SEG_OFFSET  ((gex_Flags_t)???) [UNIMPLEMENTED]

// A "token" is an opaque scalar type
// This type is interoperable with gasnet_token_t
typedef ... gex_Token_t;

// Handler index - a fixed-width integer type, used to name an AM handler
// This type is interoperable with gasnet_handler_t
typedef uint8_t gex_AM_Index_t;

// Handler argument - a fixed-width integer type, used for client-defined handler arguments
// This type is interoperable with gasnet_handlerarg_t
typedef int32_t gex_AM_Arg_t;

// Handler function pointer type
typedef ... gex_AM_Fn_t;

// Widest scalar and width
// This type is interoperable with gasnet_register_value_t
typedef [some unsigned integer type] gex_RMA_Value_t;

// Preprocess-time constant size of gex_RMA_Value_t
// Synonymous with SIZEOF_GASNET_REGISTER_VALUE_T
#define SIZEOF_GEX_RMA_VALUE_T ...

// Memvec
// A "memvec" describes a tuple of memory address and length
// gex_Memvec_t is guaranteed to have the same in-memory representation as gasnet_memvec_t;
// these two struct types name their fields differently so they are technically 
// incompatible as far as the compiler is concerned -- it *is* safe to type-pun 
// pointers to them with explicit casts.
typedef struct {
  void  *gex_addr;  // [EXPERIMENTAL]: will eventually have type gex_Addr_t
  size_t gex_len;
} gex_Memvec_t;

// gex_EP_t is an opaque scalar handle to an Endpoint (EP),
// a local representative of an isolated communication context
typedef ... gex_EP_t;

// gex_Client_t is an opaque scalar handle to a Client,
// an instance of the client interface to the GASNet library
typedef ... gex_Client_t;

// gex_Segment_t is an opaque scalar handle to a Segment,
// a local client-declared memory range for use in communication
typedef ... gex_Segment_t;

// Pre-defined value of type gex_Segment_t
// Used, for instance, to indicate no bound segment
#define GEX_SEGMENT_INVALID ((gex_Segment_t)(uintptr_t)0)

// gex_TM_t is an opaque scalar handle to a Team Member,
// a collective communication context used for remote endpoint naming.
// A gex_TM_t specifies both an ordered set of Endpoints (local or remote),
// and a local gex_EP_t, a local representative of that team.
typedef ... gex_TM_t;

//
// Client-Data (CData)
//
// The major opaque object types in GASNet-EX provide the means for the client
// to set and retrieve one void* field of client-specific data for each object
// instance, which is NULL for newly created objects.

void  gex_Client_SetCData(gex_Client_t client, const void *val);
void* gex_Client_QueryCData(gex_Client_t client);
void  gex_Segment_SetCData(gex_Segment_t seg, const void *val);
void* gex_Segment_QueryCData(gex_Segment_t seg);
void  gex_TM_SetCData(gex_TM_t tm, const void *val);
void* gex_TM_QueryCData(gex_TM_t tm);
void  gex_EP_SetCData(gex_EP_t ep, const void *val);
void* gex_EP_QueryCData(gex_EP_t ep);

//
// Operations on gex_Client_t
//

// Query flags passed to gex_Client_Init()
gex_Flags_t  gex_Client_QueryFlags(gex_Client_t client);

// Query client name passed to gex_Client_Init()
const char * gex_Client_QueryName(gex_Client_t client);

// Initialize the client
// Must be called collectively by all processes comprising this GASNet job.
// Currently supports only one call per job.
// * clientName must be a unique string used to identify this client, and
//    should match the pattern: [A-Z][A-Z0-9_]+
//   In future release this string will be used in such contexts as error messages
//   and naming of environment variables to control per-client aspects of GASNet.
// * argc/argv are optional references to the command-line arguments received by main().
//   They are permitted to both be NULL, but providing them may improve portability or
//   supplementary services.
// * client_p, ep_t and tm_p are OUT parameters that receive references to the
//   newly-created Client, the primordial (thread-safe) Endpoint for this process/client,
//   and the primordial Team (which contains all the primordial Endpoints, one
//   for every process in this job).
// * flags control the creation of the primordial objects, and must currently be 0
extern int gex_Client_Init(
                gex_Client_t           *client_p,
                gex_EP_t               *ep_p,
                gex_TM_t               *tm_p,
                int                    *argc,
                char                   ***argv,
                const char             *clientName,
                gex_Flags_t            flags);

//
// Operations on gex_Segment_t
//
// NOTE: currently gex_Segment_Attach() is the only way to create a segment.
// However, additional APIs for segment creation will be added.
//

// Query owning client
gex_Client_t gex_Segment_QueryClient(gex_Segment_t seg);

// Query flags passed when segment was created
// There are no segment flags defined in the current release.
gex_Flags_t  gex_Segment_QueryFlags(gex_Segment_t seg);

// Query address and length of a segent
void *       gex_Segment_QueryAddr(gex_Segment_t seg);
uintptr_t    gex_Segment_QuerySize(gex_Segment_t seg);

// Query addresses and length of a (possibly remote) bound segment [EXPERIMENTAL]
//
// This query takes a gex_TM_t and gex_Rank_t, which together name an endpoint.
// The remaining arguments are pointers to locations for outputs, each of which
// may be NULL if the caller does not need a particular value.
//
// If the endpoint named by (rm, rank) does not have a bound segment, this call
// returns non-zero, and the output locations are unmodified.  Otherwise, this
// call returns 0 and writes the corresponding segment properties to each of
// the non-NULL output locations as follows:
//
//   owneraddr_p: receives the address of the segment in the address space
//                of the process which owns the segment.
//   localaddr_p: receives the address of the segment in the address space
//                of the calling process, if mapped, and NULL otherwise.
//   size_p:      receives the length of the segment.
//
// In this release the gex_Segment_Attach call (below) is the only mechanism to
// create segments, and unconditionally binds them to an endpoint.  Thus all
// segments are "bound" in the current release.  However, not all endpoints may
// have a segment bound to them.
//
// rank == GEX_RANK_INVALID is *not* permitted.
// rank == gex_TM_QueryRank(tm) *is* permitted.
//
// For rank != gex_TM_QueryRank(tm), this query MAY communicate.
// This call is not legal in contexts which prohibit communication, including
// (but is limited to) AM Handler context or when holding an HSL.
int gex_Segment_QueryBound(
                gex_TM_t    tm,
                gex_Rank_t  rank,
                void        **owneraddr_p,
                void        **localaddr_p,
                uintptr_t   *size_p);

// Collective allocation and creation of Segments
// Analogous to gasnet_attach
// Must be called collectively over tm.
// The current release allows up to one call per process.
// * length is the size of the local segment to allocate and bind to the
//   local Endpoint represented by tm. length is permitted to differ 
//   across team members, and must be in [0 .. gasnet_getMaxLocalSegmentSize()].
extern int gex_Segment_Attach(
                gex_Segment_t          *segment_p,
                gex_TM_t               tm,
                uintptr_t              length);

//
// Operations on gex_TM_t
// NOTE: currently gex_Client_Init() is the only way to create a TM.
// However, additional APIs for TM creation will be added.
//

// Query owning client
gex_Client_t gex_TM_QueryClient(gex_TM_t tm);

// Query corresponding endpoint
gex_EP_t     gex_TM_QueryEP(gex_TM_t tm);

// Query flags passed when tm was created
gex_Flags_t  gex_TM_QueryFlags(gex_TM_t tm);

// Query rank of team member, and size of team
gex_Rank_t   gex_TM_QueryRank(gex_TM_t tm);
gex_Rank_t   gex_TM_QuerySize(gex_TM_t tm);

//
// Operations on gex_EP_t
// NOTE: currently gex_Client_Init() is the only way to create an EP.
// However, additional APIs for EP creation will be added.
//

// Query owning client
gex_Client_t  gex_EP_QueryClient(gex_EP_t ep);

// Query flags passed when ep was created
gex_Flags_t   gex_EP_QueryFlags(gex_EP_t ep);

// Query the bound segment
// Newly-created EPs have no bound segment and will yield GEX_SEGMENT_INVALID.
gex_Segment_t gex_EP_QuerySegment(gex_EP_t ep);

// Create an endpoint [UNIMPLEMENTED]
extern int gex_EP_Create(
                gex_EP_t                *ep_p,
                gex_Client_t            client,
                gex_Flags_t             flags);

// Minimum permitted fixed index for AM handler registration.
// Applies to both gasnet_attach() and gex_EP_RegisterHandlers().
// An integer constant, guaranteed to be 128 or less.
#define GEX_AM_INDEX_BASE ???

// Client-facing type for describing one AM handler
// This type is an alternative to (*not* interchangeable with) gasnet_handlerentry_t
//
// gex_index may either be in the range [GEX_AM_INDEX_BASE .. 255] to register
// at a fixed index, or 0 for "don't care" (see gex_EP_RegisterHandlers() for
// more information on this case).
typedef struct {
    gex_AM_Index_t          gex_index;     // 0 or in [GEX_AM_INDEX_BASE .. 255]
    gex_AM_Fn_t             gex_fnptr      // Pointer to the handler on this process
    gex_Flags_t             gex_flags;     // Incl. required S/M/L and REQ/REP, see below
    unsigned int            gex_nargs;     // Required in [0 .. gex_AM_MaxArgs()]

    // Optional fields (both are "shallow copy")
    const void             *gex_cdata;     // Available to handler
    const char             *gex_name;      // Used in debug messages
} gex_AM_Entry_t;

// Required flags for gex_flags field when registering AM handlers.
//
// When registering AM handlers, the gex_flags field of each
// gex_AM_Entry_t must indicate how the handler may be called.
// This requires ORing one constant from each of the following
// two groups.

// AM Category Flags:
#define GEX_FLAG_AM_SHORT      ??? // Called only as a Short
#define GEX_FLAG_AM_MEDIUM     ??? // Called only as a Medium
#define GEX_FLAG_AM_LONG       ??? // Called only as a Long
#define GEX_FLAG_AM_MEDLONG    ??? // Called as a Medium or Long

// AM Request/Reply Flags:
#define GEX_FLAG_AM_REQUEST    ??? // Called only as a Request
#define GEX_FLAG_AM_REPLY      ??? // Called only as a Reply
#define GEX_FLAG_AM_REQREP     ??? // Called as a Request or Reply

// gex_EP_RegisterHandlers()
//
// Registers a client-provided list of AM handlers with the given EP, with
// semantics similar to gasnet_attach().  However, unlike gasnet_attach()
// this function is not collective and does not include an implicit barrier.
// Therefore the client must provide for any synchronization required to
// ensure handlers are registered before any process may send a corresponding
// AM to the Endpoint.
//
// May be called multiple times on the same Endpoint to incrementally register handlers.
// Like gasnet_attach() the handler indices specified in the table (other than
// "don't care" zero indices) must be unique.  That now extends across multiple
// calls on the same gex_EP_t (though provisions to selectively relax this
// restriction are planned for a later release).
//
// Registration of handlers via a call to gasnet_attach() does *not* preclude
// use of this function to register additional handlers.
//
// As in GASNet-1, handlers with a handler index (gex_index) of 0 on entry are
// assigned values by GASNet after the non-zero (fixed index) entries have been
// registered.  While GASNet-1 leaves the algorithm for the assignment
// unspecified (only promising that it is deterministic) this specification
// guarantees that entries with gex_index==0 are processed in the same order
// they appear in 'table' and are assigned the highest-numbered index which is
// then still unallocated (where 255 is the highest possible).
// Updating of gex_index fields that were passed as 0 upon input is the only
// modification this function will perform upon the contents of 'table'
// (whose elements are otherwise treated as const-qualified by this call).
// Upon return from this function, the relevant information from 'table'
// has been copied into storage internal to the endpoint implementation,
// and the client is permitted to overwrite or free the contents of 'table'.
//
// If any sequence of calls attempts register a total of more than (256 -
// GEX_AM_INDEX_BASE) handlers to a single gex_EP_t, the result is undefined
//
// Returns: GASNET_OK == 0 on success
int gex_EP_RegisterHandlers(
        gex_EP_t                ep,
        gex_AM_Entry_t          *table,
        size_t                  numentries);

//
// Active Message (AM) limit queries
//

// Maximum number of supported AM arguments
// Semantically identical to gasnet_AMMaxArgs()
unsigned int gex_AM_MaxArgs(void);

// Max fixed-payload queries for specific peer, nargs, lc_opt and flags
// rank == GEX_RANK_INVALID means not asking about a specific rank - yields min-of-maxes
// The result of each query function is guaranteed to be symmetric - ie
// 1. if two team members execute a given query on each other's ranks, with all
//    other input arguments being equal, the queries are guaranteed to return the 
//    same value. Note this does NOT imply any relationship between the results of
//    different query functions (eg MaxRequestMedium versus MaxReplyMedium).
// 2. if rank == GEX_RANK_INVALID, then all team members are guaranteed
//   to get the same result given the same values of the other input arguments.
// 3. 'nargs' must be between 0 and gex_AM_MaxArgs(), inclusive.
// 4. 'lc_opt' indicates the payload local completion option to be used for the AM injection in question,
//    and should be either GEX_EVENT_NOW, GEX_EVENT_GROUP (Requests only), or NULL to indicate
//    gex_Event_t-based AM local completion.
// 5. 'flags' indicates the flags that will be provided to the corresponding AM
//    Request/Reply injection function (not to be confused with the handler registration flags).
// The result is guaranteed to be stable - ie for the same set of input arguments,
// it will always return the same value.
// Aside from the explicit guarantees above, the result may otherwise vary with the 
// input arguments in unspecified ways, and thus only defines the fixed-payload limit
// for an injection call with corresponding values of (tm, rank, lc_opt, flags and numargs).
// For example, limits may vary between different pairs of ranks on the same team, or even
// between the same pair of processes linked via different team or client.
size_t gex_AM_MaxRequestLong(
           gex_TM_t tm,
           gex_Rank_t rank,
           gex_Event_t *lc_opt,
           gex_Flags_t flags,
           unsigned int numargs);
size_t gex_AM_MaxReplyLong(
           gex_TM_t tm,
           gex_Rank_t rank,
           gex_Event_t *lc_opt,
           gex_Flags_t flags,
           unsigned int numargs);
size_t gex_AM_MaxRequestMedium(
           gex_TM_t tm,
           gex_Rank_t rank,
           gex_Event_t *lc_opt,
           gex_Flags_t flags,
           unsigned int numargs);
size_t gex_AM_MaxReplyMedium(
           gex_TM_t tm,
           gex_Rank_t rank,
           gex_Event_t *lc_opt,
           gex_Flags_t flags,
           unsigned int numargs);

// Least-upper-bound fixed-payload queries (unknown team/peer, nargs, lc_opt and flags)
// Guaranteed to be less than or equal to the result of the corresponding AM_Max* 
// function, for all valid input parameters to that function.
// The result of all four queries is guaranteed to be at least 512 (bytes).
// These functions correspond semantically to the gasnet_AMMax*() queries in GASNet-1,
// which return a globally conservative maximum.
size_t gex_AM_LUBRequestLong(void);
size_t gex_AM_LUBReplyLong(void);
size_t gex_AM_LUBRequestMedium(void);
size_t gex_AM_LUBReplyMedium(void);


//
// AM Token Info
//

// Struct type for gex_Token_Info queries contains *at least* the following
// fields, in some *unspecified* order
typedef struct {
    // "Job rank" of the sending process, as defined with the description
    //  of gex_System_QueryJobRank().
    gex_Rank_t                 gex_srcrank;

    // Entry describing the currently-running handler corresponding to this token.
    // The referenced gex_AM_Entry_t object resides in library-owned storage,
    // and should not be directly modified by client code.
    // If handler was registered using the legacy gasnet_attach() call, this
    // value may be set to a valid pointer to a gex_AM_Entry_t, with undefined
    // contents.
    const gex_AM_Entry_t      *gex_entry;

    // 1 if the current handler is a Request, 0 otherwise.
    [some integral type]       gex_is_req;

    // 1 if the current handler is a Long, 0 otherwise.
    [some integral type]       gex_is_long;
} gex_Token_Info_t;

// Bitmask constants to request specific info from gex_Token_Info():
// All listed constants are required, but the corresponding queries
// are divided into Required ones and Optional ones (with the
// exception of GEX_TI_ALL).
typedef [some integer type] gex_TI_t;

// REQUIRED: All implementations must support these queries:
#define GEX_TI_SRCRANK       ((gex_TI_t)???)

// OPTIONAL: Some implementations might not support these queries:
#define GEX_TI_ENTRY         ((gex_TI_t)???)
#define GEX_TI_IS_REQ        ((gex_TI_t)???)
#define GEX_TI_IS_LONG       ((gex_TI_t)???)

// Convenience: all defined queries (Required and Optional)
#define GEX_TI_ALL           ((gex_TI_t)???)

// Takes a token, address of client-allocated gex_Token_Info_t, and a mask.
// The mask is a bit-wise OR of GEX_TI_* constants, which indicates which
// fields of the gex_Token_Info_t should be set by the call.
//
// The return value is of the same form as the mask.
// The implementation is permitted to set fields not requested by the
// caller to valid or *invalid* values.  The returned mask will indicate
// which fields contain valid results, and may include bits not present
// in the mask.
//
// Each GEX_TI_* corresponds to either a Required or Optional query.
// When a client requests a Required query, a conforming implementation
// MUST set these fields and the corresponding bit in the return value.
// An Optional query may not be implemented on all conduits or all
// configurations, or even under various conditions (e.g. may not be
// supported in a Reply handler).  If the client makes an Optional request
// the presence of the corresponding bit in the return value is the only
// indication that the struct field is valid.
extern gex_TI_t gex_Token_Info(
                gex_Token_t         token,
                gex_Token_Info_t    *info,
                gex_TI_t            mask);


//
// Fixed-payload AM APIs
//

// NOTE 0: Prototypes in this section are "patterns"
//
//   These API instantiate the "[M]" at the end of each prototype with
//   the integers 0 through gex_AM_MaxArgs(), inclusive.
//   The '[,arg0, ... ,argM-1]' then represent the arguments
//   (each of type gex_AM_Arg_t).
// 
// NOTE 1: Return value
// 
//   An AM Request or Reply call is a "no op" IF AND ONLY IF the value
//   GEX_FLAG_IMMEDIATE is included in the 'flags' argument AND the
//   conduit could determine that it would need to block temporarily to
//   obtain the necessary resources.  This case is distinguished by a
//   non-zero return.  In all other cases the return value is zero.  
//
//   In the "no op" case no communication has been performed and the
//   contents of the location named by the 'lc_opt' argument (if any) is
//   undefined.
//
// NOTE 2: The 'lc_opt' argument for local completion
//
//   The AM interfaces never detect or report remote completion, but do
//   have selectable behavior with respect to local completion (which
//   means that the source buffer may safely by written, free()ed, etc).
//
//   Short AMs have no payload and therefore have no 'lc_opt' argument.
//
//   The Medium and Long Requests accept the pre-defined constant values
//   GEX_EVENT_NOW and GEX_EVENT_GROUP, and pointers to variables of type
//   'gex_Event_t' (note that GEX_EVENT_DEFER is prohibited).  
//   The NOW constant requires that the Request call not
//   return until after local completion.  The GROUP constant allows the
//   Request call to return without delaying for local completion and adds
//   the AM operation to the set of operations for which
//   gex_NBI_{Test,Wait}() call may check local completion when passed
//   GEX_EC_AM.  Use of a pointer to a variable of type 'gex_Event_t'
//   allows the call to return without delay, and requires the client to later
//   check local completion using gex_Event_{Test,Wait}*().
//
//   The 'lc_opt' argument to Medium and Long Reply calls behave as for the
//   Requests with the exception that GEX_EVENT_GROUP is *not* permitted.
//   It is also important to note that it is not legal to "test", or
//   "wait" on a 'gex_Event_t' in AM handler context.
//   [TBD: we *could* allow handlers to make bounded calls to "test", which
//   does not Poll, if we wanted to.]
//
// NOTE 3: The 'flags' argument for segment disposition [UNIMPLEMENTED]
// 
//   The 'flags' argument to Medium and Long Request/Reply calls may include
//   GEX_FLAG_SELF_SEG_* flags to assert segment disposition properties of the
//   address range described by [source_addr..(source_addr+nbytes-1)]. Any such
//   assertions must remain true until local completion is signalled (see above).
//
//   The 'flags' argument to Long Request/Reply calls may include
//   GEX_FLAG_PEER_SEG_* flags to assert segment disposition properties of the
//   address range described by [dest_addr..dest_addr+nbytes-1)]. Any such
//   assertions must remain true until the AM handler begins execution at the target.
//
// Other arguments behave as in the analogous GASNet-1 functions.
// Misc semantic strengthening:
// * dest_addr for Long is guaranteed to be delivered to the handler as provided
//   by the initiator, even for the degenerate case when nbytes==0

// Long
int gex_AM_RequestLong[M](
           gex_TM_t tm,                   // Names a local context ("return address")
           gex_Rank_t rank,               // Together with 'tm', names a remote context
           gex_AM_Index_t handler,        // Index into handler table of remote context
           const void *source_addr,       // Payload address (or OFFSET)
           size_t nbytes,                 // Payload length
           void *dest_addr,               // Payload destination address (or OFFSET)
           gex_Event_t *lc_opt,           // Local completion control (see above)
           gex_Flags_t flags              // Flags to control this operation
           [,arg0, ... ,argM-1])          // Handler argument list, each of type gex_AM_Arg_t
int gex_AM_ReplyLong[M](
           gex_Token_t token,             // Names local and remote contexts
           gex_AM_Index_t handler,
           const void *source_addr,
           size_t nbytes,
           void *dest_addr,
           gex_Event_t *lc_opt,
           gex_Flags_t flags
           [,arg0, ... ,argM-1]);
// Medium
int gex_AM_RequestMedium[M](
           gex_TM_t tm,
           gex_Rank_t rank,
           gex_AM_Index_t handler,
           const void *source_addr,
           size_t nbytes,
           gex_Event_t *lc_opt,
           gex_Flags_t flags
           [,arg0, ... ,argM-1]);
int gex_AM_ReplyMedium[M](
           gex_Token_t token,
           gex_AM_Index_t handler,
           const void *source_addr,
           size_t nbytes,
           gex_Event_t *lc_opt,
           gex_Flags_t flags
           [,arg0, ... ,argM-1]);
// Short
int gex_AM_RequestShort[M](
           gex_TM_t tm,
           gex_Rank_t rank,
           gex_AM_Index_t handler, 
           gex_Flags_t flags
           [,arg0, ... ,argM-1]);
int gex_AM_ReplyShort[M](
           gex_Token_t token,
           gex_AM_Index_t handler,
           gex_Flags_t flags
           [,arg0, ... ,argM-1]);

//
// Negotiated-payload AM APIs
//

// The fixed-payload APIs for Active Message Mediums and Longs (brought
// forward from GASNet-1) allow sending any payload up to defined maximum
// lengths.  However, this comes with the potential costs of extra in-memory
// copies of the payload and/or conservative maximum lengths.  Use of the
// negotiated-payload APIs can overcome these limitations to yield performance
// improvements in two important cases.  First, when the client can begin the
// negotiation before the payload is assembled (for instance concatenation of
// a client-provided header and application-provided data) payload negotiation
// can ensure that the GASNet conduit will not need to make an additional
// in-memory copy to prepend its own header, or to send from pre-registered
// memory.  Second, when the client has a need for fragmentation and
// reassembly (due to a payload exceeding the maximums) use of negotiated
// payload may permit a smaller number of fragments by taking advantage of
// transient conditions (for instance in GASNet's buffer management) that
// allow sending AMs with a larger payload than can be guaranteed in general.
//
// The basis of negotiated-payload AMs is a split-phase interface: "Prepare"
// and "Commit".  The first phase is a Prepare function to which the client
// passes an optional source buffer address, the minimum and maximum lengths
// it is willing to send, and many (but not all) of the other parameters
// normally passed when injecting an Active Message.  In this phase, GASNet
// determines how much of the payload can be sent.
//
// The return from the Prepare call provides the client with an address and a
// length.  The length is in the range defined by the minimum and maximum
// lengths.  The address will be either the client_buf (if non_NULL) or
// it may be a GASNet-owned buffer of the indicated length, suitably aligned
// to hold any data type.
//
// It is important to note that passing NULL for the client_buf argument to
// a Prepare call requires GASNet to allocate buffer space of size no
// smaller than min_length.  Care should be taken to keep such allocation
// demands reasonable.
//
// Between the Prepare and the Commit calls the client is responsible for
// assembling its payload (or the prefix of the given length) at the selected
// address (potentially a no-op).  The client may send a length shorter than
// the value returned from the Prepare, for instance rounding down to some
// natural boundary.  The client may also defer until the Prepare-Commit
// interval its selection of the AM handler and arguments, which might depend
// on the address and length returned by the Prepare call (though the number
// of args must be fixed at Prepare).  In the case of a Long, the client may
// also defer selecting the destination address.  These various parameters are
// passed to the Commit function which performs the actual AM injection.
//
// It is important to note that in the interval between a Prepare and Commit,
// the client is bound by the same restrictions as in an Active Message Reply
// handler (ie all communication calls are prohibited).  Prepare/commit pairs
// do not nest.  Additionally, the Prepare returns a thread-specific object
// that must be consumed (exactly once) by a Commit in the same thread. Calls
// to Prepare are permitted in the same places as the corresponding
// fixed-payload AM injection call.
//
// Currently the semantics of the min_length==0 case are unspecified.
// We advise avoiding that case until a later release has resolved this.

// Opaque type for AM Source Descriptor
// Used in negotiated-payload AM calls:
//   Produced by (returned from) gex_AM_Prepare*()
//   Consumed by (passed to) gex_AM_Commit*()
typedef ... gex_AM_SrcDesc_t;

// Predefined value of type gex_AM_SrcDesc_t
// Guaranteed to be zero.
// May be returned by gex_AM_Prepare*() when the GEX_FLAG_IMMEDIATE flag 
// was passed, but required resources are not available.
// Must not be passed to gex_AM_Commit*() calls or the
// gex_AM_SrcDesc*() queries.
#define GEX_AM_SRCDESC_NO_OP ((gex_AM_SrcDesc_t)(uintptr_t)0)

// Query the address component of a gex_AM_SrcDesc_t
//
// Will either be identical to the 'client_buf' passed
// to the Prepare call, or will be GASNet-owned memory
// suitably aligned to hold any data type.
void *gex_AM_SrcDescAddr(gex_AM_SrcDesc_t sd);

// Query the length component of a gex_AM_SrcDesc_t
//
// Indicates the maximum length of the buffer located at gex_AM_SrcDescAddr()
// that can be sent in the Commit call.
// Will be between the 'min_length' and 'max_length' passed
// to the Prepare call (inclusive).
size_t gex_AM_SrcDescSize(gex_AM_SrcDesc_t sd);

//
// gex_AM_Prepare calls
//
// RETURNS: gex_AM_SrcDesc_t
//   + An opaque scalar type (with accessors) described above
//   + This is thread-specific value
//   + This object is "consumed" by (cannot be used after) the
//     Commit call
// ARGUMENTS:
//  gex_TM_t tm, gex_Rank_t rank [REQUEST ONLY]
//   + These arguments name the destination of an AMRequest
//  gex_Token_t token [REPLY ONLY]
//   + This argument identifies (implicitly) the destination of
//     an AMReply
//  const void *client_buf
//   + If non-NULL the client is offering this buffer as a
//     source_addr
//   + If NULL, the client is requesting a GASNet-owned source
//     buffer to populate
//  size_t min_length
//   + This is the minimum length that the Prepare call may
//     return on success - ie the minimum-sized payload the
//     client is willing to send at this time.
//   + The value must not exceed the value of the
//     gex_AM_Max[...]() call with the analogous Prepare arguments
//  size_t max_length
//   + This is the maximum length that the Prepare call may
//     return on success - ie a (not necessarily tight) upper
//     bound on the payload size the client is willing to send at
//     this time.
//   + The value must not be less than min_length (but they may
//     be equal).
//   + The value *may* exceed the corresponding gex_AM_Max[...]().
//  void *dest_addr [LONG ONLY]
//   + If this value is non-NULL then GASNet may use this value
//     (and flags in the GEX_FLAG_PEER_SEG_* family) to guide its
//     choice of outputs (addr and size)
//   + If this value is non-NULL then the client is required to
//     pass the same value to the Commit call.
//   + May be NULL to request conservative behavior
//   + In all cases the actual dest_addr is supplied at Commit.
//  gex_Event_t *lc_opt
//   + If client_buf is NULL, this argument must also be NULL.
//   + If client_buf is non-NULL, this argument operates in the same
//     manner as the 'lc_opt' argument to the fixed-payload AM calls.
//     Between Prepare and Commit, the contents of the gex_Event_t
//     referenced by lc_opt, if any, is indeterminate.  Only after
//     return from the Commit call may such a value be used by the
//     caller.
//  gex_Flags_t flags
//   + Bitwise OR of flags valid for the corresponding
//     fixed-payload AM injection
//   + GEX_FLAG_IMMEDIATE: the Prepare call may return
//     GEX_AM_SRCDESC_NO_OP==0 if injection resources (in
//     particular a buffer of size min_length or longer) cannot
//     be obtained.
//     The Commit-time behavior is unaffected by this flag.
//   + [UNIMPLEMENTED] GEX_FLAG_SELF_SEG_OFFSET: is prohibited
//   + [UNIMPLEMENTED] GEX_FLAG_SELF_SEG_*: these flags may only be 
//     passed if client_buf is non-NULL, and assert segment disposition
//     properties for the range [client_buf..(client_buf+max_length-1)]
//     that must be true upon entry to Prepare. If gex_AM_SrcDescAddr()
//     on the Prepare result is equal to client_buf, then the assertion 
//     must remain true until after local completion is signalled via `lc_opt`.
//   + [UNIMPLEMENTED] GEX_FLAG_PEER_SEG_*: [LONG ONLY] if `dest_addr` is
//     non-NULL, these flags assert segment disposition properties for the
//     range [dest_addr..(dest_addr+max_length-1)] that must be true upon
//     entry to Prepare and remain true until entry to the AM handler at
//     the target. If `dest_addr` NULL at Prepare and non-NULL at Commit,
//     these flags assert segment disposition properties for the Commit-time
//     range [dest_addr..(dest_addr+nbytes-1)] that must be true upon
//     entry to Commit and remain true until entry to the AM handler at
//     the target. 
//  unsigned int numargs
//   + The number of arguments to be passed to the Commit call
//
extern gex_AM_SrcDesc_t gex_AM_PrepareRequestMedium(
                gex_TM_t       tm,
                gex_Rank_t     rank,
                const void     *client_buf,
                size_t         min_length,
                size_t         max_length,
                gex_Event_t    *lc_opt,
                gex_Flags_t    flags,
                unsigned int   numargs);
extern gex_AM_SrcDesc_t gex_AM_PrepareReplyMedium(
                gex_Token_t    token,
                const void     *client_buf,
                size_t         min_length,
                size_t         max_length,
                gex_Event_t    *lc_opt,
                gex_Flags_t    flags,
                unsigned int   numargs);
extern gex_AM_SrcDesc_t gex_AM_PrepareRequestLong(
                gex_TM_t       tm,
                gex_Rank_t     rank,
                const void     *client_buf,
                size_t         min_length,
                size_t         max_length,
                void           *dest_addr,
                gex_Event_t    *lc_opt,
                gex_Flags_t    flags,
                unsigned int   numargs);
extern gex_AM_SrcDesc_t gex_AM_PrepareReplyLong(
                gex_Token_t    token,
                const void     *client_buf,
                size_t         min_length,
                size_t         max_length,
                void           *dest_addr,
                gex_Event_t    *lc_opt,
                gex_Flags_t    flags,
                unsigned int   numargs);

//
// gex_AM_Commit calls
//
// NOTE: Prototypes in this section are "patterns"
//   These API instantiate the "[M]" at the end of each prototype with
//   the integers 0 through gex_AM_MaxArgs(), inclusive.
//   The '[,arg0, ... ,argM-1]' then represent the arguments
//   (each of type gex_AM_Arg_t).
//
// RETURNS: void
// ARGUMENTS:
//  gex_AM_SrcDesc sd
//   + The value returned by the immediately preceding Prepare
//     call on this thread.
//  gex_AM_Index_t handler
//   + The index of the AM handler to run at the destination
//  size_t nbytes
//   + The client's payload length
//   + Must be in the range: [0 .. gex_AM_SrcDescSize(sd)]
//   + The base address of the source payload buffer is implicitly
//     specified by gex_AM_SrcDescAddr(sd)
//  void *dest_addr [LONG ONLY]
//   + The destination address for transfer of Long payloads
//   + If non-NULL dest_addr was passed to Prepare, this must
//     be the same value
//
extern void gex_AM_CommitRequestMedium[M](
                gex_AM_SrcDesc_t sd,
                gex_AM_Index_t   handler,
                size_t           nbytes
                [,arg0, ... ,argM-1]);
extern void gex_AM_CommitReplyMedium[M](
                gex_AM_SrcDesc_t sd,
                gex_AM_Index_t   handler,
                size_t           nbytes
                [,arg0, ... ,argM-1]);
extern void gex_AM_CommitRequestLong[M](
                gex_AM_SrcDesc_t sd,
                gex_AM_Index_t   handler,
                size_t           nbytes,
                void             *dest_addr
                [,arg0, ... ,argM-1]);
extern void gex_AM_CommitReplyLong[M](
                gex_AM_SrcDesc_t sd,
                gex_AM_Index_t   handler,
                size_t           nbytes,
                void             *dest_addr
                [,arg0, ... ,argM-1]);


//
// Extended API
//

// NOTE 1: Return value
//
//   An Extended API initiation call is a "no op" IF AND ONLY IF the value
//   GEX_FLAG_IMMEDIATE is included in the 'flags' argument AND the
//   conduit could determine that it would need to block temporarily to
//   obtain the necessary resources.  The blocking and NBI calls return a
//   non-zero value *only* in the "no op" case, while the NB calls return
//   GEX_EVENT_NO_OP.
//
//   In the "no op" case no communication has been performed and the
//   contents of the location named by the 'lc_opt' argument (if any) is
//   undefined.
//
// NOTE 2a: The 'lc_opt' argument for local completion (NBI case)
//
//   Implicit-event non-blocking Puts have an 'lc_opt' argument which
//   controls the behavior with respect to local completion.  The value can
//   be the pre-defined constants GEX_EVENT_NOW, GEX_EVENT_DEFER, or
//   GEX_EVENT_GROUP.  The NOW constant requires that the call not
//   return until the operation is locally complete.  The DEFER constant
//   permits the call to return without delaying for local completion,
//   which may occur as late as in the call which syncs (retires) the
//   operation (could be an explicit-event call if using an NBI access
//   region).  The GROUP constant allows the call to return without
//   delaying for local completion and adds the operation to the set for
//   which gex_NBI_{Test,Wait}() call may check local completion when
//   passed GEX_EC_LC.
//
// NOTE 2b: The 'lc_opt' argument for local completion (NB case)
//
//   Explicit-event non-blocking Puts have an 'lc_opt' argument which
//   controls the behavior with respect to local completion.  The value can
//   be the pre-defined constants GEX_EVENT_NOW or GEX_EVENT_DEFER, or
//   a pointer to a variable of type 'gex_Event_t'.  The NOW
//   constant requires that the call not return until the operation is
//   locally complete.  The DEFER constant permits the call to return
//   without delaying for local completion, which may occur as late as in
//   the call which syncs (retires) the returned event.  Use of a pointer
//   to a variable of type 'gex_Event_t' allows the call to return without
//   delay, and allows the client to check local completion using
//   gex_Event_{Test,Wait}*().

// Put
int gex_RMA_PutBlocking(
           gex_TM_t tm,                   // Names a local context ("return address")
           gex_Rank_t rank,               // Together with 'tm', names a remote context
           void *dest,                    // Remote (destination) address (or OFFSET)
           const void *src,               // Local (source) address (or OFFSET)
           size_t nbytes,                 // Length of xfer
           gex_Flags_t flags);            // Flags to control this operation
int gex_RMA_PutNBI(
           gex_TM_t tm,
           gex_Rank_t rank,
           void *dest,
           const void *src,
           size_t nbytes,
           gex_Event_t *lc_opt,           // Local completion control (see above)
           gex_Flags_t flags);
gex_Event_t gex_RMA_PutNB(
           gex_TM_t tm,
           gex_Rank_t rank,
           void *dest,
           const void *src,
           size_t nbytes,
           gex_Event_t *lc_opt,
           gex_Flags_t flags);

// Get
int gex_RMA_GetBlocking( // Returns non-zero *only* in "no op" case (IMMEDIATE flag)
           gex_TM_t tm,                   // Names a local context ("return address")
           void *dest,                    // Local (destination) address (or OFFSET)
           gex_Rank_t rank,               // Together with 'tm', names a remote context
           void *src,                     // Remote (source) address (or OFFSET)
           size_t nbytes,                 // Length of xfer
           gex_Flags_t flags);            // Flags to control this operation
int gex_RMA_GetNBI( // Returns non-zero *only* in "no op" case (IMMEDIATE flag)
           gex_TM_t tm,
           void *dest,
           gex_Rank_t rank,
           void *src,
           size_t nbytes,
           gex_Flags_t flags);
gex_Event_t gex_RMA_GetNB(
           gex_TM_t tm,
           void *dest,
           gex_Rank_t rank,
           void *src,
           size_t nbytes,
           gex_Flags_t flags);

// Value-based payloads
gex_RMA_Value_t gex_RMA_GetBlockingVal(
           gex_TM_t tm,
           gex_Rank_t rank,
           void *src,
           size_t nbytes,
           gex_Flags_t flags);
int gex_RMA_PutBlockingVal(
           gex_TM_t tm,
           gex_Rank_t rank,
           void *dest,
           gex_RMA_Value_t value,
           size_t nbytes,
           gex_Flags_t flags);
int gex_RMA_PutNBIVal(
           gex_TM_t tm,
           gex_Rank_t rank,
           void *dest,
           gex_RMA_Value_t value,
           size_t nbytes,
           gex_Flags_t flags);
gex_Event_t gex_RMA_PutNBVal(
           gex_TM_t tm,
           gex_Rank_t rank,
           void *dest,
           gex_RMA_Value_t value,
           size_t nbytes,
           gex_Flags_t flags);

// NBI Access regions:
// These are interoperable with, and have the same semantics as,
// gasnet_{begin,end}_nbi_accessregion()
// flags are reserved for future use and must currently be zero.

void gex_NBI_BeginAccessRegion(gex_Flags_t flags);
gex_Event_t gex_NBI_EndAccessRegion(gex_Flags_t flags);


// Event test/wait operations
// The operation is indicated by the suffix
//  + _Test: no Poll call is made, returns zero on success, and non-zero otherwise.
//  + _Wait: Polls until success, void return

// Completion of a single NB event
// Success is defined as when the passed event is complete.
int  gex_Event_Test (gex_Event_t event);
void gex_Event_Wait (gex_Event_t event);

// Completion of an event array - "some"
// Success is defined as one or more events have been completed, OR
// the input array contains only GEX_EVENT_INVALID (which are otherwise ignored).
// Completed events, if any, are overwritten with GEX_EVENT_INVALID.
// These are the same semantics as gasnet_{try,wait}_syncnb_some(),
// except that "Test" does not AMPoll as "try" does.
// flags are reserved for future use and must currently be zero.
int  gex_Event_TestSome (gex_Event_t *pevent, size_t numevents, gex_Flags_t flags);
void gex_Event_WaitSome (gex_Event_t *pevent, size_t numevents, gex_Flags_t flags);

// Completion of an NB event array - "all"
// Success is defined as all passed events have been completed, OR
// the input array contains only GEX_EVENT_INVALID (which are otherwise ignored).
// Completed events, if any, are overwritten with GEX_EVENT_INVALID.
// These are the same semantics as gasnet_{try,wait}_syncnb_all(),
// except that "Test" does not AMPoll as "try" does.
// flags are reserved for future use and must currently be zero.
int  gex_Event_TestAll (gex_Event_t *pevent, size_t numevents, gex_Flags_t flags);
void gex_Event_WaitAll (gex_Event_t *pevent, size_t numevents, gex_Flags_t flags);

// Identifiers to name Event Categories (such as local completion from NBI Puts)
// TODO: will eventually include categories for collectives, VIS metadata, ...
typedef [some integer type] gex_EC_t;
#define GEX_EC_ALL   ((gex_EC_t)???)
#define GEX_EC_GET   ((gex_EC_t)???)
#define GEX_EC_PUT   ((gex_EC_t)???)
#define GEX_EC_AM    ((gex_EC_t)???)
#define GEX_EC_LC    ((gex_EC_t)???)
#define GEX_EC_RMW   ((gex_EC_t)???)

// Sync of specified subset of NBI operations
// The 'event_mask' argument is bitwise-OR of GEX_EC_* constants
// flags are reserved for future use and must currently be zero.
int  gex_NBI_Test(gex_EC_t event_mask, gex_Flags_t flags);
void gex_NBI_Wait(gex_EC_t event_mask, gex_Flags_t flags);

// Extract a leaf event from the root event
// NOTE: name is subject to change
//
// The 'root' argument must be a valid root event
// The 'event_category' argument is an GEX_EC_<x> constant.
// It cannot be a bitwise-OR of multiple such values, nor GEX_EC_ALL.
//
// There are additional validity constraints to be documented, such as one
// cannot ask for an event that was "suppressed" by passing EVENT_DEFER.
// Violating those constraints give undefined results (though we want a debug
// build to report the violation).
//
// For an event that has "already happened" the implementation may return
// either GEX_EVENT_INVALID or a valid event that tests as done.  The
// implementation is not constrained to pick consistently between these two
// options (and in the extreme could choose between them at random).
//
// This is a *query* and does not instantiate a new object, and so multiple
// calls with the same argument (that don't return INVALID_HANDLE) must return
// the *same* event.
gex_Event_t gex_Event_QueryLeaf(
        gex_Event_t event,
        gex_EC_t event_category);


//
// Neighborhood: [EXPERIMENTAL]
// A "neighborhood" is defined as a set of GEX processes that can share
// memory via the GASNet PSHM feature.
//

// Const-qualified struct type for describing a member of a neighborhood
typedef const struct {
    gex_Rank_t gex_jobrank; // the Job Rank (as defined above)
    // Reserved for future expansion and/or internal-use fields
} gex_NeighborhoodInfo_t;

// Query information about the neighborhood of the calling process.
//
// All arguments are pointers to locations for outputs, each of which
// may be NULL if the caller does not need a particular value.
//
// info_p:
//        Receives the address of an array with elements of type
//        gex_NeighborhoodInfo_t (defined above), which includes one entry
//        for each process in the neighborhood of the calling process.
//        Entries are sorted by increasing gex_jobrank.
//        The storage of this array is owned by GASNet and must not be
//        written to or free()ed.
//        High-quality implementations will store this array in shared memory
//        to reduce memory footprint.  Therefore, clients should consider using
//        it in-place to avoid creating a less-scalable copy per process.
// info_count_p:
//        Receives the number of processes in the neighborhood of the calling
//        process.  This includes the caller, and is therefore always non-zero.
// my_info_index_p:
//        Receives the 0-based index of the calling process relative to its
//        neighborhood.  In particular, the following formula holds:
//        (*info_p)[*my_info_index_p].gex_jobrank == gex_System_QueryJobRank()
//
// Semantics in a resilient build will be defined in a later release.
extern void gex_System_QueryNeighborhoodInfo(
            gex_NeighborhoodInfo_t **info_p,
            gex_Rank_t             *info_count_p,
            gex_Rank_t             *my_info_index_p);


//
// Handler-safe locks (HSLs)
// Lock semantics are identical to those in GASNet-1
//

// Type for an HSL
// This type interoperable with gasnet_hsl_t
typedef {...} gex_HSL_t;

// Static-initializer for an HSL
// Synonymous with GASNET_HSL_INITIALIZER
#define GEX_HSL_INITIALIZER {...}

// The following operations on HSLs are are semantically identical
// to the corresponding gasnet_hsl_* functions:
void gex_HSL_Init   (gex_HSL_t *hsl);
void gex_HSL_Destroy(gex_HSL_t *hsl);
void gex_HSL_Lock   (gex_HSL_t *hsl);
void gex_HSL_Unlock (gex_HSL_t *hsl);
int  gex_HSL_Trylock(gex_HSL_t *hsl);

//
// Data types for atomics and reductions [EXPERIMENTAL]
//
// GASNet-EX defines (as preprocess-time constants) at least the following
// data types codes for use with remote atomic and reduction operations.
//
//     GEX Constant  C Data Type
//     ------------  -----------
// Integer types:
//     GEX_DT_I32    int32_t
//     GEX_DT_U32    uint32_t
//     GEX_DT_I64    int64_t
//     GEX_DT_U64    uint64_t
// Floating-point types:
//     GEX_DT_FLT    float
//     GEX_DT_DBL    double
//
// It is guaranteed that all GEX_DT_* values can be combined via bit-wise OR
// without loss of information.
//
// Currently, Remote Atomics support all six data types listed above.
// Currently, Reductions are unimplemented.
//
// Note that GASNet-EX supports signed and unsigned exact-width integer types.
// Any mapping to types such as 'int', 'long' and 'long long' is the
// responsibility of the client.

typedef [some integer type] gex_DT_t;
#define GEX_DT_??? ((gex_DT_t)???) // For each GEX_DT_* above

//
// Operation codes (opcodes) for atomics and reductions [EXPERIMENTAL]
//
// GASNet-EX defines (as preprocess-time constants) at least the following
// operation codes for use with atomic and reduction operations.  Not all
// operations are valid in all contexts, as indicated below.
// See documentation for the atomic and reduction operations for more details.
//
// The following apply to the operation definitions which follow:
//   For atomics:
//     'op0' denotes the value at the target location prior to the operation
//     'op1' and 'op2' denote the value of the corresponding function arguments
//     'expr' denotes the value of the target location after the operation
//     Fetching operations always return 'op0'
//   For reductions:
//     'op0' represents the "left" (first) reduction operand
//     'op1' represents the "right" (second) reduction operand
//     'expr' denotes the value of the result of the pairwise reduction
//
// Except where otherwise noted, the expressions below are evaluated according
// to C language rules.
//
// + Non-fetching Operations
//    - Binary Arithmetic Operations
//      Valid for Atomics and Reductions
//      Valid for all specified GEX_DT_* types
//        GEX_OP_ADD   expr = (op0 + op1)
//        GEX_OP_SUB   expr = (op0 - op1)
//        GEX_OP_MULT  expr = (op0 * op1) [UNIMPLEMENTED]
//        GEX_OP_MIN   expr = ((op0 < op1) ? op0 : op1)
//        GEX_OP_MAX   expr = ((op0 > op1) ? op0 : op1)
//    - Unary Arithmetic Operations
//      Valid only for Atomics
//      Valid for all specified GEX_DT_* types
//        GEX_OP_INC   expr = (op0 + 1)
//        GEX_OP_DEC   expr = (op0 - 1)
//    - Bit-wise Operations
//      Valid for Atomics and Reductions
//      Valid only for Integer types
//        GEX_OP_AND   expr = (op0 & op1)
//        GEX_OP_OR    expr = (op0 | op1)
//        GEX_OP_XOR   expr = (op0 ^ op1)
// + Fetching Operations
//   Valid only for Atomics
//   Each GEX_OP_Fxxx performs the same operation as GEX_OP_xxx, above,
//   and is valid for the same types.
//   Additionally these operations fetch 'op0' as the result of the atomic.
//    - Binary Arithmetic Operations
//        GEX_OP_FADD
//        GEX_OP_FSUB
//        GEX_OP_FMULT [UNIMPLEMENTED]
//        GEX_OP_FMIN
//        GEX_OP_FMAX
//    - Unary Arithmetic Operations
//        GEX_OP_FINC
//        GEX_OP_FDEC
//    - Bit-wise Operations
//        GEX_OP_FAND
//        GEX_OP_FOR
//        GEX_OP_FXOR
// + Accessor Operations
//   Valid only for Atomics
//   Valid for all specified GEX_DT_* types
//    - Non-fetching Accessor
//        GEX_OP_SET   expr = op1  (writes 'op1' to the target location)
//    - Fetching Accessors (fetch 'op0' as the result of the atomic)
//        GEX_OP_GET   expr = op0  (does not modify the target location)
//        GEX_OP_SWAP  expr = op1  (swaps 'op1' with the target location)
//        GEX_OP_CSWAP expr = ((op0 == op1) ? op2 : op0)
//                     With a guarantee to be free of spurious failures as from
//                     cache events.
//
// It is guaranteed that all GEX_OP_* values can be combined via bit-wise OR without
// loss of information.

typedef [some integer type] gex_OP_t;
#define GEX_OP_??? ((gex_OP_t)???) // For each GEX_OP_* above


//----------------------------------------------------------------------
//
// Remote Atomic Operations [EXPERIMENTAL]
// APIs in this section are provided by gasnet_ratomic.h
//

//
// Atomic Domains
//
// Just as all point-to-point RMA calls take a gex_TM_t argument, calls to
// initiate Remote Atomic operations take a gex_AD_t, where "AD" is short for
// "Atomic Domain".
//
// + Creation of an AD associates it with a specific gex_TM_t.
//
//   This association defines the memory locations which can be accessed using
//   the AD.  Only memory within the address space of a process hosting an
//   endpoint that is a member of this team may be accessed by atomic
//   operations which pass a given AD.
//
//   Currently, there is an additional constraint that target locations must
//   lie within the bound segments of the team's endpoints.
//
// + Creation of an AD associates with it one data type and a set of operations.
//
//   This permits selection of the best possible implementation which can
//   provide correct results for the given set of operations on the given data
//   type.  This is important because the best possible implementation of a
//   operation "X" may not be compatible with operation "Y".  So, this best
//   "X" can only be used when it is known that "Y" will not be used.  This
//   issue arises because a NIC may offload "X" (but not "Y") and use of a
//   CPU-based implementation of "Y" would not be coherent with the NIC
//   performing a concurrent "X" operation.
//
// + Use of an AD is conceptually tied to specific data and time.
//
//   Correct operation of gex_AD_Op*() APIs is only assured if the client code
//   can ensure that there are no other accesses to the same target locations
//   concurrent with the operations on a given AD.
//
//   The prohibition against concurrent access applies to all access by CPUs,
//   GPUs and any other hardware that references memory; and to all GASNet-EX
//   operations other than the atomic accesses defined in this section.  The
//   write by a fetching remote atomic operation to an output location on the
//   initiator is NOT an atomic access for the purposes of this prohibition.
//
//   Prohibited accesses by CPUs and GPUs include not only load/store, but
//   also any atomic operations provided by languages such as C11 and C++11,
//   by compiler intrinsics, operating system facilities, etc.
//
//   This prohibition also extends to concurrent access via multiple ADs, even
//   if created with identical arguments.  However, this specification does
//   not prohibit concurrent access to distinct (non overlapping) data using
//   distinct ADs.
//
//   GASNet-EX does not provide any mechanisms to detect violations of the
//   prohibitions described above.
//
// + Atomic Access Phases [INCOMPLETE / OPEN ISSUE]
//
//   It is the intent of this specification to permit access to the same data
//   using remote atomics and other (non-atomic) mechanisms, and to the same
//   data using mutiple atomics domains.  However, such different accesses
//   must be NON-concurrent.  This separation is into what we will call
//   "atomic access phases":
//     During a given atomic access phase, any given byte in the memory of any
//     GASNet process shall NOT be accessed by more than ONE of:
//      (1) gex_AD_Op*() calls that reference that byte as part of the target
//          object.
//      (2) any means except for (1).
//     Furthermore, during a given atomic access phase, all gex_AD_Op*() calls
//     accessing a given target byte shall use the same AD object.
//
//   Note that the byte-granularity of this definition has consequences for
//   the use of union types and of type-punning, either of which may result in
//   a given byte being considered part of multiple C objects.
//
//   The means for a transition between atomic access phases has not yet been
//   fully specified.  We do NOT expect that the resolution to this open issue
//   will invalidate any interface defined in this current specification.
//   However, when implementations of remote atomics are introduced with
//   properties such as caching, it may become necessary for clients using
//   remote atomics to take additional steps to transition between atomic
//   access phases.
//
//   FOR *THIS* RELEASE we believe it is sufficient to separate atomic access
//   phases by a barrier synchronization.  However, it is necessary to ensure
//   that any GASNet-EX accesses which may conflict have been completed
//   (synced) prior to the barrier.  This includes completing all remote atomic
//   operations before a transition to non-atomic access or accesses by a
//   different atomic domain; and completing all other GASNet data-movement
//   operations (RMA, Collective, etc.) before a transition to atomic access.
//
// + Memory Ordering/Fencing/Consistency [INCOMPLETE / OPEN ISSUE]
//
//   It is the intent of this specification to include flags to demand memory
//   ordering fences (such as for Acquire and Release) when initiating an atomic
//   operation.  However, these semantics have not yet been defined.  We
//   expect that the resolution to this open issue will involve the definition
//   of additional GEX_FLAG_* values, and will not invalidate any interface
//   defined in this current specification.
//
//   FOR *THIS* RELEASE we advise use of the GASNet-Tools APIs to introduce
//   memory ordering fences where they may be required for correctness.
//   See "Memory barriers" in README-tools.

// Opaque type for Atomic Domain
typedef ... gex_AD_t;

// Create an Atomic Domain
//
// This call, collective over the 'tm' argument, creates an atomic domain for
// the operations in the 'ops' argument performed on data type 'dt'.
//
// The 'ad_p' is an OUT parameter that receives a reference to the
// newly created atomic domain.
//
// The 'dt' and 'ops' arguments define the type and operations.
//  + 'dt' is a value of type gex_DT_t
//  + 'ops' is a bitwise-OR of one or more GEX_OP_* constants of type gex_OP_t.
// If 'dt' and 'ops' do not define only valid combinations (as described in the
// definitions of gex_OP_t), then the behavior is undefined.
//
// The 'flags' argument provides additional control over the created domain.
//  + GEX_FLAG_AD_FAVOR_*: [UNIMPLEMENTED]
//    Family of flags (still TBD) to influence the selection of implementation,
//    for instance to favor performance of access by the process to which the data
//    has affinity vs access via the network (among other possibilities).
//
// The 'dt', 'ops' and 'flags' arguments must each be equal across all callers
// (single-valued) or the behavior is undefined.
//
void gex_AD_Create(
            gex_AD_t                   *ad_p,            // Output
            gex_TM_t                   tm,               // The team
            gex_DT_t                   dt,               // The data type
            gex_OP_t                   ops,              // OR of operations
            gex_Flags_t                flags);           // flags

// Destroy an Atomic Domain
//
// This call destroys an atomic domain.
//
// Calls must be collective over the team used to create the atomic domain.
//
// All operations initiated on the atomic domain must be complete prior to any
// rank making this call (or the behavior is undefined).  In practice, this
// means completing (syncing) all atomic operation at their initiators,
// followed by a barrier prior to calling this function.
//
// [INCOMPLETE / OPEN ISSUE]
// Once this specification includes a complete specification of atomic access
// phases, this call will provide and/all aspects of division between such
// phases which are stronger than the quiescence pre-condition.  We do NOT
// expect that the resolution to this open issue will invalidate this API's
// specification.
//
// Though this function is collective, it does not guarantee barrier
// synchronization.
//
void gex_AD_Destroy(gex_AD_t ad);

//
// Query operations on gex_AD_t
//

// Query the parameters passed when atomic domain was created

gex_Flags_t  gex_AD_QueryFlags(gex_AD_t ad);
gex_TM_t     gex_AD_QueryTM(gex_AD_t ad);
gex_DT_t     gex_AD_QueryDT(gex_AD_t ad);
gex_OP_t     gex_AD_QueryOps(gex_AD_t ad);

// Client-Data (CData) support for gex_AD_t
// These calls provide the means for the client to set and retrieve one void*
// field of client-specific data for each AD, which is NULL for a newly
// created AD.

void  gex_AD_SetCData(gex_AD_t ad, const void *val);
void* gex_AD_QueryCData(gex_AD_t ad);


//
// Remote Atomic Operations
//
// Remote atomic operations are point-to-point communication calls that
// perform read-modify-write and accessor operations on typed data (the
// "target location") in the address space of a process hosting an endpoint
// that is a member of the team passed to gex_AD_Create().
//
// These operations are guaranteed to be atomic with respect to all other
// accesses to the same target location made using the same AD, from any rank.
// When using a thread-safe endpoint this includes atomicity of concurrent
// access by multiple threads within a rank.  No other atomicity guarantees
// are provided.  [Currently all endpoints are "thread-safe" when using a
// GASNET_PAR build, and no endpoints are thread-safe otherwise.]
//
// Despite "Remote" in the name, it is explicitly permitted to apply these
// operations to the caller's own memory (and a high-quality implementation
// will optimize this case when possible).
//
// Additional semantics are described following the "Argument synopsis".
//
// Return value:
//
// Atomic operations are available with explicit-event (NB) or implicit-event
// (NBI) completion, with different return types:
//
//  + The gex_AD_OpNB_*() APIs return a gex_Event_t.
//
//    If (and only if) the GEX_FLAG_IMMEDIATE flag is passed to remote atomic
//    initiation, these calls are *permitted* to return GEX_EVENT_NO_OP to
//    indicate that no operation was initiated.  Otherwise, the return value
//    is an event to be used in calls to gex_NBI_{Test,Wait}() to check for
//    completion.  These calls may return GEX_EVENT_INVALID if the operation
//    was completed synchronously.
//
//  + The gex_AD_OpNBI_*() APIs return an integer.
//
//    If (and only if) the GEX_FLAG_IMMEDIATE flag is passed to remote atomic
//    initiation, these calls are *permitted* to return non-zero to indicate
//    that no operation was initiated.  Otherwise, the return value is zero
//    and a gex_NBI_{Test,Wait}() call must be used to check completion.  For
//    the opcodes GEX_OP_SET and GEX_OP_GET, one should use GEX_EC_PUT and
//    GEX_EC_GET, respectively, to check completion.  All other opcodes
//    correspond to an event category of GEX_EC_RMW.
//
// Data types and prototypes:
//   The APIs for remote atomic initiation are typed.  Therefore, descriptions
//   and prototypes below use "[DATATYPE]" to denote the tokens corresponding
//   to the "???" in each supported GEX_DT_???, and "[TYPE]" to denote the
//   corresponding C type.  There is an instance of each function (NB and NBI)
//   for each supported data type.
//   See the "Data types for atomics and reductions" section for which data
//   types are supported for remote atomics, and their corresponding C types.
//
// "Fetching":
//   Text below uses "fetching" to denote operations that write to an output
//   location ('*result_p') at the initiator (and "non-fetching" for all
//   others).
//   See the "Operation codes (opcodes) for atomics and reductions" section
//   for which opcodes are fetching vs non-fetching.
//
// Endpoints:
//   Let 'tm' denote the corresponding argument passed to gex_AD_Create().
//   The endpoint associated with 'tm' is known as the "initiating endpoint".
//   The endpoint named by (tm, tgt_rank) is known as the "target endpoint".
//
// Argument synopsis:
//   gex_AD_t       ad
//     + The Atomic Domain for this operation.
//   [TYPE] *       result_p
//     + Address (or offset) of the output location for fetching operations.
//       Ignored for non-fetching operations.
//   gex_Rank_t     tgt_rank
//     + Rank of the target location
//   void *         tgt_addr
//     + Address (or offset) of the target location
//   gex_OP_t       opcode
//     + Indicates the operation to perform atomically.
//       Operations are described with the definition of gex_OP_t.
//   [TYPE]         operand1
//     + First operand, if any.
//       Ignored if the given opcode takes no operands.
//   [TYPE]         operand2
//     + Second operand, if any.
//       Ignored if the given opcode takes fewer than two operands.
//   gex_Flags_t    flags
//     + Per-operation flags
//       A bitwise OR of zero or more of the GEX_FLAG_* constants.
//
// Semantics of gex_AD_Op*():
//
// + Successful synchronization of a fetching remote atomic operation means
//   that the local output value (at *result_p) is ready to be examined, and
//   will contain a value that was held at the target location at some time in
//   the interval between the call to the initiation function and the
//   successful completion of the synchronization.  This value will be the one
//   present at the start of the atomic operation and denoted as 'op0' in the
//   definition of the applicable opcode.
//   [THIS PARAGRAPH IS NOT INTENDED TO BE A FORMAL MODEL.
//    HOWEVER, ONE IS FORTHCOMING.]
//
// + Successful synchronization of any remote atomic operation means the
//   operation has been performed atomically (including any constituent Read
//   and Write access to the target location) and any remote atomic issued
//   subsequently by any thread on any rank with the same AD and target
//   location will observe the Write, if any (assuming no intervening updates).
//   [THIS PARAGRAPH IS NOT INTENDED TO BE A FORMAL MODEL.
//    HOWEVER, ONE IS FORTHCOMING.]
//
// + Atomicity guarantees apply only to "target locations".  They do not apply
//   to the output of a fetching operation.  Therefore, clients must check for
//   operation completion before the output value of a fetching operation can
//   safely be read (analogous to the destination of an gex_RMA_Get*()).
//   Additionally, a given 'result_p' location must not be used as the target
//   location of remote atomic operations in the same atomic access phase.
//   (see "Atomic Access Phases").
//
// + If two target objects accessed by gex_AD_Op*() overlap (partially or
//   completely) those accesses are subject to the restrictions documented in
//   "Atomic Access Phases" above.  In particular, such accesses are
//   permitted during the same atomic access phase *only* if the accessed
//   bytes exactly coincide and the calls use the same AD object.
//
// + Currently, the target location must be contained entirely within the
//   bound segment of the target endpoint (though this may eventually be
//   relaxed).
//
// + The data type associated with 'ad' and that of the gex_AD_Op*() call must
//   be equal.
//
// + The 'result_p' argument to fetching operations must be a valid pointer to
//   an object of the given type [TYPE] on the initiator.  (See also the
//   description of the [UNIMPLEMENTED] GEX_FLAG_SELF_SEG_OFFSET flag, below.)
//
// + The 'result_p' argument to non-fetching operations is ignored.
//
// + The 'tgt_rank' argument names the target endpoint as a valid rank
//   relative to the team associated with the AD at its creation.
//
// + The 'tgt_addr' argument names the target location, which must be properly
//   aligned for its data type [TYPE] and (for any operation except
//   GEX_OP_SET) must contain an object with compatible effective type,
//   including a qualified version of [TYPE], and (for integer types only)
//   including signed or unsigned variants.  (See also the description of the
//   [UNIMPLEMENTED] GEX_FLAG_PEER_SEG_OFFSET flag, below.)
//
// + The 'opcode' argument gives the operation to be performed atomically.
//   See the "Operation codes (opcodes) for atomics and reductions" section
//   for definitions of each operation.
//
// + The 'opcode' must be a single GEX_OP* value_, not a bitwise OR of two or
//   more GEX_OP_* values.
//
// + The 'opcode' must be a member of the set of opcodes passed to
//   gex_AD_Create().
//
// + Operations on floating-point data types are not guaranteed to obey all
//   rules in the IEEE 754 standard even when the C float and double types
//   otherwise do conform.  Deviations from IEEE 754 include (at least):
//     - Operations on signalling NaNs have undefined behavior.
//     - CSWAP *may* be performed as if on integers of the same width.
//       This could result in non-conforming behavior with quiet NaNs
//       or negative zero.
//     - MIN, MAX, FMIN and FMAX *may* be performed as if on "sign
//       and magnitude representation integers" of the same width.
//       This could result in non-conforming behavior with quiet NaNs.
//       (see https://en.wikipedia.org/wiki/IEEE_754-1985, and especially
//       the section Comparing_floating-point_numbers)
//   [THIS PARAGRAPH MAY NOT BE A COMPLETE LIST OF NON-IEEE BEHAVIORS]
//
//  + If the given opcode requires one or more operands, the 'operand1'
//    argument provides the first ('op1' in the gex_OP_t documentation).
//    Otherwise, 'operand1' is ignored.
//
//  + If the given opcode requires two operands, the 'operand2' argument
//    provides the second ('op2' in the gex_OP_t documentation).
//    Otherwise, 'operand2' is ignored.
//
//  + The 'flags' argument must either be zero, or a bitwise OR of one or more
//    of the following flags.
//     - GEX_FLAG_IMMEDIATE: the call is permitted (but not required) to
//       return a distinguishing value without initiating any communication if
//       the conduit could determine that it would need to block temporarily
//       to obtain the necessary resources.  The NBI calls return a non-zero
//       value (only) in this "no op" case, while the NB calls will return
//       GEX_EVENT_NO_OP.
//     - [UNIMPLEMENTED] GEX_FLAG_SELF_SEG_OFFSET: 'result_p' is to be
//       interpreted as an offset relative to the bound segment of the
//       initiating endpoint (instead of as a virtual address).
//       Ignored for non-fetching operations.
//     - [UNIMPLEMENTED] GEX_FLAG_PEER_SEG_OFFSET: 'tgt_addr' is to be
//       interpreted as an offset relative to the bound segment of the target
//       endpoint (instead of as a virtual address).
//

gex_Event_t gex_AD_OpNB_[DATATYPE](
            gex_AD_t      ad,         // The atomic domain
            [TYPE] *      result_p,   // Output location, if any, else ignored
            gex_Rank_t    tgt_rank,   // Rank of target endpoint
            void *        tgt_addr,   // Address (or OFFSET) of target location
            gex_OP_t      opcode,     // The operation (GEX_OP_*) to perform
            [TYPE]        operand1,   // First operand, if any, else ignored
            [TYPE]        operand2,   // Second operand, if any, else ignored
            gex_Flags_t   flags);     // Flags to control this operation
int gex_AD_OpNBI_[DATATYPE](
            gex_AD_t      ad,
            [TYPE] *      result_p,
            gex_Rank_t    tgt_rank,
            void *        tgt_addr,
            gex_OP_t      opcode,
            [TYPE]        operand1,
            [TYPE]        operand2,
            gex_Flags_t   flags);

// End of section describing APIs provided by gasnet_ratomic.h
//----------------------------------------------------------------------
//
// Vector/Indexed/Strided (VIS) [EXPERIMENTAL]
//
// APIs in this section are provided by gasnet_vis.h

// This API is an updated and expanded version of the VIS prototype offered
// in GASNet-1, which is documented here: http://gasnet.lbl.gov/upc_memcpy_gasnet-2.0.pdf

// For NB variants, return type for all functions in this section is gex_Event_t.
// For NBI/Blocking variants, the return type is int which is non-zero *only* in the
// "no op" case (IMMEDIATE flag), exactly analogous to the gex_RMA_{Put,Get}*() functions.

// For the CURRENT release, all 'flags' arguments must be zero.
// A future revision offer GEX_FLAG_IMMEDIATE support [UNIMPLEMENTED]

// NOTE: This interface does not yet offer local completion indication - all client-owned
// buffers (ie payload buffers and metadata arrays) passed to the non-blocking initiation 
// functions are implicitly treated as GEX_EVENT_DEFER semantics, and thus must remain 
// valid until the operation is fully completed (as in GASNet-1).
// A future revision will expose intermediate completion events [UNIMPLEMENTED]

// NOTE: All of the (void *) types in this API will eventually be gex_Addr_t [UNIMPLEMENTED]

//
// Vector and Indexed Puts and Gets
//

// These operate analogously to those in the GASNet-1 prototype gasnet_{put,get}[vi]_* API

{gex_Event_t,int} gex_VIS_VectorGet{NB,NBI,Blocking}(
        gex_TM_t tm,                                   // Names a local context
        size_t dstcount, gex_Memvec_t const dstlist[], // Local destination data description
        gex_Rank_t srcrank,                            // Together with 'tm', names a remote context
        size_t srccount, gex_Memvec_t const srclist[], // Remote source data description
        gex_Flags_t flags);                            // Flags to control this operation
{gex_Event_t,int} gex_VIS_VectorPut{NB,NBI,Blocking}(
        gex_TM_t tm, gex_Rank_t dstrank,
        size_t dstcount, gex_Memvec_t const dstlist[],
        size_t srccount, gex_Memvec_t const srclist[],
        gex_Flags_t flags);

{gex_Event_t,int} gex_VIS_IndexedGet{NB,NBI,Blocking}(
        gex_TM_t tm,
        size_t dstcount, void * const dstlist[], size_t dstlen,
        gex_Rank_t srcrank,
        size_t srccount, void * const srclist[], size_t srclen,
        gex_Flags_t flags);
{gex_Event_t,int} gex_VIS_IndexedPut{NB,NBI,Blocking}(
        gex_TM_t tm, gex_Rank_t dstrank,
        size_t dstcount, void * const dstlist[], size_t dstlen,
        size_t srccount, void * const srclist[], size_t srclen,
        gex_Flags_t flags);

//
// Strided Puts and Gets
//

// These operate similarly to the GASNet-1 prototype gasnet_{put,get}s_* API,
// but the metadata format is changing slightly in EX.  Notable changes:
// + The stride arrays change type from (const size_t[]) to (const ssize_t[])
// + The 'count[0]' datum moves to a new parameter 'elemsz', and the subsequent
//   elements 'count[1..stridelevels]' "slide down", meaning 'count' now references
//   an array with 'stridelevels' entries (down from 'stridelevels+1').
// Note that 'elemsz' need not match the "native" element size of the underlying
// datastructure, it just needs to indicate a size of contiguous data chunks
// (eg, it could be the length of an entire row of doubles stored contiguously).
// These interface changes will enable a future release of the Strided interface
// to expose more generalized data movement (specifically, transpose and reflection).
//
// The CURRENT release preserves metadata preconditions analogous to those
// in the GASNet-1 prototype, with 'count[0]' replaced by 'elemsz' - ie:
// For stridelevels == 0:
//   the operation is a contiguous copy of elemsz bytes, and the 
//   srcstrides, dststrides, count arguments are all ignored
// For stridelevels == 1, the following preconditions must hold:
//   srcstrides[0] >= elemsz
//   (and analogously for dststrides)
// For stridelevels > 1, the following preconditions must hold: 
//   srcstrides[0] >= elemsz AND 
//   srcstrides[1] >= (elemsz * count[0]) AND
//   ForAll i in [2..stridelevels) :
//     srcstrides[i] >= (count[i - 1] * srcstrides[i - 1])
//   (and analogously for dststrides)
// 
// These restrictions will be loosened in an upcoming release. [UNIMPLEMENTED]

{gex_Event_t,int} gex_VIS_StridedGet{NB,NBI,Blocking}(
        gex_TM_t tm,
        void *dstaddr, const ssize_t dststrides[],
        gex_Rank_t srcrank,
        void *srcaddr, const ssize_t srcstrides[],
        size_t elemsz, const size_t count[], size_t stridelevels,
        gex_Flags_t flags);
{gex_Event_t,int} gex_VIS_StridedPut{NB,NBI,Blocking}(
        gex_TM_t tm, gex_Rank_t dstrank,
        void *dstaddr, const ssize_t dststrides[],
        void *srcaddr, const ssize_t srcstrides[],
        size_t elemsz, const size_t count[], size_t stridelevels,
        gex_Flags_t flags);

// End of section describing APIs provided by gasnet_vis.h
//----------------------------------------------------------------------

// vim: syntax=c
