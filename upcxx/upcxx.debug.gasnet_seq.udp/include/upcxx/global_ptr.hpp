#ifndef _bcef2443_cf3b_4148_be6d_be2d24f46848
#define _bcef2443_cf3b_4148_be6d_be2d24f46848

/**
 * global_ptr.hpp
 */

#include <upcxx/backend.hpp>
#include <upcxx/diagnostic.hpp>

#include <cassert> // assert
#include <cstddef> // ptrdiff_t
#include <cstdint> // uintptr_t
#include <iostream> // ostream
#include <type_traits> // is_const, is_volatile

namespace upcxx {
  //////////////////////////////////////////////////////////////////////
  // Internal PSHM functions.
  // TODO: Rethink API, move to backend.hpp
  
  inline bool is_memory_shared_with(intrank_t r) {
    return r == upcxx::rank_me();
  }
  
  inline void *pshm_remote_addr2local(intrank_t r, void *addr) {
    return addr;
  }
  
  inline void *pshm_local_addr2remote(void *addr, intrank_t &rank_out) {
    rank_out = upcxx::rank_me();
    return addr;
  }
  
  //////////////////////////////////////////////////////////////////////
  
  namespace detail {
    struct global_ptr_ctor_internal{};
  }
  
  // Definition of global_ptr
  template<typename T>
  class global_ptr {
  public:
    static_assert(!std::is_const<T>::value && !std::is_volatile<T>::value,
                  "global_ptr<T> does not support cv qualification on T");

    using element_type = T;

    // null pointer represented with rank 0
    global_ptr(std::nullptr_t nil = nullptr):
      rank_{0},
      raw_ptr_{nullptr} {
    }

    explicit global_ptr(T *ptr) {
      if (ptr == nullptr) {
        raw_ptr_ = ptr;
        rank_ = 0; // null pointer represented with rank 0
      } else {
        raw_ptr_ = static_cast<T*>(pshm_local_addr2remote(ptr, rank_));
        UPCXX_ASSERT(raw_ptr_ && "address must be in shared segment");
      }
    }
    
    explicit global_ptr(
        detail::global_ptr_ctor_internal,
        intrank_t rank, T *raw
      ):
      rank_{rank},
      raw_ptr_{raw} {
    }
    
    bool is_local() const {
      return is_memory_shared_with(rank_);
    }

    bool is_null() const {
      return raw_ptr_ == nullptr;
    }

    T* local() const {
      return static_cast<T*>(pshm_remote_addr2local(rank_, raw_ptr_));
    }

    intrank_t where() const {
      return rank_;
    }

    global_ptr operator+(std::ptrdiff_t diff) const {
      return global_ptr(rank_, raw_ptr_ + diff);
    }

    global_ptr operator-(std::ptrdiff_t diff) const {
      return global_ptr(rank_, raw_ptr_ - diff);
    }

    std::ptrdiff_t operator-(global_ptr rhs) const {
      assert(rank_ == rhs.rank_ &&
             "operator- requires pointers to the same rank");
      return raw_ptr_ - rhs.raw_ptr_;
    }

    global_ptr& operator++() {
      return *this = *this + 1;
    }

    global_ptr operator++(int) {
      global_ptr old = *this;
      *this = *this + 1;
      return old;
    }

    global_ptr& operator--() {
      return *this = *this - 1;
    }

    global_ptr operator--(int) {
      global_ptr old = *this;
      *this = *this - 1;
      return old;
    }

    bool operator==(global_ptr rhs) const {
      return rank_ == rhs.rank_ && raw_ptr_ == rhs.raw_ptr_;
    }

    bool operator!=(global_ptr rhs) const {
      return rank_ != rhs.rank_ || raw_ptr_ != rhs.raw_ptr_;
    }

    // Comparison operators specify partial order
    bool operator<(global_ptr rhs) const {
      return raw_ptr_ < rhs.raw_ptr_;
    }

    bool operator<=(global_ptr rhs) const {
      return raw_ptr_ <= rhs.raw_ptr_;
    }

    bool operator>(global_ptr rhs) const {
      return raw_ptr_ > rhs.raw_ptr_;
    }

    bool operator>=(global_ptr rhs) const {
      return raw_ptr_ >= rhs.raw_ptr_;
    }

  private:
    friend struct std::less<global_ptr<T>>;
    friend struct std::less_equal<global_ptr<T>>;
    friend struct std::greater<global_ptr<T>>;
    friend struct std::greater_equal<global_ptr<T>>;
    friend struct std::hash<global_ptr<T>>;

