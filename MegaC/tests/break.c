int main() {
  int x = 10;

  while (x > 0) {
    if (x == 6) {
      break;
    }

    int y = 0;

    while (y < 4) {
      if (y + x - 10 == 2) {
        break;
      }

      print_int(y);
      y = y + 1;
    }

    print_int(x);
    x = x - 1;
  }

  return 0;
}
