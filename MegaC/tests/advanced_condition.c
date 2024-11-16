int f(int a) { return 1 - a; }

int main() {
  if (1 == 1 && !!!3 <= 0 || !3 > 1 && 2 > 0) {
    if (4 <= 5 && !!!!!(2 > 3)) {
      if (0) {
        print_int(4);
      } else {
        print_int(5);
      }
    }
  } else {
    print_int(6);
  }
  int a = 2;
  int b = 0;
  if (a + b < 3) {
    print_int(7);
  } else {
    print_int(8);
  }
  if (2 * a < 5 + b) {
    print_int(9);
  } else {
    print_int(10);
  }
  if (2 && 1) {
    print_int(11);
  } else {
    print_int(12);
  }
  if (f(1) || !f(0)) {
    print_int(13);
  } else {
    print_int(14);
  }

  return 0;
}
