//
// Created by USER on 2019-12-22.
//

#include <vector>
#include <algorithm>
#include "player_battle.h"
#include "number_vs_number.cpp"

int choose_number(string type, multiset<int> me, multiset<int> op) {
    int result;
    if(type == "Maximize-Gain") {
        result = maximize_gain(me, op);
    } else if(type == "Minimize-Loss") {
        result = minimize_loss(me, op);
    } else {
        result = minimize_regret(me, op);
    }
    return result;
}

int maximize_gain(multiset<int> me, multiset<int> op) {
    pair<int, int> max(0, -1000000); //max_a, max_a_prime
    for(int a : me) {
        for(int b : op) {
            int g = multiple_fg(collect_fg(factorize(a), factorize(b)));
            pair<int, int> result = fight_result(a, b, g);
            if(max.second < result.first - a) {
                max.second = result.first - a;
                max.first = a;
            }
        }
    }
    return max.first;
}

int minimize_loss(multiset<int> me, multiset<int> op) {
    pair<int, int> max(0, -1000000); //min_a, min_a_prime
    for(int a : me) {
        int min = 1000000;
        for(int b : op) {
            int g = multiple_fg(collect_fg(factorize(a), factorize(b)));
            pair<int, int> result = fight_result(a, b, g);
            if(min > result.first - a) min = result.first - a;
        }
        if(max.second < min) {
            max.second = min;
            max.first = a;
        }
    }
    return max.first;
}

int minimize_regret(multiset<int> me, multiset<int> op) {
    vector<pair<int, int>> max_vec; // a, a_max
    vector<pair<int, int>> min_vec;
    vector<pair<int, int>> regret;
    for(int a : me) {
        int min = 1000000;
        int max = -1000000;
        for(int b : op) {
            int g = multiple_fg(collect_fg(factorize(a), factorize(b)));
            pair<int, int> result = fight_result(a, b, g);
            if(min > result.first - a) min = result.first - a;
            if(max < result.first - a) max = result.first - a;
        }
        max_vec.push_back(pair<int, int>(a, max));
        min_vec.push_back(pair<int, int>(a, min));
    }

    pair<int, int> first_max(0, -1000000);   //index, max
    pair<int, int> second_max(0, -1000000);

    for(int i = 0; i < max_vec.size(); i++) {
        if(max_vec.at(i).second > first_max.second) {
            second_max.second = first_max.second;
            second_max.first = first_max.first;
            first_max.first = i;
            first_max.second = max_vec.at(i).second;
        } else if(max_vec.at(i).second > second_max.second) {
            second_max.first = i;
            second_max.second = max_vec.at(i).second;
        }
    }
    for(int i = 0; i < min_vec.size(); i++) {
        if(i != first_max.first) {
            regret.push_back(pair<int, int>(min_vec.at(i).first, first_max.second - min_vec.at(i).second));
        } else {
            regret.push_back(pair<int, int>(min_vec.at(i).first, second_max.second - min_vec.at(i).second));
        }
    }
    sort(regret.begin(), regret.end(), comp);
    return regret.at(0).first;
}

bool comp(pair<int, int> a, pair<int, int> b) {
    return a.second < b.second;
}

int total_score(multiset<int> s) {
    int score = 0;
    for(int n : s) {
        score += n;
    }
    return score;
}