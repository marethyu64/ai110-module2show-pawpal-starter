from datetime import datetime, time, timedelta
from pawpal_system import Owner, Pet

if __name__ == "__main__":
    owner = Owner("Jayden")

    pet1 = Pet(name="Fluffy", pet_type="Dog", breed="Labrador")
    pet2 = Pet(name="Whiskers", pet_type="Cat", breed="Siamese")

    owner.add_pet(pet1)
    owner.add_pet(pet2)

    now = datetime.now()

    owner.create_task(pet_id=pet1.pet_id, description="Morning walk", time_scheduled=now + timedelta(hours=1), priority=1)
    owner.create_task(pet_id=pet1.pet_id, description="Feed breakfast", time_scheduled=now + timedelta(hours=0.5), priority=2)
    owner.create_task(pet_id=pet2.pet_id, description="Grooming", time_scheduled=now + timedelta(hours=2), priority=3)

    today_tasks = owner.scheduler.generate_daily_task_list(now)

    print("Today's Schedule")
    for task in today_tasks:
        pet = owner.get_pet_by_id(task.pet_id)
        pet_name = pet.name if pet else "Unknown Pet"
        print(f"- {task.time_scheduled.strftime('%H:%M')} | {pet_name} | {task.description} | priority {task.priority} | completed: {task.completion}")
