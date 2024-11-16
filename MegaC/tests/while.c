int main() {
  int x = 3;

  while (x > 0) {
    int y = 0;

    while (y < 4) {
      print_int(2);
      y = y + 1;
    }

    print_int(1);
    x = x - 1;
  }

  return 0;
}
