#include <upcxx/backend.hpp>
#include <iostream>

int main() {
  upcxx::init();
  
  std::cout<<"Hello from "<<upcxx::rank_me()<<" of "<<upcxx::rank_n()<<"\n";
  
  upcxx::finalize();
  return 0;
}
