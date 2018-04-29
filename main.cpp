#include <upcxx/upcxx.hpp>
#include <iostream>

using namespace std;

int main(int argc, char *argv[]) {
    // setup UPC++ runtime
    upcxx::init();

    // upcxx::rank_me() - get number for this rank
    cout << "Hello world from rank " << upcxx::rank_me() << endl;

    // close down UPC++ runtime
    upcxx::finalize();
    return 0;
}
