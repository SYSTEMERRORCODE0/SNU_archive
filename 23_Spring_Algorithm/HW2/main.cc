#include <iostream>
#include <vector>
#include <algorithm>
#include <chrono> // For measuring time
using std::vector;
using std::sort;
using std::greater;

#define MAX_VERTICES 5003

/* For measuring time */
//using std::chrono::high_resolution_clock;
//using std::chrono::microseconds;
//using std::chrono::duration_cast;

/* for sorting vertices with f[v] */
typedef std::pair<int,int> P;

/* Vertices & Edges */
int n,m;

/* Finish time */
int f[MAX_VERTICES];

/* Visited */
int visited[MAX_VERTICES];

/* time */
int t = 0;

/* SCC index */
int sccIdx = 0;

/* XOR of Strongly Connected Component */
int scc[MAX_VERTICES];

/* Vector(Array) of pair<int,int> for sorting by f[v] */
vector<P> vec;

////////////////* SCC of Adjacent Matrix *////////////////

int mat[MAX_VERTICES][MAX_VERTICES]; // Adjacency Matrix
int rmat[MAX_VERTICES][MAX_VERTICES]; // Reverse Adjacency Matrix

/* aDFS of Adjacent Matrix */
void adfsMatrix(int v) {
  visited[v] = 1;
  for(int i=1;i<=n;i++) {
    if(mat[v][i] == 1 && visited[i] == 0) adfsMatrix(i);
  }
  f[v] = ++t;
} 

/* DFS of Adjacent Matrix */
void dfsMatrix() {
  for(int i=1;i<=n;i++) {
    if(visited[i] == 0) adfsMatrix(i);
  }
}

/* aDFS in G^R of Adjacent Matrix */
void radfsMatrix(int v) {
  visited[v] = 1;
  for(int i=1;i<=n;i++) {
    if(rmat[v][i] == 1 && visited[i] == 0) {
      scc[sccIdx] ^= i;
      radfsMatrix(i);
    }
  }
} 

/* DFS in G^R of Adjacent Matrix */
void rdfsMatrix() {
  /* pair<int,int> (f[v], vectex) for sorting by f[v] */
  for(int i=1;i<=n;i++) {
    visited[i] = 0; // reset visited
    vec.push_back(P(f[i],i));
  }
  sort(vec.begin(), vec.end(), greater<P>());

  for(P i : vec) {
    if(visited[i.second] == 0) {
      scc[sccIdx] = i.second;
      radfsMatrix(i.second);
      sccIdx++;
    }
  }
}

void sccMatrix() {
  dfsMatrix();
  //transpose of Graph is already ready in input
  rdfsMatrix();
}

/////////////////////////////////////////////////////////

////////////////* SCC of Adjacent List *////////////////

/* Adjacency Linked list & Functions */
struct Node{
  int data;
  Node *next = nullptr;
};

Node *list = new Node[MAX_VERTICES];
Node *rlist = new Node[MAX_VERTICES];

void insert(Node *node, int data) {
  while(node->next != nullptr) {
    node = node->next;
  }
  Node *new_node = new Node();
  new_node->data = data;
  new_node->next = nullptr;
  node->next = new_node;
}

/* aDFS of Adjacent List */
void adfsList(int v) {
  visited[v] = 1;
  Node *node = &list[v];
  while(node->next != nullptr) {
    node = node->next;
    if(visited[node->data] == 0) {
      adfsList(node->data);
    }
  }
  f[v] = ++t;
} 

/* DFS of Adjacent List */
void dfsList() {
  for(int i=1;i<=n;i++) {
    if(visited[i] == 0) adfsList(i);
  }
}

/* aDFS in G^R of Adjacent List */
void radfsList(int v) {
  visited[v] = 1;
  Node *node = &rlist[v];
  while(node->next != nullptr) {
    node = node->next;
    if(visited[node->data] == 0) {
      scc[sccIdx] ^= node->data;
      radfsList(node->data);
    }
  }
} 

