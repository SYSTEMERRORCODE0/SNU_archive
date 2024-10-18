//---------------------------------------------------------------
//
//  4190.308 Computer Architecture (Fall 2020)
//
//  Project #2: FP12 (12-bit floating point) Representation
//
//  September 28, 2020
//
//  Injae Kang (abcinje@snu.ac.kr)
//  Sunmin Jeong (sunnyday0208@snu.ac.kr)
//  Systems Software & Architecture Laboratory
//  Dept. of Computer Science and Engineering
//  Seoul National University
//
//---------------------------------------------------------------

#include "pa2.h"

/* Convert 32-bit signed integer to 12-bit floating point */
fp12 int_fp12(int n)
{
	/* TODO */
	if(n==0) return 0;
	if(n==0x80000000) return 0xFFC0;
	int S = n<0;
	int m = n>0?n:-n;
	int E = 0;
	unsigned int F = m & 0x7FFFFFFF;
	while(m>0) {
        m = m >> 1;
        E++;
	}
    if(E<6) F = F << (6-E);
    else {
        F = F << (31-E);
        if((F & 0x03000000) == 0x03000000 || (F & 0x01FFFFFF) > 0x01000000) F = F + 0x02000000;
        F = F >> 25;
    }
    if(F>=64) {
        F = F >> 1;
        E++;
    }
	fp12 fp = 0xF800 * S + ((E+30)<<5) + (F & 0x0000001F);

	return fp;
}

/* Convert 12-bit floating point to 32-bit signed integer */
int fp12_int(fp12 x)
{
	/* TODO */
	int S = (x&0x8000)>>15;
    int E = (x & 0x07E0)>>5;
	if(E >= 0x003E) return 0x80000000;
    int F = ((x & 0x001F) + 0x0020);
    if(E<31) return 0;
    else if(E<36) F = F >> (36-E);
    else F = F<<(E-36);
	return F * (-1) * (S*2-1);
}

/* Convert 32-bit single-precision floating point to 12-bit floating point */
fp12 float_fp12(float f)
{
    /* TODO */
    int* fp = &f;
    int E = ((*fp & 0x7F800000)>>23)-127;
    if(E<-36) return 0xF800 * (*fp >= 0x80000000); //+0 or -0
    if(E==128 && (*fp & 0x007FFFFF)) return 0xF800 * (*fp >= 0x80000000) + 0x07E1;
    if(E>31) return 0xF800 * (*fp >= 0x80000000) + 0x07E0;
    int F = *fp & 0x007FFFFF;
    if(E<-30) {
        if(E == -36) {
            if(F) {
                F = 0x00000001;
            } else return 0xF800 * (*fp >= 0x80000000); //+0 or -0;
        } else {
            F = (F + 0x00800000)<<(E+35);
            if ((F & 0x007FFFFF) <= 0x00400000 && (F & 0x00C00000) != 0x00C00000) F = F >> 23;
            else F = (F >> 23) + 1;
        }
        return 0xF800 * (*fp >= 0x80000000) + (F & 0x0000001F);
    }
    else {
        if((F&0x0003FFFF)<=0x00020000 && (F&0x00060000) != 0x00060000) {
            F = F >> 18;
        } else {
            F = (F >> 18) + 1;
            if(F >= 0x00000020) {
                if (E > 30) return 0xF800 * (*fp >= 0x80000000) + 0x07E0;
                E++;
            }
        }
    }
    return 0xF800 * (*fp >= 0x80000000) + ((E+31) << 5) + (F & 0x0000001F);
}

/* Convert 12-bit floating point to 32-bit single-precision floating point */
float fp12_float(fp12 x)
{
	/* TODO */
	int n = 0;
	float* fp = &n;
	int S = (x & 0x8000) >> 15;
    int E = ((x & 0x07E0)>>5)-31;
    int F = x & 0x001F;
    if(E == 32) {
        n = 0x80000000 * S + 0x7F800000 + F;
        return *fp;
    }
    if(E == -31) {
        if(F == 0) {
            n = 0x80000000 * S;
            return *fp;
        }
        while(F < 32) {
            E--;
            F = F<<1;
        }
        F-=32;
        E++;
    }
    n = 0x80000000 * S + ((E+127)<<23) + (F<<18);
	return *fp;
}
