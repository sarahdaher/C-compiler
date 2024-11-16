int x;
int y;
int z;

int main() {
  x = 20;
  y = 30;
  print_int(x);
  print_int(y);
  z = x;
  print_int(z);
  x = z + y;
  print_int(x);

  return 0;
}
