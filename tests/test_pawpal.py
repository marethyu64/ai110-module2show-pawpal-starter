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
