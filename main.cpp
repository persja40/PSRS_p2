#include <upcxx/upcxx.hpp>
#include <iostream>
#include <fstream>
#include <sstream>
#include <algorithm>
#include <numeric>
#include <vector>

using namespace std;

int main(int argc, char *argv[])
{
    // setup UPC++ runtime
    upcxx::init();
    vector<int> data_to_sort{};
    int data_to_sort_size;
    int numprocs = upcxx::rank_n();
    int myid = upcxx::rank_me();

    // PHASE I
    // read data from file
    if (myid == 0)
    {
        string input_file;
        if (argc == 2)
            input_file = argv[1];
        else
            input_file = "example.txt";
        ifstream ifile;
        ifile.open(input_file);
        while (!ifile.eof())
        {
            int t;
            ifile >> t;
            data_to_sort.push_back(t);
        }
        ifile.close();
        data_to_sort_size = data_to_sort.size();
    }

    //COUT TEST SECTION
    if (myid == 0)
        cout << "liczba wątków: " << numprocs << endl;

    for (const auto &e : data_to_sort)
        cout << e << " ";
    cout << endl;
    // close down UPC++ runtime
    upcxx::finalize();
    return 0;
}
