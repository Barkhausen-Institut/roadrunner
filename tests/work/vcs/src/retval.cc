#include "vpi_user.h"
#include <stdio.h>

extern "C" void registerCalls(void);

typedef void (voidfn)(void);
typedef PLI_INT32 (vpicall)(PLI_BYTE8 *);

vpicall printSuccess;

void registerCall(vpicall *call, const char *name)
{
  s_vpi_systf_data task;
  task.type = vpiSysTask;
  task.tfname = reinterpret_cast<PLI_BYTE8*>(const_cast<char*>(name));
  task.calltf = call;
  task.compiletf = 0;
  vpi_register_systf(&task);
}

PLI_INT32 printSuccess(PLI_BYTE8 *) {
    printf("--==--==-- RoadRunner Test Result (0) --==--==--\n");
    return 0;
}

void registerCalls(void) {
    registerCall(printSuccess, "$VPISuccess");
}

voidfn * vlog_startup_routines[] = {
    registerCalls,
    0
};

