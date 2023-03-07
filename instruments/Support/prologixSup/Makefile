TOP=..
include $(TOP)/configure/CONFIG
#=======================================

# Build drvPrologixGPIB as a library for an IOC:
LIBRARY_IOC += drvPrologixGPIB

# Library Source files
drvPrologixGPIB_SRCS += drvPrologixGPIB.c

# Link with the asyn and base libraries
drvPrologixGPIB_LIBS += asyn
drvPrologixGPIB_LIBS += $(EPICS_BASE_IOC_LIBS)

# Install .dbd
DBD += drvPrologixGPIB.dbd

#=======================================
include $(TOP)/configure/RULES
