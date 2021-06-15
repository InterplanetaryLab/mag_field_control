#define PI 3.14159

int abs(int val){return (val <=0 ) ? val*-1: val;} 
int range_limit(int val, int low, int high)
{
	if (val > high)
		val = high;
	else if (val < low)
		val = low;
	return val;
}
