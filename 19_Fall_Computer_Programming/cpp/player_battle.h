//
// Created by USER on 2019-12-22.
//

#include <string>
#include <set>
using namespace std;

#ifndef CPP_PLAYER_BATTLE_H
#define CPP_PLAYER_BATTLE_H

int choose_number(string type, multiset<int> me, multiset<int> op);
int maximize_gain(multiset<int> me, multiset<int> op);
int minimize_loss(multiset<int> me, multiset<int> op);
int minimize_regret(multiset<int> me, multiset<int> op);
bool comp(pair<int, int> a, pair<int, int> b);

int total_score(multiset<int> s);

#endif //CPP_PLAYER_BATTLE_H
