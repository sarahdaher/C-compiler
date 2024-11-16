int main() {
  if (1)
    print_int(1);

  if (0)
    print_int(2);

  if (2) {
    print_int(3);
    print_int(4);
  }

  if (0) {
    print_int(5);
    print_int(6);
  }

  int x = 12;

  if (x) {
    x = 0;
    if (x) {
      int x = 42;
      print_int(x);
    }
    int x = -10;
    if (x) {
      print_int(x * 10);
    }
  }

  return 0;
}
