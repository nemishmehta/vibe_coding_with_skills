# Flight Delay Dashboard

An interactive dashboard that helps a traveler answer "when and where am I most likely to get delayed?" using 2013 NYC-departure flight data.

## Language

**Delay**:
The gap in minutes between a flight's scheduled and actual arrival time (`arr_delay`). Positive means late, negative means early. Departure delay (`dep_delay`) is tracked in the data but is not what this dashboard means by "delay" — a flight that leaves late but lands on time is not counted as delayed.
_Avoid_: departure delay, lateness

**Delayed Flight**:
A flight that arrived 15 or more minutes after its scheduled arrival time, matching the US DOT standard. Flights delayed by less than 15 minutes are not counted as "delayed" for dashboard purposes.
_Avoid_: late flight

**Cancelled Flight**:
A flight that never departed (no recorded departure time). Distinct from a Delayed Flight — a cancellation is not a large delay, it's a different outcome, and is tracked as its own metric (Cancellation Rate) rather than folded into delay statistics.

**Unknown Outcome Flight**:
A flight that departed but has no recorded arrival delay (~0.35% of flights) — most likely a diversion. Distinct from both a Delayed Flight and a Cancelled Flight: it did depart, but its arrival outcome can't be computed. Excluded from the denominators of both Delay Rate and Cancellation Rate; tracked as its own small third rate so the dashboard's numbers still account for every flight.

**Delay Rate**:
The percentage of flights that *actually flew and have a recorded arrival* which were Delayed Flights. Cancelled Flights and Unknown Outcome Flights are excluded from this rate's denominator — they're counted separately.

**Cancellation Rate**:
The percentage of scheduled flights that were Cancelled Flights.

**Origin**:
The NYC-area airport (EWR, JFK, or LGA) a flight departed from. One of only three possible values in this dataset.

**Destination**:
The airport a flight was scheduled to fly to.

**Route**:
An Origin–Destination pair. Treated as a drill-down granularity beneath viewing Origin or Destination alone, not the default view.

**Traveler**:
The dashboard's assumed persona — an individual deciding when and from where to fly, weighing delay risk. Not an airline-ops or analyst persona.
