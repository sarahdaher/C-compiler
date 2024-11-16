int main() {
  print_int(0 && 0);
  print_int(1 && 0);
  print_int(0 && 1);
  print_int(1 && 1);

  print_int(42 && 28);
  print_int(42 && 0);
  print_int(0 && 42);
  print_int(-28 && 42);
  print_int(0 && -42);

  print_int(46 && -15 && -151 && 75 && 15);
  print_int(46 && 0 && -151 && 75 && 15);
  print_int(46 && -15 && -151 && 75 && 0);

  return 0;
}
