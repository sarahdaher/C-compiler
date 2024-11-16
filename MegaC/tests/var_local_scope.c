int main() {
  int a = 42;
  print_int(a);

  {
    int a = 65;
    print_int(a);
    a = 89;
    print_int(a);
  }

  print_int(a);

  if (1) {
    a = 12;
  } else {
    int a = 45;
  }

  print_int(a);

  if (0) {
    a = 9;
  } else {
    int a = 1;
  }

  print_int(a);

  return 0;
}
