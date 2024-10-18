#include <iostream>
#include <vector>
//#include <chrono> // For measuring time

using namespace std;

/* For measuring time */
//using std::chrono::high_resolution_clock;
//using std::chrono::microseconds;
//using std::chrono::duration_cast;

/* range of possible column of area (possible row if column) */
/* same as H, A but I made this struct for confusion*/
struct R{
  int s,e; // assert s<=e
};

/* holes */
struct H{
  int x,y;
};

/* areas */
struct A{
  int r,i,n; // r = row, i = index of vec<R>, n = now pointing column
};

vector<R> row[15], col[15], left_diag[30], right_diag[30]; // "-" "|" "\" "/"
vector<int> row_c[15], col_c[15], left_diag_c[30], right_diag_c[30]; // check vacant (0) occupied (column)
int p[15][15];
vector<A> areas;

int possible(int x, int y, int n) {
  for(int i=0;i<col[y].size();i++) if(col[y][i].s<=x && col[y][i].e>=x && col_c[y][i] > 0) return 0;
  for(int i=0;i<left_diag[n+x-y].size();i++) if(left_diag[n+x-y][i].s<=y && left_diag[n+x-y][i].e>=y && left_diag_c[n+x-y][i] > 0) return 0;
  for(int i=0;i<right_diag[x+y-1].size();i++) if(right_diag[x+y-1][i].s<=y && right_diag[x+y-1][i].e>=y && right_diag_c[x+y-1][i] > 0) return 0;
  return 1;
}

int recursive_backtracking(int n, int area_i, int queens) {
  if(queens == n) return 1;
  if(n-queens > areas.size()-area_i) return 0;

  A area = areas[area_i];
  R ro = row[area.r][area.i];
  int x = area.r;
  int y, sum=0;

  for(y=ro.s-1;y<=ro.e;y++) {
    if(y < ro.s) {
      // don't insert queen in this area and check next area
      sum += recursive_backtracking(n, area_i+1, queens);
    } else if(possible(x, y, n) == 1) {
      // if possible to put queen, put it
      row_c[x][area.i] = y;
      for(int i=0;i<col[y].size();i++) if(col[y][i].s<=x && col[y][i].e>=x) col_c[y][i]=x;
      for(int i=0;i<left_diag[n+x-y].size();i++) if(left_diag[n+x-y][i].s<=y && left_diag[n+x-y][i].e>=y) left_diag_c[n+x-y][i]=y;
      for(int i=0;i<right_diag[x+y-1].size();i++) if(right_diag[x+y-1][i].s<=y && right_diag[x+y-1][i].e>=y) right_diag_c[x+y-1][i]=y;
      sum += recursive_backtracking(n, area_i+1, queens+1);
      // delete after recursion
      row_c[x][area.i] = 0;
      for(int i=0;i<col[y].size();i++) if(col[y][i].s<=x && col[y][i].e>=x) col_c[y][i]=0;
      for(int i=0;i<left_diag[n+x-y].size();i++) if(left_diag[n+x-y][i].s<=y && left_diag[n+x-y][i].e>=y) left_diag_c[n+x-y][i]=0;
      for(int i=0;i<right_diag[x+y-1].size();i++) if(right_diag[x+y-1][i].s<=y && right_diag[x+y-1][i].e>=y) right_diag_c[x+y-1][i]=0;
    }
  }

  return sum;
}

int iterative_backtracking(int n) {
  int queens = 0, area_i = 0, sum = 0;
  
  while(area_i >= 0) {

    // if there is neccesary areas nums for queens, backtrack
    if(n-queens > areas.size()-area_i) {
      area_i--;
      continue;
    }

    A area = areas[area_i];
    R ro = row[area.r][area.i];
    int x = area.r;
    // reset the start idx of next area
    if(area_i + 1 < areas.size()) areas[area_i+1].n = row[areas[area_i+1].r][areas[area_i+1].i].s-1;
    int y;

    // if there was a queen in the area, erase it
    if(row_c[x][area.i] > 0) {
      y = row_c[x][area.i];
      row_c[x][area.i] = 0;
      for(int i=0;i<col[y].size();i++) if(col[y][i].s<=x && col[y][i].e>=x) col_c[y][i]=0;
      for(int i=0;i<left_diag[n+x-y].size();i++) if(left_diag[n+x-y][i].s<=y && left_diag[n+x-y][i].e>=y) left_diag_c[n+x-y][i]=0;
      for(int i=0;i<right_diag[x+y-1].size();i++) if(right_diag[x+y-1][i].s<=y && right_diag[x+y-1][i].e>=y) right_diag_c[x+y-1][i]=0;
      queens--;
    }
    
    // if already found all the index of the area, backtrack
    if(area.n > ro.e) {
      area_i--;
      continue;
    }

    for(y=area.n;y<=ro.e;y++) {
      if(y < ro.s) {  // not put queen in this area and go to next area
        break;
      } else if(possible(x, y, n) == 1) {
        // if possible to put queen, put it
        row_c[x][area.i] = y;
        for(int i=0;i<col[y].size();i++) if(col[y][i].s<=x && col[y][i].e>=x) col_c[y][i]=x;
        for(int i=0;i<left_diag[n+x-y].size();i++) if(left_diag[n+x-y][i].s<=y && left_diag[n+x-y][i].e>=y) left_diag_c[n+x-y][i]=y;
        for(int i=0;i<right_diag[x+y-1].size();i++) if(right_diag[x+y-1][i].s<=y && right_diag[x+y-1][i].e>=y) right_diag_c[x+y-1][i]=y;
        queens++;
        break;
      }
    }

    // if found all the idx in the area, backtrack
    if(y > ro.e) {
      area_i--;
      continue;
    }

    // pointing next idx and ready to go next area
    areas[area_i].n = y + 1; 
    area_i++;

    // there is a case, don't go to next area and erase last
    if(queens == n) {
      sum++;
      area_i--;
      //erase last
      row_c[x][area.i] = 0;
      for(int i=0;i<col[y].size();i++) if(col[y][i].s<=x && col[y][i].e>=x) col_c[y][i]=0;
      for(int i=0;i<left_diag[n+x-y].size();i++) if(left_diag[n+x-y][i].s<=y && left_diag[n+x-y][i].e>=y) left_diag_c[n+x-y][i]=0;
      for(int i=0;i<right_diag[x+y-1].size();i++) if(right_diag[x+y-1][i].s<=y && right_diag[x+y-1][i].e>=y) right_diag_c[x+y-1][i]=0;
      queens--;
    }
  }
  return sum;
}

