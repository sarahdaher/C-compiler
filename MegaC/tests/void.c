void f(int a) { a = a + 1; }

void g(int a) {
  if (a % 2 == 0) {
    print_int(a + 1);
    return;
  }

  print_int(-a);
}

int main() {
  int x = 0;
  f(x);
  print_int(x);

  g(0);
  g(1);
  g(2);
  g(3);

  return 0;
}
