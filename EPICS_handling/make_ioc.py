import subprocess
import os
from utility import variables_handling

cmd = ['powershell', "echo ($env:LOCALAPPDATA + '\\Packages\\' + ($(get-appxpackage).PackageFamilyName|findstr UbuntuonWindows))"]
epics_path = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].decode().rstrip()
if not os.path.isdir(epics_path):
    epics_path = f"{os.getenv('LOCALAPPDATA')}/Packages/CanonicalGroupLimited.UbuntuonWindows_79rhkp1fndgsc/LocalState/rootfs/home/epics".replace('\\', '/')
epics_path_wsl = '/home/epics'
localappdata = os.getenv("LOCALAPPDATA").replace("\\", "/")
localappdata_program = f'{localappdata}/CAMELS'
localappdata_program_wsl = f'/mnt/{localappdata_program[0].lower()}{localappdata_program[2:]}'

def clean_up_ioc(ioc='CAMELS'):
    info1 = subprocess.Popen(['wsl', './EPICS_handling/clean_up_ioc.cmd', ioc], stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0]
    info2 = subprocess.Popen(['wsl', './EPICS_handling/create_ioc.cmd', ioc], stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0]
    return f'{info1.decode()}\n\n{info2.decode()}'

def make_ioc(ioc='CAMELS'):
    """This function calls the make_ioc.cmd from the wsl shell.
    It goes to the given ioc, and performs one "make distclean" followed by a "make"."""
    ioc_sup_path = f'{epics_path}/IOCs/{ioc}/{ioc}Sup'
    if os.path.isdir(ioc_sup_path) and not len(os.listdir(ioc_sup_path)) > 0:
        os.rmdir(ioc_sup_path)
    output = subprocess.Popen(['wsl', './EPICS_handling/make_ioc.cmd', ioc], stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0]
    return output.decode()


