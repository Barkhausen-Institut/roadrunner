#include <stdio.h>
#include <svdpi.h>
#include "msg.h"


extern "C" void DPIGreeting();
extern "C" void DPISuccess();

void DPIGreeting() {
    printf(HELLO_MESSAGE);
    return;
}

void DPISuccess() {
    printf(SUCCESS_MESSAGE);
    return;
}