/* DFS in G^R of Adjacent List */
void rdfsList() {
  /* pair<int,int> (f[v], vectex) for sorting by f[v] */
  for(int i=1;i<=n;i++) {
    visited[i] = 0; // reset visited
    vec.push_back(P(f[i],i));
  }
  sort(vec.begin(), vec.end(), greater<P>());

  for(P i : vec) {
    if(visited[i.second] == 0) {
      scc[sccIdx] = i.second;
      radfsList(i.second);
      sccIdx++;
    }
  }
}

void sccList() {
  dfsList();
  //transpose of Graph is already ready in input
  rdfsList();
}

/////////////////////////////////////////////////////////

////////////////* SCC of Adjacent Array *////////////////

vector<int> arr[MAX_VERTICES]; // Adjacency array : vector is dynamic array
vector<int> rarr[MAX_VERTICES]; // Reverse Adjacency array : vector is dynamic array

/* aDFS of Adjacent Array */
void adfsArray(int v) {
  visited[v] = 1;
  for(int i:arr[v]) {
    if(visited[i] == 0) adfsArray(i);
  }
  f[v] = ++t;
} 

/* DFS of Adjacent Array */
void dfsArray() {
  for(int i=1;i<=n;i++) {
    if(visited[i] == 0) adfsArray(i);
  }
}

/* aDFS in G^R of Adjacent Array */
void radfsArray(int v) {
  visited[v] = 1;
  for(int i:rarr[v]) {
    if(visited[i] == 0) {
      scc[sccIdx] ^= i;
      radfsArray(i);
    }
  }
} 

/* DFS in G^R of Adjacent Array */
void rdfsArray() {
  /* pair<int,int> (f[v], vectex) for sorting by f[v] */
  for(int i=1;i<=n;i++) {
    visited[i] = 0; // reset visited
    vec.push_back(P(f[i],i));
  }
  sort(vec.begin(), vec.end(), greater<P>());

  for(P i : vec) {
    if(visited[i.second] == 0) {
      scc[sccIdx] = i.second;
      radfsArray(i.second);
      sccIdx++;
    }
  }
}

void sccArray() {
  dfsArray();
  //transpose of Graph is already ready in input
  rdfsArray();
}

/////////////////////////////////////////////////////////

int main(int argc, char **argv) {
  int version = int(*argv[1])-'0';
  FILE *in = fopen(argv[2], "r");
  FILE *out = fopen(argv[3], "w");

  /* input n, m */
  fscanf(in,"%d", &n);
  fscanf(in,"%d", &m);

  if(version == 1) {
    /* input Adjacency Matrix */
    for(int i=0;i<m;i++) {
      int x,y;
      fscanf(in, "%d %d", &x, &y);
      mat[x][y] = 1;
      rmat[y][x] = 1;
    }
  } else if(version == 2) {
    /* input Adjacency List */
    for(int i=0;i<m;i++) {
      int x,y;
      fscanf(in, "%d %d", &x, &y);
      insert(&list[x], y);
      insert(&rlist[y], x);
    }
  } else {
    /* input Adjacency Array */
    for(int i=0;i<m;i++) {
      int x,y;
      fscanf(in, "%d %d", &x, &y);
      arr[x].push_back(y);
      rarr[y].push_back(x);
    }
  }

  /* measure the time of SCC */
  //auto start = high_resolution_clock::now();

  if(version == 1) {
    /* SCC Adjacency Matrix */
    sccMatrix();
  } else if(version == 2) {
    /* SCC Adjacency List */
    sccList();
  } else {
    /* SCC Adjacency Array */
    sccArray();
  }

  /* convert the time into integer */
  //auto end = high_resolution_clock::now()-start;
  //long long micros = duration_cast<microseconds>(end).count();
  //std::cout<<"Input size : n = "<<n<<", m = "<<m<<", microseconds : "<<micros<<"us\n";

  /* sort and print */
  sort(scc, scc+sccIdx);
  fprintf(out,"%d\n",sccIdx);
  for(int i=0;i<sccIdx;i++) {
    if(i == sccIdx - 1) fprintf(out,"%d",scc[i]);
    else fprintf(out,"%d ",scc[i]);
  }
  fprintf(out,"\n");

  fclose(in);
  fclose(out);

  return 0;
}
