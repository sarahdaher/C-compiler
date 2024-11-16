int f(int n) { return n * n; }

int main() {
  int n = 10;
  int r = n * f(n - 1);
  print_int(r);
  print_int(f(f(3) - 5) * 3);
  return 0;
}
