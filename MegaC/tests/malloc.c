int main() {
  int *a = malloc(sizeof(int));
  *a = 42;
  print_int(*a);
  return 0;
}
