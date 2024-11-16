int f() { return 5; }

int main() {
  print_int(f());
  f();
  print_int(f());

  return 0;
}
