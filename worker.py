import zmq
import sys
import time
import uuid

def worker():
    context = zmq.Context()

    worker_id = uuid.uuid4()
    receiver = context.socket(zmq.DEALER)  # Connect to load balancer's DEALER
    receiver.setsockopt(zmq.IDENTITY, str(worker_id).encode('utf-8'))
    receiver.connect("tcp://localhost:5556")

    sender = context.socket(zmq.PUSH)
    sender.connect("tcp://localhost:5557")

    print(f"Worker ID: {worker_id}")
    sender.send_string(str(worker_id))
    print("Sent worker ID")
    local_result = 1
    while True:
        print("Waiting for message")
        message = receiver.recv_multipart()  # DEALER socket adds an envelope
        _, task = message  # The actual task is the second part
        task = task.decode('utf-8')
        print(f"Worker {worker_id} got {task}")
        try:
            if task == "STOP":
                sender.send_string(str(local_result))
                break
            local_result *= int(task)
            time.sleep(0.1)
        except ValueError:
            print(f"Worker {worker_id} received invalid task: {task}")
    print(f"Worker {worker_id} OUT OF LOOP")
    receiver.close()
    sender.close()
    context.term()

if __name__ == "__main__":
    worker()