#include <iostream>
#include <vector>
using std::swap;
using std::vector;

/* using partition in ch04 */
int partition(vector<int>& a,int p,int r) {
  int piv = a[r];
  int i=p-1;
  for(int j=p;j<r;j++) {
    if(a[j]<=piv) {
      i++;
      swap(a[i],a[j]);
    }
  }
  swap(a[i+1],a[r]);
  return i+1;
}

/* */
int select(vector<int>& a,int p,int r,int i) {
  if(p==r) return a[p];
  int q = partition(a,p,r);
  int k = q-p+1;
  if(i==k) return a[q];
  if(i<k) return select(a,p,q-1,i);
  return select(a,q+1,r,i-k);
}

int main(int argc, char **argv) {
  FILE *in = fopen(argv[1], "r");
  FILE *out = fopen(argv[2], "r");
  
  vector<int> a;
  a.push_back(0); //for starting index 1
  int n,m,t;
  fscanf(in,"%d %d",&n,&m);
  for(int i=1;i<=n;i++) {
    fscanf(in, "%d", &t);
    a.push_back(t);
  }

  int output;
  fscanf(out, "%d", &output);
  if(select(a,1,n,m)==output) std::cout<<1<<"\n";
  else std::cout<<0<<"\n";

  fclose(in);
  fclose(out);

  return 0;
}
