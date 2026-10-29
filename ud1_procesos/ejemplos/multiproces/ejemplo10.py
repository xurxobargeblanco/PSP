import multiprocessing
import time

def event_worker(event, num):
   print(f"Worker {num} waiting for event")
   event.wait()
   print(f"Worker {num} received event")

if __name__ == '__main__':
   event = multiprocessing.Event()
   processes = []

   for i in range(5):
       process = multiprocessing.Process(target=event_worker, args=(event, i))
       processes.append(process)
       process.start()

   time.sleep(3)
   event.set()  # Trigger the event
   for process in processes:
       process.join()

   print("All event-driven processes are done")