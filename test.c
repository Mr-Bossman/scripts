#include <stdio.h>
#include "foo.h"

int main(){
	foo(1);
	return 0;
}

void foo(int a){
	printf("%s %d\n",PENUM(a));
}
