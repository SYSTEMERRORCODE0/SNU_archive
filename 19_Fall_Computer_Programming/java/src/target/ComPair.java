package target;

import datastructure.Pair;

import java.util.Comparator;

public class ComPair implements Comparator<Pair<String, Pair<Integer, Integer>>> {

    @Override
    public int compare(Pair<String, Pair<Integer, Integer>> a, Pair<String, Pair<Integer, Integer>> b) {
        if(a.value.key == b.value.key){
            if(a.value.value == b.value.value) {
                return a.key.compareTo(b.key);
            } else if(a.value.value < b.value.value) {
                return -1;
            } else {
                return 1;
            }
        } else if(a.value.key > b.value.key) {
            return -1;
        } else {
            return 1;
        }
    }
}
