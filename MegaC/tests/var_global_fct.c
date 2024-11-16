int x;

int f(int y) { return x + 5 * y; }

int main() {
  x = 20;
  print_int(f(0));
  x = 10;
  print_int(f(1));
  return 0;
}