void collect_area(int n) {
  // collect area
  for(int i=1;i<=n;i++) {
    // row
    int t=1;
    for(int j=1;j<=n;j++) {
      if(p[i][j]==1) {
        if(t!=j) {
          row[i].push_back(R{t,j-1});
          row_c[i].push_back(0);
        }
        t=j+1;
      }
    }
    if(t<=n) {
      row[i].push_back(R{t,n});
      row_c[i].push_back(0);
    }

    //column
    t=1;
    for(int j=1;j<=n;j++) {
      if(p[j][i]==1) {
        if(t!=j) {
          col[i].push_back(R{t,j-1});
          col_c[i].push_back(0);
        }
        t=j+1;
      }
    }
    if(t<=n) {
      col[i].push_back(R{t,n});
      col_c[i].push_back(0);
    }

    // left diagonal / upper
    t=n+1-i;
    for(int j=1;j<=i;j++) {
      if(p[j][n-i+j]==1) {
        if(t!=n-i+j) {
          left_diag[i].push_back(R{t,n-1-i+j});
          left_diag_c[i].push_back(0);
        }
        t=n+1-i+j;
      }
    }
    if(t<=n) {
      left_diag[i].push_back(R{t,n});
      left_diag_c[i].push_back(0);
    }

    // left diagonal / lower
    if(i!=n) {
      t=1;
      for(int j=1;j<=i;j++) {
        if(p[n-i+j][j]==1) {
          if(t!=j) {
            left_diag[2*n-i].push_back(R{t,j-1});
            left_diag_c[2*n-i].push_back(0);
          }
          t=j+1;
        }
      }
      if(t<=i) {
        left_diag[2*n-i].push_back(R{t,i});
        left_diag_c[2*n-i].push_back(0);
      }
    }

    // right diagonal / upper
    t=1;
    for(int j=1;j<=i;j++) {
      if(p[i-j+1][j]==1) {
        if(t!=j) {
          right_diag[i].push_back(R{t,j-1});
          right_diag_c[i].push_back(0);
        }
        t=j+1;
      }
    }
    if(t<=i) {
      right_diag[i].push_back(R{t,i});
      right_diag_c[i].push_back(0);
    }

    if(i!=n) {
      // right diagonal / lower
      t=n+1-i;
      for(int j=1;j<=i;j++) {
        if(p[n+1-j][n-i+j]==1) {
          if(t!=n-i+j) {
            right_diag[2*n-i].push_back(R{t,n-i-1+j});
            right_diag_c[2*n-i].push_back(0);
          }
          t=n+1-i+j;
        }
      }
      if(t<=n) {
        right_diag[2*n-i].push_back(R{t,n});
        right_diag_c[2*n-i].push_back(0);
      }
    }
  }
}

int main(int argc, char **argv) {

  int version = int(*argv[1])-'0';
  FILE *in = fopen(argv[2], "r");
  FILE *out = fopen(argv[3], "w");

  int n,m,r;
  vector<H> holes;
  
  fscanf(in,"%d %d",&n,&m);
  for(int i=0;i<m;i++) {
    int x,y;
    fscanf(in, "%d %d", &x, &y);
    holes.push_back(H{x,y});
    p[x][y]=1;
  }

  /* measure the time of Backtracking */
  //auto start = high_resolution_clock::now();

  collect_area(n);

  // indexing areas
  for(int i=1;i<=n;i++) {
    for(int j=0;j<row[i].size();j++) {
      areas.push_back(A{i,j,row[i][j].s-1});
    }
  }

  if(version == 1) r = iterative_backtracking(n);
  else r = recursive_backtracking(n, 0, 0);

  /* convert the time into integer */
  //auto end = high_resolution_clock::now()-start;
  //long long micros = duration_cast<microseconds>(end).count();
  //std::cout<<"Input size : n = "<<n<<", microseconds : "<<micros<<"us\n";

  fprintf(out,"%d\n",r);

  fclose(in);
  fclose(out);

  return 0;
}