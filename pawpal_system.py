from dataclasses import dataclass, field
from datetime import datetime, time
from typing import List, Dict, Any, Optional
import uuid


@dataclass
class Pet:
    """Represents a pet with its attributes and maintenance logs."""
    name: str
    pet_type: str
    breed: str
    logs: Dict[str, Any] = field(default_factory=dict)
    pet_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    
    def update_logs(self, log_type: str, value: Any) -> None:
        """Update pet logs with new information."""
        if log_type not in self.logs:
            self.logs[log_type] = []
        self.logs[log_type].append({"value": value, "timestamp": datetime.now()})
    
    def update_pet_info(self, info: Dict[str, Any]) -> None:
        """Update pet information."""
        if "name" in info:
            self.name = info["name"]
        if "pet_type" in info:
            self.pet_type = info["pet_type"]
        if "breed" in info:
            self.breed = info["breed"]
    
    def delete_pet(self) -> None:
        """Delete the pet."""
        pass


@dataclass
class Task:
    """Represents a scheduled pet care task."""
    description: str
    time_scheduled: datetime
    priority: int
    pet_id: str
    completion: bool = False
    frequency: str = "once"  # "once", "daily", "weekly", "monthly"
    task_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    last_completed: Optional[datetime] = None
    
    def edit_task_info(self, info: Dict[str, Any]) -> None:
        """Edit task information."""
        if "description" in info:
            self.description = info["description"]
        if "priority" in info:
            self.priority = info["priority"]
        if "time_scheduled" in info:
            self.time_scheduled = info["time_scheduled"]
        if "frequency" in info:
            self.frequency = info["frequency"]
    
    def mark_task_completion(self) -> None:
        """Mark the task as completed."""
        self.completion = True
        self.last_completed = datetime.now()
    
    def delete_task(self) -> None:
        """Delete the task."""
        pass


class Scheduler:
    """Manages scheduling of pet care tasks."""
    
    def __init__(self, owner: 'Owner'):
        self.owner: 'Owner' = owner
        self.available_hours: Dict[str, List[time]] = {}  # day -> list of available times
        self.tasks: List[Task] = []
    
    def add_task(self, task: Task) -> None:
        """Add a task to the scheduler."""
        self.tasks.append(task)
    
    def add_schedule(self, schedule: Dict[str, Any]) -> None:
        """Add a schedule with available time slots."""
        # schedule format: {"day": "Monday", "hours": [time(9, 0), time(17, 0)]}
        day = schedule.get("day")
        hours = schedule.get("hours", [])
        if day:
            self.available_hours[day] = hours
    
    def generate_daily_task_list(self, target_date: datetime) -> List[Task]:
        """Generate a daily list of tasks for a specific date."""
        daily_tasks = []
        target_day = target_date.strftime("%A")
        available = self.available_hours.get(target_day, [])
        
        for task in self.tasks:
            task_date = task.time_scheduled.date()
            if task_date == target_date.date():
                daily_tasks.append(task)
        
        # Sort by priority (higher priority first, i.e., lower number = higher priority)
        daily_tasks.sort(key=lambda t: t.priority)
        return daily_tasks
    
    def get_tasks_for_pet(self, pet_id: str) -> List[Task]:
        """Retrieve all tasks associated with a specific pet."""
        return [task for task in self.tasks if task.pet_id == pet_id]
    
    def get_all_tasks(self) -> List[Task]:
        """Retrieve all tasks across all pets."""
        return self.tasks.copy()
    
    def remove_pet_tasks(self, pet_id: str) -> None:
        """Remove all tasks associated with a pet (cascade on pet deletion)."""
        self.tasks = [task for task in self.tasks if task.pet_id != pet_id]


class Owner:
    """Represents a pet owner with their preferences and pets."""
    
    def __init__(self, name: str):
        self.name: str = name
        self.owner_preferences: Dict[str, Any] = {}
        self.pets: List[Pet] = []
        self.scheduler: Scheduler = Scheduler(self)
    
    def add_pet(self, pet: Pet) -> None:
        """Add a pet to the owner's collection."""
        self.pets.append(pet)
    
    def delete_pet(self, pet_id: str) -> None:
        """Delete a pet and cascade remove its tasks from scheduler."""
        self.pets = [pet for pet in self.pets if pet.pet_id != pet_id]
        self.scheduler.remove_pet_tasks(pet_id)
    
    def edit_name(self, new_name: str) -> None:
        """Edit the owner's name."""
        self.name = new_name
    
    def edit_preferences(self, preferences: Dict[str, Any]) -> None:
        """Edit the owner's preferences."""
        self.owner_preferences.update(preferences)
    
    def get_all_tasks(self) -> List[Task]:
        """Retrieve all tasks from all pets through the scheduler."""
        return self.scheduler.get_all_tasks()
    
    def get_pet_by_id(self, pet_id: str) -> Optional['Pet']:
        """Find a pet by its ID."""
        for pet in self.pets:
            if pet.pet_id == pet_id:
                return pet
        return None
    
    def create_task(self, pet_id: str, description: str, time_scheduled: datetime, 
                    priority: int = 1, frequency: str = "once") -> Task:
        """Create a new task for a pet and add it to the scheduler."""
        task = Task(
            description=description,
            time_scheduled=time_scheduled,
            priority=priority,
            pet_id=pet_id,
            frequency=frequency
        )
        self.scheduler.add_task(task)
        return task
