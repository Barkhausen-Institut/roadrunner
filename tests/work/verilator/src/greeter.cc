#include <stdio.h>
#include <svdpi.h>

extern "C" void DPIGreeting();

void DPIGreeting() {
    printf("Hello, World!\n");
    return;
}

