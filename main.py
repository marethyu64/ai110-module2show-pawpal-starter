from datetime import datetime, time, timedelta
from pawpal_system import Owner, Pet

if __name__ == "__main__":
    owner = Owner("Jayden")

    pet1 = Pet(name="Fluffy", pet_type="Dog", breed="Labrador")
    pet2 = Pet(name="Whiskers", pet_type="Cat", breed="Siamese")

    owner.add_pet(pet1)
    owner.add_pet(pet2)

    # Use a fixed base time for today to ensure all tasks are on the same day
    today = datetime.now().replace(hour=8, minute=0, second=0, microsecond=0)

    # Add tasks out of order to test sorting
    owner.create_task(pet_id=pet1.pet_id, description="Evening walk", time_scheduled=today + timedelta(hours=6), priority=1)
    owner.create_task(pet_id=pet1.pet_id, description="Morning walk", time_scheduled=today + timedelta(hours=1), priority=2)
    owner.create_task(pet_id=pet2.pet_id, description="Grooming", time_scheduled=today + timedelta(hours=2), priority=3)
    owner.create_task(pet_id=pet1.pet_id, description="Feed breakfast", time_scheduled=today + timedelta(hours=0.5), priority=1)
    owner.create_task(pet_id=pet2.pet_id, description="Feed dinner", time_scheduled=today + timedelta(hours=5), priority=2)
    
    # Add recurring tasks
    owner.create_task(pet_id=pet1.pet_id, description="Daily medication", time_scheduled=today + timedelta(hours=3), priority=1, frequency="daily")
    owner.create_task(pet_id=pet2.pet_id, description="Weekly nail trim", time_scheduled=today + timedelta(hours=4), priority=2, frequency="weekly")
    
    # Add conflicting tasks at the same time
    conflict_time = today + timedelta(hours=2, minutes=30)
    owner.create_task(pet_id=pet1.pet_id, description="Play time", time_scheduled=conflict_time, priority=3)
    owner.create_task(pet_id=pet2.pet_id, description="Vet check", time_scheduled=conflict_time, priority=1)

    # Check for conflicts and print warnings
    conflicts = owner.scheduler.detect_conflicts()
    if conflicts:
        print("🚨 Scheduling Conflicts Detected:")
        for warning in conflicts:
            print(f"  {warning}")
        print()
    else:
        print("✅ No scheduling conflicts detected.\n")

    # Mark some tasks as completed to test filtering and recurring task creation
    owner.scheduler.mark_task_complete(owner.scheduler.tasks[1])  # Morning walk (once)
    owner.scheduler.mark_task_complete(owner.scheduler.tasks[3])  # Feed dinner (once)
    owner.scheduler.mark_task_complete(owner.scheduler.tasks[5])  # Daily medication (should create tomorrow's instance)
    owner.scheduler.mark_task_complete(owner.scheduler.tasks[6])  # Weekly nail trim (should create next week's instance)

    today_tasks = owner.scheduler.generate_daily_task_list(today)

    print("Today's Schedule (sorted by priority)")
    for task in today_tasks:
        pet = owner.get_pet_by_id(task.pet_id)
        pet_name = pet.name if pet else "Unknown Pet"
        print(f"- {task.time_scheduled.strftime('%H:%M')} | {pet_name} | {task.description} | priority {task.priority} | completed: {task.completion} | freq: {task.frequency}")

    print("\nToday's Schedule (sorted by time)")
    time_sorted_tasks = owner.scheduler.sort_by_time(today_tasks)
    for task in time_sorted_tasks:
        pet = owner.get_pet_by_id(task.pet_id)
        pet_name = pet.name if pet else "Unknown Pet"
        print(f"- {task.time_scheduled.strftime('%H:%M')} | {pet_name} | {task.description} | priority {task.priority} | completed: {task.completion} | freq: {task.frequency}")

    print("\nPending Tasks (filtered by completion status)")
    pending_tasks = owner.scheduler.filter_tasks(today_tasks, completion_status=False)
    for task in pending_tasks:
        pet = owner.get_pet_by_id(task.pet_id)
        pet_name = pet.name if pet else "Unknown Pet"
        print(f"- {task.time_scheduled.strftime('%H:%M')} | {pet_name} | {task.description} | priority {task.priority}")

    print("\nTasks for Fluffy (filtered by pet name)")
    fluffy_tasks = owner.scheduler.filter_tasks(today_tasks, pet_name="Fluffy", owner=owner)
    for task in fluffy_tasks:
        pet = owner.get_pet_by_id(task.pet_id)
        pet_name = pet.name if pet else "Unknown Pet"
        print(f"- {task.time_scheduled.strftime('%H:%M')} | {pet_name} | {task.description} | priority {task.priority} | completed: {task.completion}")

    # Show all tasks including future recurring ones
    print("\nAll Tasks (including future recurring):")
    all_tasks = owner.scheduler.get_all_tasks()
    for task in sorted(all_tasks, key=lambda t: t.time_scheduled):
        pet = owner.get_pet_by_id(task.pet_id)
        pet_name = pet.name if pet else "Unknown Pet"
        date_str = task.time_scheduled.strftime('%m/%d %H:%M')
        print(f"- {date_str} | {pet_name} | {task.description} | completed: {task.completion} | freq: {task.frequency}")
