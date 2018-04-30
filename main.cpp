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
    auto fut = rget(global_data_size);
    fut.wait();
    int size = fut.result();
    {
        int min_index = static_cast<double>(myid) / numprocs * size; //start from this index
        int limit = static_cast<double>(myid + 1) / numprocs * size;
        int max_index = limit > size ? size : limit; //end before this
        vector<int> local_data{};
        for (int i = min_index; i < max_index; i++)
        {
            auto fut = rget(global_data + i);
            fut.wait();
            local_data.push_back(fut.result());
        }
        sort(begin(local_data), end(local_data));
        for (int i = 0; i < local_data.size(); i++)
            upcxx::rput(local_data[i], global_data + min_index + i).wait();
        // cout << "ID: " << myid << "  start  " << min_index << "   stop  " << max_index << endl;
    }

    // PHASE III
    upcxx::barrier();
    upcxx::global_ptr<int> pivots = nullptr;
    if (myid == 0)
    {
        vector<int> piv{};
        for (int i = 0; i < numprocs; i++) //each thread
        {
            int min_index = static_cast<double>(i) / numprocs * size; //start from this index
            int limit = static_cast<double>(i + 1) / numprocs * size;
            int max_index = limit > size ? size : limit; //end before this
            for (int j = 0; j < numprocs; j++)
            { //find thread_nr pivots
                auto fut = rget(global_data + min_index + round(j * static_cast<double>(max_index - 1 - min_index) / (numprocs + 1)));
                fut.wait();
                piv.push_back(fut.result());
            }
        }
        sort(begin(piv), end(piv));
        // for (const auto &e : piv)
        //     cout << e << " ";
        // cout << endl;
        pivots = upcxx::new_<int>(numprocs);
        for (int i = 1; i < numprocs; i++) //select pivots value
            upcxx::rput(static_cast<double>(i)/(numprocs + 1), pivots + i).wait();
    }
    pivots = upcxx::broadcast(pivots, 0).wait();

    // PHASE IV

    //COUT TEST SECTION
    if (myid == 0)
        cout << "liczba wątków: " << numprocs << endl;
    if (myid == 2)
    {
        auto fut = rget(global_data_size);
        fut.wait();
        cout << "Ilosc elem: " << fut.result() << endl;
    }
    // close down UPC++ runtime
    upcxx::finalize();
    return 0;
}
