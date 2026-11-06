import zmq
import multiprocessing

def run_zmq_proxy(queue: multiprocessing.Queue):
    """
    Binds to port 0 (OS picks a free port) and returns the chosen ports
    via the queue.
    """
    context = zmq.Context.instance()
    frontend = context.socket(zmq.SUB)
    backend = context.socket(zmq.PUB)
    
    # Binding to port 0 lets the OS pick an available port
    in_port = frontend.bind_to_random_port("tcp://*")
    out_port = backend.bind_to_random_port("tcp://*")
    
    frontend.setsockopt_string(zmq.SUBSCRIBE, "")
    
    # Send the chosen ports back to the main process
    queue.put((in_port, out_port))
    
    try:
        zmq.proxy(frontend, backend)
    except Exception:
        pass
    finally:
        frontend.close()
        backend.close()
        context.term()