//c
// Created by user on 2019-12-21.
//

const int PRIME_TEST_LIMIT = 999999;
int sieve_of_eratosthenes[PRIME_TEST_LIMIT + 1];
bool sieve_calculated = false;

#include "number_fight.h"

set<int> collect_fg(multiset<int> a, multiset<int> b) {
    set<int> new_a;
    for(int n : a) {
        new_a.insert(n);
    }
    set<int> fg;
    for(int n : new_a) {
        if(b.find(n) != b.end()) {
            fg.insert(n);
        }
    }
    return fg;
}

int multiple_fg(set<int> fg) {
    int mux = 1;
    for(int n : fg) {
        mux *= n;
    }
    return mux;
}

void make_sieve() {
    sieve_of_eratosthenes[0] = -1;
    sieve_of_eratosthenes[1] = -1;
    for(int i=2; i<=PRIME_TEST_LIMIT; i++) {
        sieve_of_eratosthenes[i] = i;
    }
    for(int i=2; i*i<=PRIME_TEST_LIMIT; i++) {
        if(sieve_of_eratosthenes[i] == i) {
            for(int j=i*i; j<=PRIME_TEST_LIMIT; j+=i) {
                sieve_of_eratosthenes[j] = i;
            }
        }
    }
    sieve_calculated = true;
}

bool is_prime(int num) {
    if (!sieve_calculated) {
        make_sieve();
    }
    return sieve_of_eratosthenes[num] == num;
}

multiset<int> factorize(int num) {
    if (!sieve_calculated) {
        make_sieve();
    }
    multiset<int> result;
    while(num > 1) {
        result.insert(sieve_of_eratosthenes[num]);
        num /= sieve_of_eratosthenes[num];
    }
    if(result.empty()) {
        result.insert(1);
    }
    return result;
}