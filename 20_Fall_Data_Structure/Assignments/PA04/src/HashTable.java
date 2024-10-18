
public class HashTable {
    private int[] table;
    private int c1, c2, c3;
    private int delMarker = -1;
    private int tableSize;

    public HashTable(int n) {
        //TODO: fill your code
        this.table = new int[n];
        this.tableSize = n;
    }

    public void create(int c1, int c2, int c3) {
        //TODO: fill your code
        this.c1 = c1;
        this.c2 = c2;
        this.c3 = c3;
    }

    public void insert(int key) {
        //TODO: fill your code
        int h_key = key % tableSize;
        int index = (h_key + quadProb(key, 0)) % tableSize;
        for(int i = 1; table[index] > 0; i++) {
            index = (h_key + quadProb(key, i)) % tableSize;
        }
        table[index] = key;
        System.out.println("INSERT: " + key + ", INDEX: " + index);
    }

    public void delete(int key) {
        //TODO: fill your code
        int h_key = key % tableSize;
        int index = (h_key + quadProb(key, 0)) % tableSize;
        for(int i = 1; table[index] != key && table[index] != 0; i++) {
            index = (h_key + quadProb(key, i)) % tableSize;
        }
        if(table[index] == 0) {
            System.out.println("Failed to find " + key);
        } else {
            table[index] = delMarker;
            System.out.println("DELETE: " + key + ", INDEX: " + index);
        }
    }

    public void search(int key) {
        //TODO: fill your code
        int h_key = key % tableSize;
        int index = (h_key + quadProb(key, 0)) % tableSize;
        for(int i = 1; table[index] != key && table[index] != 0; i++) {
            index = (h_key + quadProb(key, i)) % tableSize;
        }
        if(table[index] == 0) {
            System.out.println("Failed to find " + key);
        } else {
            System.out.println("SEARCH: " + key + ", INDEX: " + index);
        }
    }

    public void avgProbes() {
        //TODO: fill your code
        float total_probes = 0;
        for(int j = 0; j < tableSize; j++) {
            int key = j;
            int h_key = key % tableSize;
            int i = 0;
            int index = (h_key + quadProb(key, i)) % tableSize;
            for(i = 1; table[index] > 0; i++) {
                index = (h_key + quadProb(key, i)) % tableSize;
            }
            total_probes += i;
            //System.out.println(i);
        }
        System.out.println("Average number of probes: " + (total_probes / tableSize));
    }

    private int quadProb(int k, int i) {
        //TODO: fill your code
        return (c1*i*i + c2*i + c3) % tableSize;
    }
}
