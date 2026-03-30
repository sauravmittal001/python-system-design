# Problem: Event Scheduler with Conflict Resolution
# You are building an Event Scheduler system that allows users to create events on a shared calendar.

# Each event has:
# event_id: string
# start_time: integer (epoch seconds)
# end_time: integer (epoch seconds)
# user_id: string

# Requirements:

# You need to support adding events.
# Reject an event if it conflicts with an already scheduled event for the same user.

# Allow querying:
# All events for a user, sorted by start time

# All overlapping events within a given time range, across all users
# 1. add event (st_t, en_t, user_id) -> true/false
# 2. reject conflicted events
# 3. person events -> query by user_id
# 4. list events in that time (event st/en time within the time range or just st time)

import bisect
from collections import defaultdict


class Event:
    def __init__(self, event_id, start, end, user_id):
        self.event_id = event_id
        self.start = start
        self.end = end
        self.user_id = user_id

    def __lt__(self, other):
        return self.start < other.start

    def __repr__(self):
        return f"({self.event_id}, {self.start}, {self.end}, {self.user_id})"


class EventScheduler:
    def __init__(self):
        # user_id -> sorted list of events
        self.user_events = defaultdict(list)

        # all events (unsorted or sorted depending on need)
        self.all_events = []

    # 1. Add event
    def add_event(self, event_id, start, end, user_id):
        new_event = Event(event_id, start, end, user_id)
        events = self.user_events[user_id]

        # Find position using binary search
        idx = bisect.bisect_left(events, new_event)

        # Check conflict with previous event
        if idx > 0 and events[idx - 1].end > start:
            return False

        # Check conflict with next event
        if idx < len(events) and events[idx].start < end:
            return False

        # No conflict → insert
        events.insert(idx, new_event)
        self.all_events.append(new_event)
        return True

    # 2. Get all events for a user (sorted)
    def get_user_events(self, user_id):
        return self.user_events[user_id]

    # 3. Get overlapping events in a time range (across all users)
    def get_events_in_range(self, start, end):
        result = []
        for event in self.all_events:
            if event.start < end and event.end > start:
                result.append(event)
        return result

scheduler = EventScheduler()

print(scheduler.add_event("e1", 10, 20, "u1"))  # True
print(scheduler.add_event("e2", 15, 25, "u1"))  # False (conflict)
print(scheduler.add_event("e3", 20, 30, "u1"))  # True

print(scheduler.get_user_events("u1"))
# [(e1, 10, 20, u1), (e3, 20, 30, u1)]

print(scheduler.get_events_in_range(18, 22))
# Overlapping events