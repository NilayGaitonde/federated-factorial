import zmq
import sys
import timeit
import time
import numpy as np

def main(fact: int) -> None:
    context = zmq.Context()
    sender = context.socket(zmq.DEALER)  # Send to the load balancer
    sender.connect("tcp://localhost:5555")  # Connect to load balancer's ROUTER

    worker = context.socket(zmq.PUSH)
    worker.connect("tcp://localhost:5556")

    sink = context.socket(zmq.PUSH)
    sink.connect("tcp://localhost:5557")
    sink.send_string("Ventilator signal")
    try:
        for i in range(1, fact + 1):
            print(i)
            sender.send_string(str(i))
            print("Sent")
        sender.send_string("STOP")
    except KeyboardInterrupt:
        sender.close()
        context.term()

if __name__ == "__main__":
    num = int(sys.argv[1])
    main(num)