def change_devices(device_dict:dict, ioc='CAMELS'):
    """First, all the '.db' files are removed from the 'ioc'App/Db directory, also the supporting files in 'ioc'Sup are removed. Depending on the given device_dict, the necessary files of the files are added to the files that are to be copied. If there are requirements specified, they will first be collected in a list, to avoid duplicates. Then, the requirements are also added to the copying-string. The string is then written in a temporary file 'copy_temp.cmd', in binary. Subprocess is used to call the wsl to run 'copy_temp.cmd'. This workaround is necessary, as the file-protections etc. have to be correct in the wsl environment."""
    driver_path = variables_handling.device_driver_path
    # driver_path = 'C:/Users/od93yces/FAIRmat/devices_drivers'
    driver_path_wsl = f'/mnt/{driver_path[0].lower()}{driver_path[2:]}'
    required = []
    db_path_wsl = f'{epics_path_wsl}/IOCs/{ioc}/{ioc}App/Db'
    sup_path_wsl = f'{epics_path_wsl}/IOCs/{ioc}/{ioc}Sup'
    ioc_boot_path_wsl = f'{epics_path_wsl}/IOCs/{ioc}/iocBoot/ioc{ioc}'
    src_path_wsl = f'{epics_path_wsl}/IOCs/{ioc}/{ioc}App/src'

    # cleaning out the paths
    path = f'{epics_path}/IOCs/{ioc}/{ioc}App/Db'
    if os.path.isdir(path):
        for file in os.listdir(path):
            # if file == 'Makefile':
            #     continue
            os.remove(f'{path}/{file}')
    path = f'{epics_path}/IOCs/{ioc}/{ioc}Sup'
    if os.path.isdir(path):
        for file in os.listdir(path):
            os.remove(f'{path}/{file}')

    # adding devices / files
    st_cmd_string = f'#!../../bin/linux-x86_64/{ioc}\n< envPaths\n'
    st_cmd_string += 'epicsEnvSet("STREAM_PROTOCOL_PATH", "$(TOP)/db")\n'
    asyn_port_string = '# Set up ASYN port\n'
    load_record_string = '## Load record instances\n'
    addresses = {}
    write_string = ''
    make_db_string = 'TOP=../..\ninclude $(TOP)/configure/CONFIG\n'
    for key in sorted(device_dict):
        device = device_dict[key]
        device_path_wsl = f'{driver_path_wsl}/{device.directory}'
        for req in device.requirements:
            if req not in required:
                required.append(req)
        for file in device.files:
            write_string += f'cp {device_path_wsl}/{file} {db_path_wsl}/{file}\n'
            make_db_string += f'DB += {file}\n'
        # if 'settings' in device:
        asyn_port_string, load_record_string = update_addresses(key, addresses, device.settings, asyn_port_string, load_record_string, ioc)
    includers = ['calc', 'stream', 'asyn'] + required
    for req in required:
        req_path = f'{driver_path}/Support/{req}'
        req_path_wsl = f'{driver_path_wsl}/Support/{req}'
        if not os.path.isdir(req_path):
            continue
        for file in os.listdir(req_path):
            write_string += f'cp {req_path_wsl}/{file} {sup_path_wsl}/{file}\n'
            if file.endswith('.dbd'):
                write_string += f'cp {req_path_wsl}/{file} {src_path_wsl}/{file}\n'
    make_db_string += 'DB_INSTALLS += $(ASYN)/db/asynRecord.db\ninclude $(TOP)/configure/RULES\n'
    with open(f'{localappdata_program}/Makefile_db', 'wb') as file:
        file.write(make_db_string.encode())
    write_string += f'cp {localappdata_program_wsl}/Makefile_db {db_path_wsl}/Makefile.test\n'
    write_string += f'mv {db_path_wsl}/Makefile.test {db_path_wsl}/Makefile\n'

    # making st.cmd
    st_cmd_string += 'epicsEnvSet("PROLOGIX_ADDRESS", "$(PROLOGIX_ADDRESS=10.131.162.32)");\n'
    st_cmd_string += 'epicsEnvSet("P", "$(P=Prologix:)");\n'
    st_cmd_string += 'epicsEnvSet("R", "$(R=Test:)");\n'
    st_cmd_string += 'epicsEnvSet("A", "$(A=5)");\n'
    st_cmd_string += 'epicsEnvSet("B", "$(B=23)");\n'
    st_cmd_string += 'cd "${TOP}"\n'
    st_cmd_string += '## Register all support components\n'
    st_cmd_string += f'dbLoadDatabase "dbd/{ioc}.dbd"\n'
    st_cmd_string += f'{ioc}_registerRecordDeviceDriver pdbbase\n'
    st_cmd_string += asyn_port_string
    st_cmd_string += load_record_string
    st_cmd_string += 'iocInit()\n'
    st_cmd_string += '## Start any sequence programs\n'
    st_cmd_string += f'#seq snc{ioc},"user=epics"\n'
    with open(f'{localappdata_program}/st.cmd', 'wb') as file:
        file.write(st_cmd_string.encode())
    write_string += f'cp {localappdata_program_wsl}/st.cmd {ioc_boot_path_wsl}/st.cmd\n'
    # Makefile for iocApp/src
    make_src_string = make_src_mk_string(ioc, includers)
    with open(f'{localappdata_program}/Makefile_src', 'wb') as file:
        file.write(make_src_string.encode())
    write_string += f'cp {localappdata_program_wsl}/Makefile_src {src_path_wsl}/Makefile\n'

    # copying all the files
    with open(f'{localappdata_program}/copy_temp.cmd', 'wb') as file:
        file.write(write_string.encode())
    info = subprocess.Popen(['wsl', f'{localappdata_program_wsl}/copy_temp.cmd'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0]
    if len(info.decode()) > 0:
        return info.decode()
    else:
        return f'Adding devices...\n{write_string}'
    # TODO check whether correct in all cases, more possibilities for connections

def add_to_string(req, dbd_string, libs_string, ioc):
    non_lib = ['drvAsynSerialPort']
    if req == 'std':
        dbd_string += f'{ioc}_DBD += stdSupport.dbd\n'
        libs_string += f'{ioc}_LIBS += {req}\n'
    else:
        dbd_string += f'{ioc}_DBD += {req}.dbd\n'
        if req not in non_lib:
            libs_string += f'{ioc}_LIBS += {req}\n'
    return dbd_string, libs_string

def make_src_mk_string(ioc, included):
    driver_path = variables_handling.device_driver_path
    add_order = ['calc', 'prologixSup', 'stream', 'asyn', 'drvAsynSerialPort', 'std']
    non_copy = ['calc', 'stream', 'asyn', 'drvAsynSerialPort', 'std']
    add_src_dbd_string = ''
    add_src_libs_string = ''
    for req in add_order:
        if req not in included:
            continue
        if req in non_copy:
            add_src_dbd_string, add_src_libs_string = add_to_string(req, add_src_dbd_string, add_src_libs_string, ioc)
            continue
        req_path = f'{driver_path}/Support/{req}'
        for file in os.listdir(req_path):
            if file.endswith('.dbd'):
                add_src_dbd_string += f'{ioc}_DBD += {file}\n'
                add_src_libs_string += f'{ioc}_LIBS += {file[:-4]}\n'
    make_src_string = 'TOP=../..\n'
    make_src_string += 'include $(TOP)/configure/CONFIG\n'
    make_src_string += '#----------------------------------------\n'
    make_src_string += '#  ADD MACRO DEFINITIONS AFTER THIS LINE\n'
    make_src_string += '#=============================\n'
    make_src_string += '#=============================\n'
    make_src_string += '# Build the IOC application\n'
    make_src_string += f'PROD_IOC = {ioc}\n'
    make_src_string += f'# {ioc}.dbd will be created and installed\n'
    make_src_string += f'DBD += {ioc}.dbd\n'
    make_src_string += f'# {ioc}.dbd will be made up from these files:\n'
    make_src_string += f'{ioc}_DBD += base.dbd\n'
    make_src_string += '# Include dbd files from all support applications:\n'
    make_src_string += f'#{ioc}_DBD += xxx.dbd\n'
    make_src_string += add_src_dbd_string
    make_src_string += '# Add all the support libraries needed by this IOC\n'
    make_src_string += f'#{ioc}_LIBS += xxx\n'
    make_src_string += add_src_libs_string
    make_src_string += f'# {ioc}_registerRecordDeviceDriver.cpp derives from {ioc}.dbd\n'
    make_src_string += f'{ioc}_SRCS += {ioc}_registerRecordDeviceDriver.cpp\n'
    make_src_string += '# Build the main IOC entry point on workstation OSs.\n'
    make_src_string += f'{ioc}_SRCS_DEFAULT += {ioc}Main.cpp\n'
    make_src_string += f'{ioc}_SRCS_vxWorks += -nil-\n'
    make_src_string += '# Add support from base/src/vxWorks if needed\n'
    make_src_string += f'#{ioc}_OBJS_vxWorks += $(EPICS_BASE_BIN)/vxComLibrary\n'
    make_src_string += '# Finally link to the EPICS Base libraries\n'
    make_src_string += f'{ioc}_LIBS += $(EPICS_BASE_IOC_LIBS)\n'
    make_src_string += '#===========================\n'
    make_src_string += 'include $(TOP)/configure/RULES\n'
    make_src_string += '#----------------------------------------\n'
    make_src_string += '#  ADD RULES AFTER THIS LINE\n'
    return make_src_string



def update_addresses(device, address_dict, device_settings, port_string, record_string, ioc):
    """Called by change_devices. Updates the two given strings with the necessary lines for the given device.
    Arguments:
        - device: The device name, as for the loaded database.
        - address_dict: The dictionary with so far used addresses, needed to number the the ports, e.g. the IP-Addresses for Prologix-Adapters.
        - device_settings: The dictionary of device-settings, specifically 'connection'.
        - port_string: The string to be updated with additional asyn-ports.
        - record_string: The string to be updated with additional databases."""
    if 'connection' in device_settings:
        conn_dict = device_settings['connection']
        conn_type = conn_dict['type']
        if conn_type not in address_dict:
            address_dict.update({conn_type: []})
        if conn_type == 'prologix-GPIB':
            if conn_dict['IP-Address'] in address_dict[conn_type]:
                n = address_dict[conn_type].index(conn_dict['IP-Address'])
            else:
                n = len(address_dict[conn_type])
                address_dict[conn_type].append(conn_dict['IP-Address'])
                port_string += f'prologixGPIBConfigure("L{n}", "{conn_dict["IP-Address"]}")\n'
                port_string += f'asynOctetSetInputEos("L{n}", -1, "\\n")\n'
                port_string += f'asynSetTraceIOMask("L{n}_TCP", -1, 0x2)\n'
                port_string += f'asynSetTraceMask("L{n}_TCP", -1, 0x9)\n'
                port_string += f'asynSetTraceIOMask("L{n}", $(A), 0x2)\n'
                port_string += f'asynSetTraceMask("L{n}", $(A), 0x9)\n'
            record_string += f'dbLoadRecords("db/{device.replace(" ", "_")}.db", "SETUP={ioc},PORT=L{n},G={conn_dict["GPIB-Address"]}")\n'  # TODO several devices of same type
    else:
        record_string += f'dbLoadRecords("db/{device.replace(" ", "_")}.db", "SETUP={ioc}")\n'
    return port_string, record_string





if __name__ == '__main__':
    # make_ioc()
    os.chdir('..')
    print(os.getcwd())
    # check_for_ioc('tester')
    # print(subprocess.run(['wsl', './test.cmd']))