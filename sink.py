import zmq
import time
import sys


def sink(num_workers):
    context = zmq.Context()
    # worker = context.socket(zmq.PULL)
    # worker.connect("tcp://localhost:5556")
    worker = context.socket(zmq.PULL)
    worker.bind("tcp://*:5557")


    completed = context.socket(zmq.PUSH)
    completed.bind("tcp://*:5558")
    for _ in range(num_workers + 1):
        worker_id = worker.recv_string()
        print(f"Received worker ID: {worker_id}")

    fact = 1
    try:
        for _ in range(num_workers):
            result = worker.recv_string()
            try:
                fact*=int(result)
            except ValueError:
                pass
    except KeyboardInterrupt:
        worker.close()
        context.term()
    print(f"Factorial is {fact}")
    completed.send_string("DONE")

if __name__ == "__main__":
    sink(int(sys.argv[1]))