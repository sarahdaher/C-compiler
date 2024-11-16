int f(int x) {
  if (!x) {
    print_int(42);
    return 1;
  }

  print_int(-x);
  return 0;
}

int main() {
  if (f(0) || f(2)) {
    print_int(-42);
  } else {
    print_int(10);
  }

  if (f(2) || f(0)) {
    print_int(-42);
  } else {
    print_int(10);
  }

  if (f(2) || f(3) || f(4) || f(0)) {
    print_int(-42);
  } else {
    print_int(10);
  }

  if (f(2) || f(3) || f(4) || f(5)) {
    print_int(-42);
  } else {
    print_int(10);
  }

  return 0;
}
