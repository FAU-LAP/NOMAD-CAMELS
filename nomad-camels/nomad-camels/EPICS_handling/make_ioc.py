import subprocess
import os
from nomad-camels.utility import variables_handling

# Finding / configuring the paths that will be used when building the IOC
cmd = ['powershell', "echo ($env:LOCALAPPDATA + '\\Packages\\' + ($(get-appxpackage).PackageFamilyName|findstr UbuntuonWindows))"]
# epics_path = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0].decode().rstrip()
# if not os.path.isdir(epics_path):
#     epics_path = f"{os.getenv('LOCALAPPDATA')}/Packages/CanonicalGroupLimited.UbuntuonWindows_79rhkp1fndgsc/LocalState/rootfs/home/epics".replace('\\', '/')
epics_path_wsl = '/home/epics'
localappdata = os.getenv("LOCALAPPDATA").replace("\\", "/")
localappdata_program = f'{localappdata}/CAMELS'
localappdata_program_wsl = f'/mnt/{localappdata_program[0].lower()}{localappdata_program[2:]}'

def clean_up_ioc(ioc='CAMELS'):
    """Calls `clean_up_ioc.cmd` followed by `create_ioc.cmd` to build a
    fresh and empty IOC."""
    info1 = subprocess.Popen(['wsl', './EPICS_handling/clean_up_ioc.cmd', ioc],
                             stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT,
                             creationflags=subprocess.CREATE_NO_WINDOW).communicate()[0]
    info2, err = subprocess.Popen(['wsl', './EPICS_handling/create_ioc.cmd', ioc],
                                  stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE,
                                  creationflags=subprocess.CREATE_NO_WINDOW).communicate()
    if err and not info2:
        info2 = subprocess.Popen(['wsl', './EPICS_handling/create_ioc_abspath.cmd', ioc],
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.STDOUT,
                                 creationflags=subprocess.CREATE_NO_WINDOW).communicate()[0]
        return f'{info1.decode()}\n\n!!!!!using abspath!!!!!\n\n{info2.decode()}'
    return f'{info1.decode()}\n\n{info2.decode()}'

def make_ioc(ioc='CAMELS', info_signal=None, step_signal=None):
    """This function calls the make_ioc.cmd from the wsl shell.
    It goes to the given ioc, and performs one "make distclean" followed
    by a "make"."""
    # ioc_sup_path = f'{epics_path}/IOCs/{ioc}/{ioc}Sup'
    # if os.path.isdir(ioc_sup_path) and not len(os.listdir(ioc_sup_path)) > 0:
    #     os.rmdir(ioc_sup_path)
    cmd = ['wsl', './EPICS_handling/make_ioc.cmd', ioc]
    if info_signal is None:
        output = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                                  stderr=subprocess.STDOUT,
                                  creationflags=subprocess.CREATE_NO_WINDOW).communicate()[0]
        return output.decode()
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                         creationflags=subprocess.CREATE_NO_WINDOW,
                         bufsize=1)
    i = 0
    for line in iter(p.stdout.readline, b''):
        text = line.decode().rstrip()
        info_signal.emit(text)
        if step_signal is not None:
            step_signal.emit(10 + 90 / 500 * i)
        i += 1


