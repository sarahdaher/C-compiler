int f(int *a) { return *a + 3; }

int set_value(int ***a, int b) {
  ***a = b;
  return 0;
}

int main() {
  int x = 5;
  int *y = &x;
  int **z = &y;
  print_int(f(*z));
  int h = set_value(&z, 20);
  print_int(x);

  int a1 = 42;
  int *a2 = &a1;
  int **a3 = &a2;
  int ***a4 = &a3;
  int ****a5 = &a4;
  int *****a6 = &a5;
  int ******a7 = &a6;
  print_int(******a7);
  ***a4 = 89;
  print_int(******a7);
  int b1 = -6;
  int *b2 = &b1;
  int **b3 = &b2;
  int ***b4 = &b3;
  a4 = b4;
  print_int(******a7);

  return 0;
}
