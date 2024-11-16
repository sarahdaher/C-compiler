int main() {
  if (1)
    print_int(1);
  else
    print_int(2);

  if (0)
    print_int(3);
  else
    print_int(4);

  if (1) {
    print_int(5);
  } else
    print_int(6);

  if (0)
    print_int(7);
  else {
    print_int(8);
  }

  if (1) {
    print_int(9);
  } else {
    print_int(10);
  }

  int x = 12;

  if (x) {
    print_int(-x + 9);

    x = 45;
    int x = 0;

    if (x) {
      print_int(x);
    } else {
      print_int(x + 120);

      if (x + 18) {
        print_int(88);
      }
    }
  } else {
    print_int(99);
  }

  print_int(x);

  return 0;
}
