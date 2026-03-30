import pytest
from datetime import datetime, timedelta
from pawpal_system import Owner, Pet


def test_task_completion_marks_task_complete():
    owner = Owner("TestUser")
    pet = Pet(name="Rover", pet_type="Dog", breed="Beagle")
    owner.add_pet(pet)

    task = owner.create_task(
        pet_id=pet.pet_id,
        description="Walk the dog",
        time_scheduled=datetime.now() + timedelta(hours=1),
        priority=1,
    )

    assert task.completion is False
    task.mark_task_completion()
    assert task.completion is True
    assert task.last_completed is not None


def test_task_addition_increases_pet_task_count():
    owner = Owner("TestUser")
    pet = Pet(name="Mittens", pet_type="Cat", breed="Tabby")
    owner.add_pet(pet)

    initial_tasks = owner.scheduler.get_tasks_for_pet(pet.pet_id)
    assert len(initial_tasks) == 0

    owner.create_task(
        pet_id=pet.pet_id,
        description="Feed the cat",
        time_scheduled=datetime.now() + timedelta(hours=2),
        priority=1,
    )

    owner.create_task(
        pet_id=pet.pet_id,
        description="Play with yarn",
        time_scheduled=datetime.now() + timedelta(hours=3),
        priority=2,
    )

    tasks_after = owner.scheduler.get_tasks_for_pet(pet.pet_id)
    assert len(tasks_after) == 2


def test_sort_by_time_returns_chronological_order():
    owner = Owner("TestUser")
    pet = Pet(name="Max", pet_type="Dog", breed="Labrador")
    owner.add_pet(pet)

    base_time = datetime.now().replace(hour=9, minute=0, second=0, microsecond=0)
    
    # Create tasks out of chronological order
    task3 = owner.create_task(
        pet_id=pet.pet_id,
        description="Evening walk",
        time_scheduled=base_time + timedelta(hours=6),  # 3:00 PM
        priority=1,
    )
    
    task1 = owner.create_task(
        pet_id=pet.pet_id,
        description="Morning walk",
        time_scheduled=base_time + timedelta(hours=1),  # 10:00 AM
        priority=2,
    )
    
    task2 = owner.create_task(
        pet_id=pet.pet_id,
        description="Lunch feeding",
        time_scheduled=base_time + timedelta(hours=4),  # 1:00 PM
        priority=1,
    )

    # Get all tasks (they should be in creation order, not time order)
    all_tasks = owner.scheduler.get_all_tasks()
    
    # Sort by time
    sorted_tasks = owner.scheduler.sort_by_time(all_tasks)
    
    # Verify chronological order
    assert len(sorted_tasks) == 3
    assert sorted_tasks[0].description == "Morning walk"  # 10:00 AM
    assert sorted_tasks[1].description == "Lunch feeding"  # 1:00 PM
    assert sorted_tasks[2].description == "Evening walk"  # 3:00 PM
    
    # Verify the original list is not modified
    assert all_tasks[0].description == "Evening walk"  # Still in creation order
    
    # Verify exact times
    assert sorted_tasks[0].time_scheduled == base_time + timedelta(hours=1)
    assert sorted_tasks[1].time_scheduled == base_time + timedelta(hours=4)
    assert sorted_tasks[2].time_scheduled == base_time + timedelta(hours=6)


def test_recurring_daily_task_creates_next_occurrence():
    owner = Owner("TestUser")
    pet = Pet(name="Buddy", pet_type="Dog", breed="Golden Retriever")
    owner.add_pet(pet)

    today = datetime.now().replace(hour=10, minute=0, second=0, microsecond=0)
    
    # Create a daily task
    task = owner.create_task(
        pet_id=pet.pet_id,
        description="Daily walk",
        time_scheduled=today,
        priority=1,
        frequency="daily"
    )

    initial_task_count = len(owner.scheduler.get_all_tasks())
    
    # Mark the task as complete
    owner.scheduler.mark_task_complete(task)
    
    # Should have created a new task for tomorrow
    all_tasks = owner.scheduler.get_all_tasks()
    assert len(all_tasks) == initial_task_count + 1  # Original + 1 new
    
    # Find the new task
    new_tasks = [t for t in all_tasks if t.task_id != task.task_id]
    assert len(new_tasks) == 1
    new_task = new_tasks[0]
    
    # Check that the new task is scheduled for tomorrow at the same time
    expected_time = today + timedelta(days=1)
    assert new_task.time_scheduled == expected_time
    assert new_task.description == task.description
    assert new_task.frequency == "daily"
    assert new_task.pet_id == task.pet_id
    assert new_task.completion is False


def test_recurring_weekly_task_creates_next_occurrence():
    owner = Owner("TestUser")
    pet = Pet(name="Whiskers", pet_type="Cat", breed="Siamese")
    owner.add_pet(pet)

    today = datetime.now().replace(hour=14, minute=30, second=0, microsecond=0)
    
    # Create a weekly task
    task = owner.create_task(
        pet_id=pet.pet_id,
        description="Weekly grooming",
        time_scheduled=today,
        priority=2,
        frequency="weekly"
    )

    initial_task_count = len(owner.scheduler.get_all_tasks())
    
    # Mark the task as complete
    owner.scheduler.mark_task_complete(task)
    
    # Should have created a new task for next week
    all_tasks = owner.scheduler.get_all_tasks()
    assert len(all_tasks) == initial_task_count + 1  # Original + 1 new
    
    # Find the new task
    new_tasks = [t for t in all_tasks if t.task_id != task.task_id]
    assert len(new_tasks) == 1
    new_task = new_tasks[0]
    
    # Check that the new task is scheduled for next week at the same time
    expected_time = today + timedelta(days=7)
    assert new_task.time_scheduled == expected_time
    assert new_task.description == task.description
    assert new_task.frequency == "weekly"
    assert new_task.pet_id == task.pet_id
    assert new_task.completion is False


def test_conflict_detection_identifies_simultaneous_tasks():
    owner = Owner("TestUser")
    pet1 = Pet(name="Buddy", pet_type="Dog", breed="Golden Retriever")
    pet2 = Pet(name="Whiskers", pet_type="Cat", breed="Siamese")
    owner.add_pet(pet1)
    owner.add_pet(pet2)

    today = datetime.now().replace(hour=10, minute=0, second=0, microsecond=0)
    conflict_time = today + timedelta(hours=2)
    
    # Create tasks at different times (no conflicts)
    owner.create_task(pet_id=pet1.pet_id, description="Walk", time_scheduled=today + timedelta(hours=1), priority=1)
    owner.create_task(pet_id=pet2.pet_id, description="Feed", time_scheduled=today + timedelta(hours=1, minutes=30), priority=1)
    
    # Initially no conflicts
    conflicts = owner.scheduler.detect_conflicts()
    assert len(conflicts) == 0
    
    # Add two tasks at the same time (conflict)
    owner.create_task(pet_id=pet1.pet_id, description="Play time", time_scheduled=conflict_time, priority=2)
    owner.create_task(pet_id=pet2.pet_id, description="Vet check", time_scheduled=conflict_time, priority=1)
    
    # Should detect the conflict
    conflicts = owner.scheduler.detect_conflicts()
    assert len(conflicts) == 1
    assert "12:00" in conflicts[0]  # conflict_time is today (10:00) + 2 hours = 12:00
    assert "Play time" in conflicts[0]
    assert "Vet check" in conflicts[0]
