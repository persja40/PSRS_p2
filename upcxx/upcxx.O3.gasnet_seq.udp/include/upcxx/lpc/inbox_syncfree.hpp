#ifndef _b68cb319_851a_4f86_bf16_a95c9b16a93f
#define _b68cb319_851a_4f86_bf16_a95c9b16a93f

#include <upcxx/diagnostic.hpp>

namespace upcxx {
  namespace detail {
    struct lpc_inbox_syncfree_base {
      struct lpc {
        lpc *next;
        virtual void execute_and_delete() = 0;
      };
      
      template<typename Fn>
      struct lpc_impl final: lpc {
        Fn fn_;
        lpc_impl(Fn fn): fn_{std::move(fn)} {}
        
        void execute_and_delete() {
          this->fn_();
          delete this;
        }
      };
    };
  }
  
  template<int queue_n>
  struct lpc_inbox_syncfree: detail::lpc_inbox_syncfree_base {
    lpc *head_[queue_n];
    lpc **tailp_[queue_n];
  
  public:
    lpc_inbox_syncfree();
    ~lpc_inbox_syncfree();
    lpc_inbox_syncfree(lpc_inbox_syncfree const&) = delete;
    
    template<typename Fn1>
    void send(int q, Fn1 &&fn);
    
    // returns num lpc's executed
    int burst(int q, int burst_n = 100);
  };
  
  //////////////////////////////////////////////////////////////////////
  
  template<int queue_n>
  lpc_inbox_syncfree<queue_n>::lpc_inbox_syncfree() {
    for(int q=0; q < queue_n; q++) {
      head_[q] = nullptr;
      tailp_[q] = &head_[q];
    }
  }
  
  template<int queue_n>
  lpc_inbox_syncfree<queue_n>::~lpc_inbox_syncfree() {
    for(int q=0; q < queue_n; q++) {
      UPCXX_ASSERT(this->head_[q] == nullptr, "Abandoned lpc's detected.");
    }
  }
  
  template<int queue_n>
  template<typename Fn1>
  void lpc_inbox_syncfree<queue_n>::send(int q, Fn1 &&fn) {
    using Fn = typename std::decay<Fn1>::type;
    
    auto *m = new lpc_inbox_syncfree::lpc_impl<Fn>{std::forward<Fn1>(fn)};
    m->next = nullptr;
    *this->tailp_[q] = m;
    this->tailp_[q] = &m->next;
  }
}
#endif
