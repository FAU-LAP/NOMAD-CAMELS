The .cmd files in this directory are called from within the wsl, when an IOC is
made.

check_for_ioc.cmd:
    not needed anymore?
clean_up_ioc.cmd:
    remove the ioc-directory
create_ioc.cmd
    creates the directory, then makes the baseApp and changes rights on the
    `st.cmd`
make_ioc.cmd
    performs `make distclean` and `make`
run_ioc.cmd
    starts the `st.cmd`