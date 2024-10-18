#include <cstdint>
#include <iostream>
#include <vector>
using namespace std;

uint64_t area(vector<pair<int, int>> &points) {
  // This code has signed overflows. :)
  // Please fix this so it correctly evaluates area..!
  uint64_t total = 0;
  int64_t val[105] = {};
  int64_t remain = 0;
  size_t n = points.size();

  for (unsigned i = 0; i < n; i++) {
    unsigned j = (i + 1) % n;
    int64_t x_i = points[i].first;
    int64_t y_i = points[i].second;
    int64_t x_j = points[j].first;
    int64_t y_j = points[j].second;
    val[i] = (x_i * (y_j - y_i) - y_i * (x_j - x_i));
    remain += val[i] % 2;
    val[i] /= 2;
  }

  // simple insertion sort
  for(int i=1;i<n;i++) {
    for(int j = i; j > 0 && val[j-1] > val[j]; j--) {
      swap(val[j-1],val[j]);
    }
  }

  int r = n-1;
  for(int i = 0; i <= r; i++) {
    while(val[i] < 0) {
      val[i] += val[r--];
    }
    total += val[i];
  }

  total += remain / 2;
  return total;
}