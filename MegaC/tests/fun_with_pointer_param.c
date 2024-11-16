int f(int *a, int b) { return *a + b; }

int main() {
  int b = 2;
  int c = 3;
  print_int(f(&b, c));
  b = 4;
  int *a = &b;
  print_int(*a);
  int d = 7;
  *a = d;
  print_int(*a);
  print_int(f(a, b));
  return 0;
}
