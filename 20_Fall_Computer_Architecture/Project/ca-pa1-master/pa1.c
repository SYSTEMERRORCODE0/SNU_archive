//---------------------------------------------------------------
//
//  4190.308 Computer Architecture (Fall 2020)
//
//  Project #1: Compressing Data with Huffman Coding
//
//  September 9, 2020
//
//  Injae Kang (abcinje@snu.ac.kr)
//  Sunmin Jeong (sunnyday0208@snu.ac.kr)
//  Systems Software & Architecture Laboratory
//  Dept. of Computer Science and Engineering
//  Seoul National University
//
//---------------------------------------------------------------

/* TODO: Implement this function */
int encode(const char *inp, int inbytes, char *outp, int outbytes)
{
    if(inbytes == 0 ) return 0;

    //--------input---------//
    char input[inbytes];

    for(int i = 0; i < inbytes; i++) {
        input[i] = *(inp+i);
    }

    //--------count----------//
    struct pair{
        int x;
        int rank;
        int change;
        int cnt;
        int move_bit;
    };

    struct pair count[16] = {};
    for(int i = 0; i < 16; i++) {
        count[i].x = i;
    }
    for(int i = 0; i < inbytes; i++) {
        int n = input[i] % 16;
        int m = (input[i] >> 4) % 16;
        if(n < 0) n += 16;
        if(m < 0) m += 16;
        count[n].cnt++; count[m].cnt++;
    }

    //-----insertion sort (stable)-----//
    //0 to 7
    for(int i = 1; i < 16; i++) {
        for(int j = i; j > 0; j--) {
            if(count[j - 1].cnt < count[j].cnt) {
                struct pair t = count[j];
                count[j] = count[j - 1];
                count[j - 1] = t;
            }
        }
    }
    //8 to 15
    for(int i = 9; i < 16; i++) {
        for(int j = i; j > 8; j--) {
            if(count[j - 1].x > count[j].x) {
                struct pair t = count[j];
                count[j] = count[j - 1];
                count[j - 1] = t;
            }
        }
    }

    int sumofbits = 4;
    for(int i = 0; i < 16; i++) {
        count[i].rank = i;
        if(i < 4) {
            count[i].change = i;
            count[i].move_bit = 3;
            sumofbits += 3 * count[i].cnt;
        } else if(i < 8) {
            count[i].change = i + 4;
            count[i].move_bit = 4;
            sumofbits += 4 * count[i].cnt;
        } else {
            count[i].change = i + 16;
            count[i].move_bit = 5;
            sumofbits += 5 * count[i].cnt;
        }
    }

    //----------rank header---------//
    char A[4] = {};
    for(int i = 0; i < 4; i++) {
        A[i] = (count[2 * i].x << 4) + count[2 * i + 1].x;
    }

    //---------re-sort-------------//
    for(int i = 0; i < 16; i++) {
        for(int j = i; j > 0; j--) {
            if(count[j - 1].x > count[j].x) {
                struct pair t = count[j];
                count[j] = count[j - 1];
                count[j - 1] = t;
            }
        }
    }

    //---------encode------------//
    char D[20000] = {};
    D[0] = (8 - (sumofbits % 8));
    if(D[0] == 8) D[0] = 0;
    int index = 0;
    int bit = 4;
    for(int i = 0; i < inbytes; i++) {
        int n = input[i] % 16;
        int m = (input[i] >> 4) % 16;
        if(n < 0) n += 16;
        if(m < 0) m += 16;
        for(int j = 0; j < 2; j++) {
            if (bit + count[m].move_bit < 8) {
                D[index] = (D[index] << count[m].move_bit) + count[m].change;
                bit += count[m].move_bit;
            } else {
                D[index] = (D[index] << (8 - bit)) + (count[m].change >> (count[m].move_bit - 8 + bit));
                index++;
                D[index] = (count[m].change << (16 - count[m].move_bit - bit)) >> (16 - count[m].move_bit - bit);
                bit = count[m].move_bit - 8 + bit;
            }
            m = n;
        }
    }
    if(bit == 0) index--;
    else D[index] = D[index] << (8 - bit);
    //--------rank table---------//

    if(5 + index > outbytes) return -1;

    //--------output---------//
    for(int i = 0; i < 5 + index; i++) {
        if(i < 4) *(outp+i) = A[i];
        else *(outp+i) = D[i-4];
    }

	return 5 + index;
}
