#include <iostream>
#include <random>
#include <vector>
//#include <chrono> // For measuring time
using std::swap;
using std::vector;
/* For measuring time */
//using std::chrono::high_resolution_clock;
//using std::chrono::microseconds;
//using std::chrono::duration_cast;

/* using advanced random in c++ */
std::random_device rd;
std::mt19937 gen(rd());

/* partition for randomSelect */
int randomPartition(vector<int>& a,int p,int r) {
  /* select the random pivot with uniform distribution */
  std::uniform_int_distribution<int> dis(p,r);
  int piv_idx = dis(gen);

  int piv = a[piv_idx];
  swap(a[piv_idx],a[r]);
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

int randomPivotSelect(vector<int>& a,int p,int r,int i) {
  if(p==r) return a[p];
  int q = randomPartition(a,p,r);
  int k = q-p+1;
  if(i==k) return a[q];
  if(i<k) return randomPivotSelect(a,p,q-1,i);
  return randomPivotSelect(a,q+1,r,i-k);
}

/* using insertion sort in ch02 */
void insertionSort(vector<int>& a,int p,int r) {
  for(int i=p+1;i<=r;i++) {
    int k = a[i];
    int j = i-1;
    while(j>=p&&a[j]>k) {
      a[j+1] = a[j];
      j--;
    }
    a[j+1] = k;
  }
}

/* partition for determSelect */
int determPartition(vector<int>& a,int p,int r,int piv) {
  /* almost same with normal partition algorithm */
  int i=p-1;
  int piv_idx_find = 0;
  for(int j=p;j<r;j++) {
    if(a[j]<=piv) {
      if(a[j]==piv&&piv_idx_find==0) {  //find pivot index and swap with a[r]
        swap(a[j],a[r]);
        j--;
        piv_idx_find = 1;
        continue;
      }
      i++;
      swap(a[i],a[j]);
    }
  }
  swap(a[i+1],a[r]);
  return i+1;
}

int determSelect(vector<int>& a,int p,int r,int i) {
  /* size <= 5, then */
  if(r-p<=4) {
    insertionSort(a,p,r);
    return a[p+i-1];
  }
  
  vector<int> m;  //medians
  m.push_back(0); //for starting index 1

  /* divide into upto 5 elements */
  for(int j=p;j<=r;j+=5) {
    int end = std::min(r,j+4);
    insertionSort(a,j,end);
    m.push_back(a[j+(end-j)/2]);
  }
  
  int mid = determSelect(m,1,m.size(),(m.size()+1)/2); // get median by resursion

  int q = determPartition(a,p,r,mid);
  int k = q-p+1;

  if(i==k) return a[q];
  if(i<k) return determSelect(a,p,q-1,i);
  return determSelect(a,q+1,r,i-k);
}

int main(int argc, char **argv) {
  int version = int(*argv[1])-'0';
  FILE *in = fopen(argv[2], "r");
  FILE *out = fopen(argv[3], "w");
  
  vector<int> a;
  a.push_back(0); //for starting index 1

  /* input */
  int n,m,t;
  fscanf(in,"%d %d",&n,&m);
  for(int i=1;i<=n;i++) {
    fscanf(in, "%d", &t);
    a.push_back(t);
  }

  /* measure the time of selection */
  //auto start = high_resolution_clock::now();

  if(version==1) fprintf(out, "%d", randomPivotSelect(a,1,n,m));
  else fprintf(out, "%d", determSelect(a,1,n,m));

  /* convert the time into integer */
  //auto end = high_resolution_clock::now()-start;
  //long long micros = duration_cast<microseconds>(end).count();
  //std::cout<<"Input size : "<<n<<", microseconds : "<<micros<<"us\n";

  fclose(in);
  fclose(out);

  return 0;
}
