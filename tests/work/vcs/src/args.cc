#include "vpi_user.h"
#include <stdio.h>
#include <string>

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

PLI_INT32 passArgs(PLI_BYTE8 *) {
    vpiHandle vpiSys, vpiArgs, vpiArg;
    t_vpi_value vpiValue;

    //init VPI system
    vpiSys = vpi_handle(vpiSysTfCall, NULL);
    vpiArgs = vpi_iterate(vpiArgument, vpiSys);

    //get arg 0: string
    vpiArg = vpi_scan(vpiArgs);
    vpiValue.format = vpiStringVal;
    vpi_get_value(vpiArg, &vpiValue);
    std::string msg(vpiValue.value.str); //do we have to copy?
    printf("Got arg 0: %s\n", msg.c_str());

    //get arg 1: integer
    int num;
    vpiArg = vpi_scan(vpiArgs);
    vpiValue.format = vpiIntVal;
    vpi_get_value(vpiArg, &vpiValue);
    num = vpiValue.value.integer;
    printf("Got arg 1: %d\n", num);

    //set arg 2: msgOut
    vpiArg = vpi_scan(vpiArgs);
    vpiValue.format = vpiStringVal;
    vpiValue.value.str = "burbel burbel"; //(PLI_BYTE8*)msg.c_str();
    vpi_put_value(vpiArg, &vpiValue, NULL, vpiNoDelay);
    printf("Set arg 2: %s\n", "burbel burbel"); //msg.c_str());

    //set arg 4: numOut
    vpiArg = vpi_scan(vpiArgs);
    vpiValue.format = vpiIntVal;
    vpiValue.value.integer = 37;
    vpi_put_value(vpiArg, &vpiValue, NULL, vpiNoDelay);
    printf("Set arg 4: %d\n", 37); //num);

    vpi_free_object(vpiArgs);
    return 0;
}

void registerCalls(void) {
    registerCall(passArgs, "$VPIArgs");
    printf("Registered VPIArgs\n");
}