    template<typename U, typename V>
    friend global_ptr<U> reinterpret_pointer_cast(global_ptr<V> ptr);

    template<typename U>
    friend std::ostream& operator<<(std::ostream &os, global_ptr<U> ptr);

    explicit global_ptr(intrank_t rank, T* ptr)
      : rank_(rank), raw_ptr_(ptr) {}
  
  public: //private!
    intrank_t rank_;
    T* raw_ptr_;
  };

  template <typename T>
  global_ptr<T> operator+(std::ptrdiff_t diff, global_ptr<T> ptr) {
    return ptr + diff;
  }

  template<typename T, typename U>
  global_ptr<T> reinterpret_pointer_cast(global_ptr<U> ptr) {
    return global_ptr<T>(ptr.rank_,
                         reinterpret_cast<T*>(ptr.raw_ptr_));
  }

  template<typename T>
  std::ostream& operator<<(std::ostream &os, global_ptr<T> ptr) {
    return os << "(gp: " << ptr.rank_ << ", " << ptr.raw_ptr_ << ")";
  }
} // namespace upcxx

// Specializations of standard function objects
namespace std {
  // Comparators specify total order
  template<typename T>
  struct less<upcxx::global_ptr<T>> {
    constexpr bool operator()(upcxx::global_ptr<T> lhs,
                              upcxx::global_ptr<T> rhs) const {
      return (lhs.rank_ < rhs.rank_ ||
             (lhs.rank_ == rhs.rank_ && lhs.raw_ptr_ < rhs.raw_ptr_));
    }
  };

  template<typename T>
  struct less_equal<upcxx::global_ptr <T>> {
    constexpr bool operator()(upcxx::global_ptr<T> lhs,
                              upcxx::global_ptr<T> rhs) const {
      return (lhs.rank_ < rhs.rank_ ||
             (lhs.rank_ == rhs.rank_ && lhs.raw_ptr_ <= rhs.raw_ptr_));
    }
  };

  template <typename T>
  struct greater<upcxx::global_ptr <T>> {
    constexpr bool operator()(upcxx::global_ptr<T> lhs,
                              upcxx::global_ptr<T> rhs) const {
      return (lhs.rank_ > rhs.rank_ ||
             (lhs.rank_ == rhs.rank_ && lhs.raw_ptr_ > rhs.raw_ptr_));
    }
  };

  template<typename T>
  struct greater_equal<upcxx::global_ptr <T>> {
    constexpr bool operator()(upcxx::global_ptr<T> lhs,
                              upcxx::global_ptr<T> rhs) const {
      return (lhs.rank_ > rhs.rank_ ||
             (lhs.rank_ == rhs.rank_ && lhs.raw_ptr_ >= rhs.raw_ptr_));
    }
  };

  template<typename T>
  struct hash<upcxx::global_ptr<T>> {
    std::size_t operator()(upcxx::global_ptr<T> gptr) const {
      /** Utilities derived from Boost, subject to the following license:

      Boost Software License - Version 1.0 - August 17th, 2003

      Permission is hereby granted, free of charge, to any person or organization
      obtaining a copy of the software and accompanying documentation covered by
      this license (the "Software") to use, reproduce, display, distribute,
      execute, and transmit the Software, and to prepare derivative works of the
      Software, and to permit third-parties to whom the Software is furnished to
      do so, all subject to the following:

      The copyright notices in the Software and this entire statement, including
      the above license grant, this restriction and the following disclaimer,
      must be included in all copies of the Software, in whole or in part, and
      all derivative works of the Software, unless such copies or derivative
      works are solely in the form of machine-executable object code generated by
      a source language processor.

      THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
      IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
      FITNESS FOR A PARTICULAR PURPOSE, TITLE AND NON-INFRINGEMENT. IN NO EVENT
      SHALL THE COPYRIGHT HOLDERS OR ANYONE DISTRIBUTING THE SOFTWARE BE LIABLE
      FOR ANY DAMAGES OR OTHER LIABILITY, WHETHER IN CONTRACT, TORT OR OTHERWISE,
      ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
      DEALINGS IN THE SOFTWARE.
      */
      std::uintptr_t h = reinterpret_cast<std::uintptr_t>(gptr.raw_ptr_);
      h ^= std::uintptr_t(gptr.rank_) + 0x9e3779b9 + (h<<6) + (h>>2);
      return std::size_t(h);
    }
  };
} // namespace std

#endif
