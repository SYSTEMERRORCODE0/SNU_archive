//
// Created by user on 2019-12-22.
//

#include "number_vs_number.h"
#include "number_fight.cpp"

pair<int, int> fight_result(int a, int b, int g) {
    pair<int, int> both_fight_result = both_fight(a, b, g);
    pair<int, int> a_fight_result = a_fight(a, b, g);
    pair<int, int> b_fight_result = b_fight(a, b, g);
    pair<int, int> not_fight_result = not_fight(a, b, g);

    int a_fight = will_a_fight(both_fight_result, a_fight_result, b_fight_result, not_fight_result);
    int b_fight = will_b_fight(both_fight_result, a_fight_result, b_fight_result, not_fight_result);
    //a or b_fight : 1 = true, 0 = false, -1 = different
    if(a_fight == -1) {
        if(a >= b) a_fight = 0; //false, not fight
        else a_fight = 1;
    }
    if(b_fight == -1) {
        if(b >= a) b_fight = 0; //false, not fight
        else b_fight = 1;
    }

    pair<int, int> result;
    if(a_fight == 1 && b_fight == 1) {
        result = both_fight_result;
    } else if(a_fight == 1 && b_fight == 0) {
        result = a_fight_result;
    } else if(a_fight == 0 && b_fight == 1) {
        result = b_fight_result;
    } else {
        result = not_fight_result;
    }

    return result;
}

pair<int, int> both_fight(int a, int b, int g) {
    return pair<int, int>(a/g, b/g);
}

pair<int, int> a_fight(int a, int b, int g) {
    int damage = b - b/g;
    if(b % 7 == 0) return pair<int, int>(if_under_one(a - damage / 2), if_under_one(b - damage / 2));
    else return pair<int, int>(a, b - damage);
}

pair<int, int> b_fight(int a, int b, int g) {
    int damage = a - a/g;
    if(a % 7 == 0) return pair<int, int>(if_under_one(a - damage / 2), if_under_one(b - damage / 2));
    else return pair<int, int>(if_under_one(a - damage), b);
}

pair<int, int> not_fight(int a, int b, int g) {
    return pair<int, int>(a, b);
}

int will_a_fight(pair<int, int> both, pair<int, int> a, pair<int, int> b, pair<int, int> neither) {
    bool when_b_not_fight = a.first >= neither.first;
    bool when_b_fight = both.first >= b.first;
    if(when_b_not_fight == when_b_fight) return when_b_fight;
    else return -1;
}

int will_b_fight(pair<int, int> both, pair<int, int> a, pair<int, int> b, pair<int, int> neither) {
    bool when_a_not_fight = b.second >= neither.second;
    bool when_a_fight = both.second >= a.second;
    if(when_a_not_fight == when_a_fight) return when_a_fight;
    else return -1;
}

int if_under_one(int n) {
    return n >= 1 ? n : 1;
}