def change_devices(device_dict:dict, ioc='CAMELS'):
    """First, all the '.db' files are removed from the 'ioc'App/Db
    directory, also the supporting files in 'ioc'Sup are removed.
    Depending on the given device_dict, the necessary files of the files
    are added to the files that are to be copied.
    If there are requirements specified, they will first be collected in
    a list, to avoid duplicates. Then, the requirements are also added
    to the copying-string. The string is then written in a temporary
    file 'copy_temp.cmd', in binary. Subprocess is used to call the wsl
    to run 'copy_temp.cmd'. This workaround is necessary, as the
    file-protections etc. have to be correct in the wsl environment."""
    driver_path = variables_handling.device_driver_path
    driver_path_wsl = f'/mnt/{driver_path[0].lower()}{driver_path[2:]}'
    supports = []
    db_path_wsl = f'{epics_path_wsl}/IOCs/{ioc}/{ioc}App/Db'
    sup_path_wsl = f'{epics_path_wsl}/IOCs/{ioc}/{ioc}Sup'
    ioc_boot_path_wsl = f'{epics_path_wsl}/IOCs/{ioc}/iocBoot/ioc{ioc}'
    src_path_wsl = f'{epics_path_wsl}/IOCs/{ioc}/{ioc}App/src'

    # adding devices / files
    asyn_port_string = '# Set up ASYN port\n'
    substitutions_string = ''
    addresses = {}
    write_string = ''
    make_db_string = 'TOP=../..\ninclude $(TOP)/configure/CONFIG\n'
    make_db_string += f'DB += {ioc}.substitutions\n'
    # going over the devices, adding their files and the requirements
    for key in sorted(device_dict):
        device = device_dict[key]
        device_path_wsl = f'{driver_path_wsl}/{device.directory}'
        if not device.ioc_settings or not device.ioc_settings['use_local_ioc']:
            continue
        for req in device.requirements:
            if req not in supports:
                supports.append(req)
        for file in device.files:
            write_string += f'cp {device_path_wsl}/{file} {db_path_wsl}/{file}\n'
            make_db_string += f'DB += {file}\n'
        asyn_port_string, comm = update_addresses(device, addresses,
                                                  asyn_port_string, supports)
        substitutions_string += device.get_substitutions_string(ioc, comm)
    includers = ['calc', 'stream', 'asyn'] + supports
    # going over the requirements, adding their files
    first_sup = True
    for req in supports:
        req_path = f'{driver_path}/Support/{req}'
        req_path_wsl = f'{driver_path_wsl}/Support/{req}'
        if not os.path.isdir(req_path):
            continue
        for file in os.listdir(req_path):
            if first_sup:
                write_string += f'mkdir {sup_path_wsl}\n'
                first_sup = False
            write_string += f'cp {req_path_wsl}/{file} {sup_path_wsl}/{file}\n'
            if file.endswith('.dbd'):
                write_string += f'cp {req_path_wsl}/{file} {src_path_wsl}/{file}\n'
    make_db_string += 'DB_INSTALLS += $(ASYN)/db/asynRecord.db\ninclude $(TOP)/configure/RULES\n'
    with open(f'{localappdata_program}/Makefile_db', 'wb') as file:
        file.write(make_db_string.encode())
    write_string += f'cp {localappdata_program_wsl}/Makefile_db {db_path_wsl}/Makefile.test\n'
    write_string += f'mv {db_path_wsl}/Makefile.test {db_path_wsl}/Makefile\n'

    # making st.cmd
    st_cmd_string = f'#!../../bin/linux-x86_64/{ioc}\n< envPaths\n'
    st_cmd_string += 'epicsEnvSet("STREAM_PROTOCOL_PATH", "$(TOP)/db")\n'
    # st_cmd_string += 'epicsEnvSet("PROLOGIX_ADDRESS", "$(PROLOGIX_ADDRESS=10.131.162.32)");\n'
    # st_cmd_string += 'epicsEnvSet("P", "$(P=Prologix:)");\n'
    # st_cmd_string += 'epicsEnvSet("R", "$(R=Test:)");\n'
    # st_cmd_string += 'epicsEnvSet("A", "$(A=5)");\n'
    # st_cmd_string += 'epicsEnvSet("B", "$(B=23)");\n'
    st_cmd_string += 'cd "${TOP}"\n'
    st_cmd_string += '## Register all support components\n'
    st_cmd_string += f'dbLoadDatabase "dbd/{ioc}.dbd"\n'
    st_cmd_string += f'{ioc}_registerRecordDeviceDriver pdbbase\n'
    st_cmd_string += asyn_port_string
    st_cmd_string += '## Load record instances\n'
    st_cmd_string += f'dbLoadTemplate "db/{ioc}.substitutions"\n'
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
    with open(f'{localappdata_program}/{ioc}.substitutions', 'wb') as file:
        file.write(substitutions_string.encode())
    write_string += f'cp {localappdata_program_wsl}/{ioc}.substitutions {db_path_wsl}/{ioc}.substitutions\n'
    # copying all the files
    with open(f'{localappdata_program}/copy_temp.cmd', 'wb') as file:
        file.write(write_string.encode())
    info = subprocess.Popen(['wsl', f'{localappdata_program_wsl}/copy_temp.cmd'],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT,
                            creationflags=subprocess.CREATE_NO_WINDOW).communicate()[0]
    if len(info.decode()) > 0:
        return info.decode()
    else:
        return f'Adding devices...\n{write_string}'
    # TODO check whether correct in all cases, more possibilities for connections

