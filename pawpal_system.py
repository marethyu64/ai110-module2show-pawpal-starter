from dataclasses import dataclass, field
from datetime import datetime, time, timedelta
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
        if "pet_id" in info:
            self.pet_id = info["pet_id"]
    
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
    
    def sort_by_time(self, tasks: List[Task]) -> List[Task]:
        """Sort a list of tasks by their scheduled time in ascending order.
        
        Args:
            tasks: List of Task objects to sort
            
        Returns:
            List[Task]: New sorted list of tasks (original list is not modified)
            
        Note:
            Uses Python's sorted() function with a lambda key function.
            For sorting HH:MM time strings, you would use:
            sorted(time_strings, key=lambda t: datetime.strptime(t, "%H:%M"))
        """
        return sorted(tasks, key=lambda t: t.time_scheduled)
    
    def filter_tasks(self, tasks: List[Task], completion_status: Optional[bool] = None, 
                    pet_name: Optional[str] = None, owner: Optional['Owner'] = None) -> List[Task]:
        """Filter tasks by completion status and/or pet name.
        
        Args:
            tasks: List of Task objects to filter
            completion_status: If provided, filter tasks by completion status
                             (True for completed, False for pending)
            pet_name: If provided, filter tasks for pets with this name
            owner: Owner object required when filtering by pet_name to access pet list
            
        Returns:
            List[Task]: Filtered list of tasks matching the criteria
            
        Example:
            # Get all pending tasks
            pending = scheduler.filter_tasks(all_tasks, completion_status=False)
            
            # Get tasks for specific pet
            pet_tasks = scheduler.filter_tasks(all_tasks, pet_name="Fluffy", owner=owner)
        """
        filtered = tasks.copy()
        
        if completion_status is not None:
            filtered = [t for t in filtered if t.completion == completion_status]
        
        if pet_name is not None and owner is not None:
            # Find pet by name to get pet_id
            pet = next((p for p in owner.pets if p.name == pet_name), None)
            if pet:
                filtered = [t for t in filtered if t.pet_id == pet.pet_id]
        
        return filtered
    
    def mark_task_complete(self, task: Task) -> None:
        """Mark a task as completed and create next occurrence for recurring tasks.
        
        Args:
            task: The Task object to mark as completed
            
        Behavior:
            - Marks the task as completed and sets last_completed timestamp
            - For daily tasks: Creates a new task instance for the next day
            - For weekly tasks: Creates a new task instance for next week
            - For one-time tasks: No new task is created
            
        Example:
            # Complete a daily medication task
            scheduler.mark_task_complete(daily_medication_task)
            # This will create tomorrow's medication task automatically
        """
        task.mark_task_completion()
        
        # Handle recurring tasks
        if task.frequency == "daily":
            # Create next daily occurrence
            next_occurrence = task.time_scheduled + timedelta(days=1)
            new_task = Task(
                description=task.description,
                time_scheduled=next_occurrence,
                priority=task.priority,
                pet_id=task.pet_id,
                frequency=task.frequency
            )
            self.add_task(new_task)
        elif task.frequency == "weekly":
            # Create next weekly occurrence
            next_occurrence = task.time_scheduled + timedelta(days=7)
            new_task = Task(
                description=task.description,
                time_scheduled=next_occurrence,
                priority=task.priority,
                pet_id=task.pet_id,
                frequency=task.frequency
            )
            self.add_task(new_task)
        # For "once" and "monthly" frequencies, no new task is created
    
    def detect_conflicts(self) -> List[str]:
        """Detect scheduling conflicts and return warning messages.
        
        Returns:
            List[str]: List of warning messages for detected conflicts
            
        Algorithm:
            Lightweight strategy that checks for exact time matches between tasks.
            Groups tasks by their scheduled datetime and identifies any time slots
            with multiple tasks as conflicts.
            
        Note:
            This method only detects exact time conflicts, not overlapping durations.
            Tasks are considered to conflict if they have identical scheduled times.
            
        Example:
            conflicts = scheduler.detect_conflicts()
            if conflicts:
                for warning in conflicts:
                    print(warning)
        """
        warnings = []
        # Group tasks by scheduled time
        time_groups = {}
        
        for task in self.tasks:
            time_key = task.time_scheduled
            if time_key not in time_groups:
                time_groups[time_key] = []
            time_groups[time_key].append(task)
        
        # Check for conflicts (multiple tasks at same time)
        for time_key, tasks_at_time in time_groups.items():
            if len(tasks_at_time) > 1:
                task_descriptions = [f"'{t.description}'" for t in tasks_at_time]
                time_str = time_key.strftime("%m/%d %H:%M")
                warning = f"⚠️  Scheduling conflict at {time_str}: {', '.join(task_descriptions)} are scheduled simultaneously"
                warnings.append(warning)
        
        return warnings
    
    def get_tasks_for_pet(self, pet_id: str) -> List[Task]:
        """Retrieve all tasks associated with a specific pet."""
        return [task for task in self.tasks if task.pet_id == pet_id]
    
    def get_all_tasks(self) -> List[Task]:
        """Retrieve all tasks across all pets."""
        return self.tasks.copy()
    
    def edit_task(self, task_id: str, info: Dict[str, Any]) -> bool:
        """Edit an existing task by its ID.
        
        Args:
            task_id: The unique ID of the task to edit
            info: Dictionary containing the fields to update
            
        Returns:
            bool: True if task was found and edited, False otherwise
        """
        for task in self.tasks:
            if task.task_id == task_id:
                task.edit_task_info(info)
                return True
        return False
    
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
    
    def edit_task(self, task_id: str, info: Dict[str, Any]) -> bool:
        """Edit an existing task.
        
        Args:
            task_id: The unique ID of the task to edit
            info: Dictionary containing the fields to update (description, priority, time_scheduled, frequency, pet_id)
            
        Returns:
            bool: True if task was found and edited, False otherwise
        """
        return self.scheduler.edit_task(task_id, info)
    
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
