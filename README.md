## Description
TritonScheduler is a schedule for UCSD students. The schedule data is found using the [Schedule of Classes](https://act.ucsd.edu/scheduleOfClasses/scheduleOfClassesStudent.htm). The schedules are generated by using a genetic algorithm to find an optimal schedule. Factors such as conflicts, gaps in the schedule, having 8 AMs, no lunch break, and having classes that are late are considered in the schedule finding algorithm.

Note that this is still a work-in-progress.

## Installation
The dependencies ([Requests](https://github.com/kennethreitz/requests) and [lxml](https://github.com/lxml/lxml)) can be simply installed by typing `make`.

## Running
The program can be ran by using `make run`.