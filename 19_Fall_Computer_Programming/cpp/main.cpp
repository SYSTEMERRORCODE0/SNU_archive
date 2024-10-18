#include <iostream>
#include <string>
#include <utility>
#include <set>
#include <queue>
#include <vector>
#include <tuple>
#include "player_battle.cpp"

using namespace std;

/* =======START OF PRIME-RELATED HELPERS======= */
/*
 * The code snippet below AS A WHOLE does the primality
 * test and integer factorization. Feel free to move the
 * code to somewhere more appropriate to get your codes
 * more structured.
 *
 * You don't have to understand the implementation of it.
 * But if you're curious, refer to the sieve of Eratosthenes
 *
 * If you want to just use it, use the following 2 functions.
 *
 * 1) bool is_prime(int num):
 *     * `num` should satisfy 1 <= num <= 999999
 *     - returns true if `num` is a prime number
 *     - returns false otherwise (1 is not a prime number)
 *
 * 2) multiset<int> factorize(int num):
 *     * `num` should satisfy 1 <= num <= 999999
 *     - returns the result of factorization of `num`
 *         ex ) num = 24 --> result = { 2, 2, 2, 3 }
 *     - if `num` is 1, it returns { 1 }
 */



/* =======END OF PRIME-RELATED HELPERS======= */

/* =======START OF STRING LITERALS======= */
/* Use this code snippet if you want */

const string MAXIMIZE_GAIN = "Maximize-Gain";
const string MINIMIZE_LOSS = "Minimize-Loss";
const string MINIMIZE_REGRET = "Minimize-Regret";

/* =======END OF STRING LITERALS======= */


/* =======START OF TODOs======= */

pair<int, int> number_fight(int a, int b) {
    // TODO 1-1
    multiset<int> fa = factorize(a), fb = factorize(b);
    set<int> fg = collect_fg(fa, fb);
    int mux_fg = multiple_fg(fg);
    return pair<int, int>(a/mux_fg, b/mux_fg);
}

pair<int, int> number_vs_number(int a, int b) {
    // TODO 1-2
    multiset<int> fa = factorize(a), fb = factorize(b);
    set<int> fg = collect_fg(fa, fb);
    int mux_fg = multiple_fg(fg);
    return fight_result(a, b, mux_fg);
}

pair<multiset<int>, multiset<int>> player_battle(
        string type_a, multiset<int> a, string type_b, multiset<int> b
) {
    // TODO 1-3
    int a_choose = choose_number(type_a, a, b);
    int b_choose = choose_number(type_b, b, a);
    a.erase(a.find(a_choose));
    b.erase(b.find(b_choose));
    pair<int, int> result = number_vs_number(a_choose, b_choose);
    a.insert(result.first);
    b.insert(result.second);
    return pair<multiset<int>, multiset<int>>(a, b);
}

pair<multiset<int>, multiset<int>> player_vs_player(
        string type_a, multiset<int> a, string type_b, multiset<int> b
) {
    // TODO 1-4
    multiset<int> save_a(a);
    multiset<int> save_b(b);
    pair<multiset<int>, multiset<int>> change = player_battle(type_a, a, type_b, b);
    a = change.first;
    b = change.second;
    while(save_a != a && save_b != b) {
        save_a = multiset<int>(a);
        save_b = multiset<int>(b);
        pair<multiset<int>, multiset<int>> change = player_battle(type_a, a, type_b, b);
        a = multiset<int>(change.first);
        b = multiset<int>(change.second);
    }
    return pair<multiset<int>, multiset<int>>(a, b);
}

int tournament(vector<pair<string, multiset<int>>> players) {
    // TODO 1-5
    queue<int> survived;
    for(int i = 0; i < players.size(); i++) {
        survived.push(i);
    }
    while(survived.size() > 1) {
        queue<int> temp;
        while(!survived.empty()) {
            int first_player_id, second_player_id;
            first_player_id = survived.front();
            survived.pop();
            if (!survived.empty()) {
                second_player_id = survived.front();
                survived.pop();
                string saved_type_a(players.at(first_player_id).first);
                multiset<int> saved_a(players.at(first_player_id).second);
                string saved_type_b(players.at(second_player_id).first);
                multiset<int> saved_b(players.at(second_player_id).second);
                pair<multiset<int>, multiset<int>> result = player_vs_player(saved_type_a, saved_a, saved_type_b,
                                                                             saved_b);
                int first_player_score = total_score(result.first);
                int second_player_score = total_score(result.second);
                if (first_player_score == second_player_score) {
                    if (result.first.size() >= result.second.size()) {
                        temp.push(first_player_id);
                    } else {
                        temp.push(second_player_id);
                    }
                } else if (first_player_score > second_player_score) {
                    temp.push(first_player_id);
                } else {
                    temp.push(second_player_id);
                }
            } else {
                temp.push(first_player_id);
            }
        }
        survived = queue<int>(temp);
    }

    return survived.front();
}

int steady_winner(vector<pair<string, multiset<int>>> players) {
    // TODO 1-6
    vector<pair<int, int>> wins; //id, wins
    for(int i = 0; i < players.size(); i++) {
        wins.push_back(pair<int, int>(i, 0));
    }
    for(int i = 0; i < players.size(); i++) {
        int winner = tournament(players) + i;
        if(winner >= players.size()) winner -= players.size();
        wins.at(winner).second++;
        pair<string, multiset<int>> temp = players.front();
        players.erase(players.begin());
        players.push_back(temp);
    }
    pair<int, int> max(-1, -1); //id, wins
    for(int i = 0; i < players.size(); i++) {
        if(wins.at(i).second > max.second) {
            max = pair<int, int>(i, wins.at(i).second);
        }
    }
    return max.first;
}

/* =======END OF TODOs======= */

/* =======START OF THE MAIN CODE======= */
/* Please do not modify the code below */

typedef pair<string, multiset<int>> player;

player scan_player() {
    multiset<int> numbers;
    string player_type; int size;
    cin >> player_type >> size;
    for(int i=0;i<size;i++) {
        int t; cin >> t; numbers.insert(t);
    }
    return make_pair(player_type, numbers);
}

void print_multiset(const multiset<int>& m) {
    for(int number : m) {
        cout << number << " ";
    }
    cout << endl;
}

int main() {
    int question_number; cin >> question_number;
    if (question_number == 1) {
        int a, b; cin >> a >> b;
        tie(a, b) = number_fight(a, b);
        cout << a << " " << b << endl;
    } else if (question_number == 2) {
        int a, b; cin >> a >> b;
        tie(a, b) = number_vs_number(a, b);
        cout << a << " " << b << endl;
    } else if (question_number == 3 || question_number == 4) {
        auto a = scan_player();
        auto b = scan_player();
        multiset<int> a_, b_;
        if (question_number == 3) {
            tie(a_, b_) = player_battle(
                    a.first, a.second, b.first, b.second
            );
        } else {
            tie(a_, b_) = player_vs_player(
                    a.first, a.second, b.first, b.second
            );
        }
        print_multiset(a_);
        print_multiset(b_);
    } else if (question_number == 5 || question_number == 6) {
        int num_players; cin >> num_players;
        vector<player> players;
        for(int i=0;i<num_players;i++) {
            players.push_back(scan_player());
        }
        int winner_id;
        if (question_number == 5) {
            winner_id = tournament(players);
        } else {
            winner_id = steady_winner(players);
        }
        cout << winner_id << endl;
    }
    return 0;
}
/* =======END OF MAIN CODE======= */