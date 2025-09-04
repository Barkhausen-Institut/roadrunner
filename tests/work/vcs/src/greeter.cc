#include "vpi_user.h"
#include <stdio.h>

extern "C" void registerCalls(void);

typedef void (voidfn)(void);
typedef PLI_INT32 (vpicall)(PLI_BYTE8 *);

vpicall printGreeting;

void registerCall(vpicall *call, const char *name)
{
  s_vpi_systf_data task;
  task.type = vpiSysTask;
  task.tfname = reinterpret_cast<PLI_BYTE8*>(const_cast<char*>(name));
  task.calltf = call;
  task.compiletf = 0;
  vpi_register_systf(&task);
}

PLI_INT32 printGreeting(PLI_BYTE8 *) {
    printf("Hello, World!\n");
    return 0;
}

void registerCalls(void) {
    registerCall(printGreeting, "$VPIGreeting");
}

voidfn * vlog_startup_routines[] = {
    registerCalls,
    0
};