def add_to_string(req, dbd_string, libs_string, ioc):
    """Adding the requirements in the correct order to the DBD and LIBS-
    strings."""
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
    """This function should create the the makefile for the src
    directory using the correct order of included packages."""
    driver_path = variables_handling.device_driver_path
    add_order = ['calc', 'prologixSup', 'stream', 'asyn', 'drvAsynSerialPort',
                 'std']
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


sudo_pwd = ''


def update_addresses(device, address_dict, port_string, supports):
    """Called by change_devices. Updates the two given strings with the
    necessary lines for the given device.

    Parameters
    ----------
    device : device_class.Device
        The device object
    address_dict : dict
        The dictionary with so far used addresses, needed to number the
        the ports, e.g. the IP-Addresses for Prologix-Adapters.
    port_string : str
        The string to be updated with additional asyn-ports.
    supports : list
        The list will be updated, adding further necessary
        support-packages.
    """
    comm = ''
    if 'connection' in device.ioc_settings:
        conn_dict = device.ioc_settings['connection']
        conn_type = conn_dict['type']
        if conn_type not in address_dict:
            address_dict.update({conn_type: []})
        if conn_type == 'EPICS: prologix-GPIB':
            if 'prologixSup' not in supports:
                supports.append('prologixSup')
            if conn_dict['IP-Address'] in address_dict[conn_type]:
                n = address_dict[conn_type].index(conn_dict['IP-Address'])
            else:
                n = len(address_dict[conn_type])
                address_dict[conn_type].append(conn_dict['IP-Address'])
                port_string += f'prologixGPIBConfigure("prologix_{n}", "{conn_dict["IP-Address"]}")\n'
                port_string += f'asynOctetSetInputEos("prologix_{n}", -1, "\\n")\n'
                port_string += f'asynSetTraceIOMask("prologix_{n}_TCP", -1, 0x2)\n'
                port_string += f'asynSetTraceMask("prologix_{n}_TCP", -1, 0x9)\n'
                port_string += f'asynSetTraceIOMask("prologix_{n}", 5, 0x2)\n'
                port_string += f'asynSetTraceMask("prologix_{n}", 5, 0x9)\n'
            comm = f'prologix_{n} {conn_dict["GPIB-Address"]}'
        elif conn_type == 'EPICS: USB-serial':
            address_dict[conn_type].append(conn_dict['Port'])
            tty = f'/dev/ttyS{conn_dict["Port"][3:]}'
            info = subprocess.Popen(['wsl', './EPICS_handling/chmod_maker.cmd',
                                     sudo_pwd, tty],
                                    stderr=subprocess.STDOUT,
                                    creationflags=subprocess.CREATE_NO_WINDOW,
                                    stdout=subprocess.PIPE).communicate()
            print(info)
            port_string += f'drvAsynSerialPortConfigure({conn_dict["Port"]}, "{tty}")\n'
            port_string += f'asynSetOption({conn_dict["Port"]}, 1, "baud", "9600")\n'
            port_string += f'asynSetOption({conn_dict["Port"]}, 1, "bits", "8")\n'
            port_string += f'asynSetOption({conn_dict["Port"]}, 1, "parity", "none")\n'
            port_string += f'asynSetOption({conn_dict["Port"]}, 1, "stop", "1")\n'
            port_string += f'asynSetTraceIOMask({conn_dict["Port"]}, -1, 0x2)\n'
            port_string += f'asynSetTraceMask({conn_dict["Port"]}, -1, 0x9)\n'
            port_string += f'asynSetTraceIOMask({conn_dict["Port"]}, 5, 0x2)\n'
            comm = f'{conn_dict["Port"]} {tty}'
    return port_string, comm





if __name__ == '__main__':
    # make_ioc()
    os.chdir('..')
    print(os.getcwd())
    # check_for_ioc('tester')
    # print(subprocess.run(['wsl', './test.cmd']))