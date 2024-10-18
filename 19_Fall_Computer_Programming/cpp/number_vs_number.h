//
// Created by user on 2019-12-22.
//
using namespace std;

#ifndef EXAM_NUMBER_VS_NUMBER_H
#define EXAM_NUMBER_VS_NUMBER_H

pair<int, int> fight_result(int a, int b, int g);
pair<int, int> both_fight(int a, int b, int g);
pair<int, int> a_fight(int a, int b, int g);
pair<int, int> b_fight(int a, int b, int g);
pair<int, int> not_fight(int a, int b, int g);
int will_a_fight(pair<int, int> both, pair<int, int> a, pair<int, int> b, pair<int, int> neither);
int will_b_fight(pair<int, int> both, pair<int, int> a, pair<int, int> b, pair<int, int> neither);
int if_under_one(int n);

#endif //EXAM_NUMBER_VS_NUMBER_H
