int f(int x) {
  print_int(-10 + x);
  return x * 2;
}

int main() {
  print_int(f(13));
  print_int(f(-42));
  f(45);

  return 0;
}
