#include <upcxx/upcxx.hpp>
#include <iostream>
#include <fstream>
#include <sstream>
#include <algorithm>
#include <numeric>
#include <vector>
#include <future>

using namespace std;

int main(int argc, char *argv[])
{
    // setup UPC++ runtime
    upcxx::init();
    int numprocs = upcxx::rank_n();
    int myid = upcxx::rank_me();

    // PHASE I
    // read data from file
    upcxx::global_ptr<int> global_data_size = nullptr;
    upcxx::global_ptr<int> global_data = nullptr;
    if (myid == 0)
    {
        string input_file;
        if (argc == 2)
            input_file = argv[1];
        else
            input_file = "example.txt";
        ifstream ifile;
        vector<int> data_to_sort{};
        ifile.open(input_file);
        while (!ifile.eof())
        {
            int t;
            ifile >> t;
            data_to_sort.push_back(t);
        }
        ifile.close();
        global_data_size = upcxx::new_<int>(data_to_sort.size());
        global_data = upcxx::new_array<int>(data_to_sort.size());
        auto iter = global_data;
        for (int i = 0; i < data_to_sort.size(); i++)
        {
            upcxx::rput(data_to_sort[i], iter).wait();
            iter++;
        }
    }
    global_data_size = upcxx::broadcast(global_data_size, 0).wait();
    global_data = upcxx::broadcast(global_data, 0).wait();

    // PHASE II

    //COUT TEST SECTION
    if (myid == 0)
        cout << "liczba wątków: " << numprocs << endl;
    if (myid == 2){
        auto fut = rget ( global_data_size );
        fut.wait();
        cout<<"Ilosc elem: "<<fut.result()<<endl;
    }
    // close down UPC++ runtime
    upcxx::finalize();
    return 0;
}
