int main() {
  print_int(!0);
  print_int(!-0);
  print_int(!1);
  print_int(!42);
  print_int(!-42);
  print_int(!!0);
  print_int(!!42);
  print_int(!!!!!!!0);
  print_int(!!!!!!!-42);

  int a = !(0 == 1);
  print_int(a);
  int b = !(1 == 1);
  print_int(b);

  return 0;
}
