//
//  Copyright (c) 2002-2023, Rice University.
//  See the file LICENSE for details.
//
//  Simple selection sort, shows a couple of loops, some C++
//  templates.
//

#include <stdlib.h>
#include <iostream>
#include <list>

using namespace std;

typedef list <long> llist;

int main(int argc, char **argv)
{
    llist olist, nlist;
    long n, N, sum;

    N = 80000;

    if (argc > 1) {
        N = atol(argv[1]);
    }

    sum = 0;
    for (n = 1; n <= N; n += 2) {
        olist.push_front(n);
        olist.push_back(n + 1);
        sum += 2 * n + 1;
    }

    cout << "orig list:  " << N << "  " << sum << endl;

    sum = 0;
    while (olist.size() > 0) {
        auto min = olist.begin();

        for (auto it = olist.begin(); it != olist.end(); ++it) {
            if (*it < *min) {
                min = it;
            }
        }
        sum += *min;
        nlist.push_back(*min);
        olist.erase(min);
    }

    cout << "new list:   " << N << "  " << sum << endl;

    return 0;
}
