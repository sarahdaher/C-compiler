int fib1(int n) {
  if (n <= 1)
    return n;
  return fib1(n - 1) + fib1(n - 2);
}

void fib2(int n, int *res) {
  if (n == 0) {
    *res = 0;
    return;
  }

  if (n == 1) {
    *res = 1;
    return;
  }

  if (n > 1) {
    int y;
    int z;
    fib2(n - 1, &y);
    fib2(n - 2, &z);
    *res = y + z;
  }
}

int main() {
  print_int(fib1(0));
  print_int(fib1(1));
  print_int(fib1(2));
  print_int(fib1(3));
  print_int(fib1(10));
  print_int(fib1(30));

  int res;

  fib2(0, &res);
  print_int(res);

  fib2(1, &res);
  print_int(res);

  fib2(2, &res);
  print_int(res);

  fib2(3, &res);
  print_int(res);

  fib2(10, &res);
  print_int(res);

  fib2(30, &res);
  print_int(res);

  return 0;
}
