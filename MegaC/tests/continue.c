int main() {
  int x = 10;

  while (x > 5) {
    x = x - 1;

    if (x == 6) {
      print_int(-x);
      continue;
    }

    int y = 0;

    while (y < 4) {
      if (y == 2) {
        break;
      }

      print_int(y);
      y = y + 1;
    }

    print_int(x);
  }

  return 0;
}
