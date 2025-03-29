import zmq
import time
import sys
import timeit

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
    start_time = timeit.default_timer()
    fact = 1
    try:
        for _ in range(num_workers):
            print("Waiting for worker to complete")
            result = worker.recv_string()
            try:
                fact*=int(result)
            except ValueError:
                break
    except KeyboardInterrupt:
        pass
    finally:
        worker.close()
        completed.close()
        context.term()
    elapsed = timeit.default_timer() - start_time
    print(f"Elapsed time: {elapsed}")
    print(f"Factorial is {fact}")

if __name__ == "__main__":
    sink(int(sys.argv[1]))