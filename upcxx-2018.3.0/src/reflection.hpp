#ifndef _b61286c5_ccd4_4f8b_b1fc_fd318d666f5e
#define _b61286c5_ccd4_4f8b_b1fc_fd318d666f5e

#include <array>
#include <cstdint>
#include <utility>
#include <iostream>
#include <tuple>
#include <type_traits>


////////////////////////////////////////////////////////////////////////
// reflection of class/struct members.

/* The easiest way to enable reflection for your class is:
 * 
 * struct my_type {
 *   int foo;
 *   float bar;
 *   
 *   // `Me` will either be `my_type` or `const my_type`.
 *   template<typename Re, typename Me>
 *   static void reflect(Re &re, Me &me) {
 *     re(me.foo);
 *     re(me.bar);
 *   }
 * };
 */

// The default ADL method for reflection just considers its subject
// entirely opaque.
template<typename Reflector, typename Subject>
inline void reflect(Reflector &re, Subject &&x) {
  re.opaque(std::forward<Subject>(x));
}

namespace upcxx {
  // How to apply a reflector on a subject. May be specialized per type
  // but rarely is since default implementation finds a "reflect" associated
  // with T via ADL.
  template<typename Subject>
  struct reflection {
    template<typename Reflector, typename Subject1>
    void operator()(Reflector &re, Subject1 &&subj) {
      reflect(re, subj);
    }
  };
  
  // Invoke a reflector upon a subject object.
  template<typename Reflector, typename Subject>
  void reflect_upon(Reflector &re, Subject &&subj) {
    reflection<typename std::decay<Subject>::type>()(re, std::forward<Subject>(subj));
  }
}


////////////////////////////////////////////////////////////////////////
// Reflection based hashing

namespace upcxx {
  struct fast_hasher {
    std::size_t s;
    
    fast_hasher(std::size_t salt):
      s{salt} {
    }
    
    void operator()(std::size_t x) {
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
      s ^= x + 0x9e3779b9 + (s<<6) + (s>>2);
    }
    
    std::size_t result() const {
      return s;
    }
  };
  
  template<typename Hasher>
  struct hasher_reflector {
    Hasher &h;
    
    template<typename T>
    void operator()(const T &x) {
      reflect_upon(*this, x);
    }
    
    template<typename T>
    void opaque(const T &x) {
      h(std::hash<T>()(x));
    }
  };
  
  
  //////////////////////////////////////////////////////////////////////
  // fast_hashing: Drop-in for std::hash that uses reflection.
  
  template<typename T>
  struct fast_hashing {
    std::size_t operator()(const T &x, std::size_t salt=0) const {
      fast_hasher h{salt};
      hasher_reflector<fast_hasher> re{h};
      reflect_upon(re, x);
      return h.result();
    }
  };
  
  template<typename T>
  inline std::size_t fast_hash(const T &x, std::size_t salt=0) {
    return fast_hashing<T>()(x, salt);
  }


  //////////////////////////////////////////////////////////////////////
  // mod2n_hashing, mod2n_hash
  
  template<int bit_n>
  struct integer_golden_ratio_bits;
  
  template<> struct integer_golden_ratio_bits<32> {
    static constexpr std::uint32_t value = 0x9e3779b1u; // prime!
  };
  template<> struct integer_golden_ratio_bits<64> {
    static constexpr std::uint64_t value = 0x9e3779b97f4a7c15u; // not prime, try harder?
  };
  
  template<typename T>
  struct integer_golden_ratio {
    static constexpr T value = integer_golden_ratio_bits<8*sizeof(T)>::value;
  };
  
  template<typename T>
  struct mod2n_hashing {
    std::size_t operator()(const T &x, int bit_n) const {
      if(bit_n == 0)
        return 0;
      else {
        std::size_t h = fast_hash(x);
        h ^= h >> 4*sizeof(std::size_t);
        h *= upcxx::integer_golden_ratio<std::size_t>::value;
        h >>= 8*sizeof(std::size_t) - bit_n;
        return h;
      }
    }
  };
  
  template<typename T>
  inline std::size_t mod2n_hash(const T &x, int bits) {
    return mod2n_hashing<T>()(x, bits);
  }
  
  
  //////////////////////////////////////////////////////////////////////
  // reflection<std::tuple>
  
  template<typename Tup, int i, int n>
  struct reflection_tuple {
    template<typename Re, typename Tup1>
    void operator()(Re &re, Tup1 &&x) const {
      re(std::get<i>(x));
      reflection_tuple<Tup,i+1,n>()(re, static_cast<Tup1&&>(x));
    }
  };
  template<typename Tup, int n>
  struct reflection_tuple<Tup,n,n> {
    template<typename Re, typename Tup1>
    void operator()(Re &re, Tup1 &&x) const {}
  };

  
  template<typename ...Ts>
  struct reflection<std::tuple<Ts...>> {
    template<typename Re, typename Tup1>
    void operator()(Re &re, Tup1 &&x) const {
      reflection_tuple<std::tuple<Ts...>,0,sizeof...(Ts)>()(re, static_cast<Tup1&&>(x));
    }
  };
  
  
  //////////////////////////////////////////////////////////////////////
  // reflection<std::pair>
  
  template<typename A, typename B>
  struct reflection<std::pair<A,B>> {
    template<typename Re, typename Pair>
    void operator()(Re &re, Pair &&x) const {
      re(x.first);
      re(x.second);
    }
  };
  
  
  //////////////////////////////////////////////////////////////////////
  // reflection<std::array>
  
  template<typename T, std::size_t n>
  struct reflection<std::array<T,n>> {
    template<typename Re, typename Array>
    void operator()(Re &re, Array &&x) const {
      for(std::size_t i=0; i < n; i++)
        re(x[i]);
    }
  };
}


////////////////////////////////////////////////////////////////////////
// ostream& << upcxx::print(T): Reflection based iostream printing.

namespace upcxx {
  struct print_reflector {
    std::ostream &o;
    bool comma;
    
    template<typename T>
    void opaque(const T &x) {
      if(comma) o << ',';
      comma = true;
      o << x;
    }
    template<typename T>
    void operator()(const T &x) {
      this->opaque(x);
    }
  };
  
  template<typename T>
  struct print_proxy {
    T const &subject;
    
    friend std::ostream& operator<<(std::ostream &o, print_proxy &me) {
      print_reflector re{o, false};
      o << '{';
      upcxx::reflect_upon(re, me.subject);
      o << '}';
      return o;
    }
  };
  
  template<typename T>
  inline print_proxy<T> print(T const &subject) {
    return print_proxy<T>{subject};
  }
}

#endif
