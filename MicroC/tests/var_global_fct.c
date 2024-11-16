int x;

int main(int y) {
	x = 20;
	print(f(0));
	x = 10;
	print(f(1));
	return 0;
}

int f(int y) {
	return x + 5 * y;
}
