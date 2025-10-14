import time
import bot.client
import bot.database

def main() -> None:
    next_updates_offset = 0
    try:
        while(True):
            updates = bot.client.getUpdates(next_updates_offset)
            bot.database.persist_updates(updates)
            for update in updates:
                try:
                    bot.client.sendMessage(
                        chat_id=update["message"]["chat"]["id"],
                        text=update["message"]["text"],
                    )
                except:
                    pass
                print(".",  end="", flush=True)
                next_updates_offset = max(next_updates_offset, update["update_id"] + 1)
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nBye!")
        
if __name__ == "__main__":
    main()