int main() {
  int a = 10;

  while (a) {
    a = a - 1;

    {
      int y = 42;
      if (a % 2 == 0) {
        continue;
      }
      print_int(a);
      print_int(y);
    }
  }

  int x = 12;
  print_int(x);
  print_int(a);

  return 0;
}
