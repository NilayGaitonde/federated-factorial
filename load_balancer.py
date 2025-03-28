import zmq
import sys

def main(num_workers:int) -> None:
    context = zmq.Context()

    # Frontend socket (for ventilators/clients)
    frontend = context.socket(zmq.ROUTER)
    frontend.bind("tcp://*:5555")
    print("Load Balancer frontend bound to 5555")

    # Backend socket (for workers)
    backend = context.socket(zmq.DEALER)
    backend.bind("tcp://*:5556")
    print("Load Balancer backend bound to 5556")

    # Create a poller to manage messages between frontend and backend
    poller = zmq.Poller()
    poller.register(frontend, zmq.POLLIN)
    poller.register(backend, zmq.POLLIN)

    # Main proxy loop
    try:
        while True:
            socks = dict(poller.poll())

            if frontend in socks:
                # Receive message from ventilator
                message = frontend.recv_multipart()
                print(f"Frontend received: {message}")
                if message[1] == b"STOP":
                    print("Stopping ZeroMQ proxy...")
                    for _ in range(num_workers**2):
                        print("Sending STOP to backend")
                        backend.send_multipart(message)
                    break
                backend.send_multipart(message)
                # backend.send_string(message[1].decode('utf-8'))
                print("Sent to backend")

            if backend in socks:
                # Receive message from worker
                message = backend.recv_multipart()
                print(f"Backend received: {message}")
                frontend.send_multipart(message)
                print("Sent to frontend")

    except KeyboardInterrupt:
        print("\nStopping ZeroMQ proxy...")
    finally:
        frontend.close()
        backend.close()
        context.term()

if __name__ == "__main__":
    main(int(sys.argv[1]))