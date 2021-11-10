#include <stdio.h>
int main(){
    int x = 0;
    for( int i = 0 ; i < 5; i++){
        x += i*i;
    }
    printf("%lu",x);
    return 0;
}