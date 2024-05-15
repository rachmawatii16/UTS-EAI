# subscriber.py
import redis

def handle_inventory_update(message):
    print(f"Received inventory update: {message['data']}" , flush=True)

def main():
    r = redis.Redis(host='192.168.1.3', port=6379, db=0)

    pubsub = r.pubsub()
    pubsub.subscribe('inventory_updates')

    for message in pubsub.listen():
        if message['type'] == 'message':
            handle_inventory_update(message)

if __name__ == "__main__":
    main()