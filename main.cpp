#include <upcxx/upcxx.hpp>
#include <iostream>
#include <fstream>
#include <sstream>
#include <algorithm>
#include <numeric>
#include <vector>
#include <future>
#include <limits>
#include <utility>

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
        int min_index = round(static_cast<double>(myid) / numprocs * size); //start from this index
        int limit = round(static_cast<double>(myid + 1) / numprocs * size);
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
    upcxx::global_ptr<int> final_data = nullptr;
    if (myid == 0)
    {
        vector<int> piv{};
        for (int i = 0; i < numprocs; i++) //each thread
        {
            int min_index = round(static_cast<double>(i) / numprocs * size); //start from this index
            int limit = round(static_cast<double>(i + 1) / numprocs * size);
            int max_index = limit > size ? size : limit; //end before this
            for (int j = 0; j < numprocs; j++)
            { //find thread_nr pivots
                auto fut = rget(global_data + min_index + round(j * static_cast<double>(max_index - 1 - min_index) / (numprocs + 1)));
                fut.wait();
                piv.push_back(fut.result());
            }
        }
        sort(begin(piv), end(piv));
        cout<<"Piv: ";
        for (const auto &e : piv)
            cout << e << " ";
        cout << endl;
        vector<int> pivots{};
        final_data = upcxx::new_array<int>(size);
        for (int i = 1; i < numprocs; i++) //select pivots value
            pivots.push_back(piv[numprocs * i]);
        pivots.push_back(std::numeric_limits<int>::max()); //fake max pivot for iteration in phase iv

        cout << "Pivots: ";
        for (const auto &e : pivots)
            cout << e << " ";
        cout << endl;

        // PHASE IV
        vector<int> ind(numprocs); //indexes for iteration over final_data
        fill(begin(ind), end(ind), 0);
        vector<pair<int, int>> piv_ind{}; //pivot's indexes <start, max> for each thread
        for (int i = 0; i < numprocs; i++)
        {
            int min_index = round(static_cast<double>(i) / numprocs * size); //start from this index
            int limit = round(static_cast<double>(i + 1) / numprocs * size);
            int max_index = limit > size ? size : limit; //end before this
            piv_ind.push_back(make_pair(min_index, max_index));
        }
        cout << "Pivots indexes: ";
        for (const auto &e : piv_ind)
            cout << get<0>(e) << ":" << get<1>(e) << " ";
        cout << endl;

        for (int i = 0; i < numprocs; i++)
        {                     //each thread
            int curr_piv = 0; //current pivot
            int range = get<1>(piv_ind[i]) - get<0>(piv_ind[i]);
            for (int j = 0; j < range; j++)
            {
                auto fut = rget(global_data + j + get<0>(piv_ind[i]));
                fut.wait();
                int v = fut.result();
                if (v < pivots[curr_piv])
                {
                    upcxx::rput(v, final_data + get<0>(piv_ind[curr_piv]) + ind[curr_piv]).wait();
                    ind[curr_piv]++;
                }
                else
                { //retry with next pivot
                    curr_piv++;
                    j--;
                    continue;
                }
            }
        }
        cout << "Ind: ";
        for (const auto &e : ind)
            cout << e << " ";
        cout << endl;
        //upcxx::delete_array(global_data);
    }
    final_data = upcxx::broadcast(final_data, 0).wait();

    // PHASE V
    {
        int min_index = round(static_cast<double>(myid) / numprocs * size); //start from this index
        int limit = round(static_cast<double>(myid + 1) / numprocs * size);
        int max_index = limit > size ? size : limit; //end before this
        vector<int> local_data{};
        for (int i = min_index; i < max_index; i++)
        {
            auto fut = rget(final_data + i);
            fut.wait();
            local_data.push_back(fut.result());
        }
        sort(begin(local_data), end(local_data));
        for (int i = 0; i < local_data.size(); i++)
            upcxx::rput(local_data[i], final_data + min_index + i).wait();
        // cout << "ID: " << myid << "  start  " << min_index << "   stop  " << max_index << endl;
    }

    //Check if sorted
    if (myid == 0)
    {
        vector<int> check{};
        for (int i = 0; i < size; i++)
        {
            auto fut = rget(final_data + i);
            fut.wait();
            check.push_back(fut.result());
        }
        cout << "Is it sorted: " << is_sorted(begin(check), end(check)) << endl;
    }
    //COUT TEST SECTION
    // if (myid == 0)
    //     cout << "liczba wątków: " << numprocs << endl;
    // if (myid == 2)
    // {
    //     auto fut = rget(global_data_size);
    //     fut.wait();
    //     cout << "Ilosc elem: " << fut.result() << endl;
    // }
    // upcxx::barrier();
    // if (myid == 2)
    // {
    //     for (int i = 0; i < numprocs - 1; i++)
    //     {
    //         auto fut = rget(pivots + i);
    //         fut.wait();
    //         cout << fut.result() << " ";
    //     }
    //     cout << endl;
    // }
    if (myid == 2)
    {
        cout << "Final data: ";
        for (int i = 0; i < size; i++)
        {
            auto fut = rget(final_data + i);
            fut.wait();
            cout << fut.result() << " ";
        }
        cout << endl;
    }

    if (myid == 1)
    {
        cout << "Global data: ";
        for (int i = 0; i < size; i++)
        {
            auto fut = rget(global_data + i);
            fut.wait();
            cout << fut.result() << " ";
        }
        cout << endl;
    }

    // close down UPC++ runtime
    upcxx::finalize();
    return 0;
}
