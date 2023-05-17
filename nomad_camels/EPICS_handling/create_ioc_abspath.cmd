cd /home/epics/IOCs
mkdir $1
cd $1
/home/epics/EPICS/epics-base/bin/linux-x86_64/makeBaseApp.pl -t ioc $1
echo | /home/epics/EPICS/epics-base/bin/linux-x86_64/makeBaseApp.pl -i -t ioc $1
cd iocBoot/ioc$1
chmod u+x st.cmd
