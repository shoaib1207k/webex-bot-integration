from bot_script import rooms, send_message_to_person, get_person_id
def main():
    print("Hello from webexbot!")

    rooms_list = rooms()
    print("Rooms List:", rooms_list)

    email = "shoaib12dev@gmail.com"
    person_id = get_person_id(email)

    print(f"Person ID for {email}:", person_id)

    send_message_to_person(person_id, "🚀 Hello Shoaib! This message was sent by my HITL Test Bot.")

if __name__ == "__main__":
    main()
