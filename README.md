# Pokemon Route Completion Tracker

This is an early exploration of a program to track completion of the pokedex for the various pokemon games using various parameters. 
For simplicity sake I am going to start with Pokemon Red/Blue and track based on Route you can catch them on.
That is for the first implementation the user will type the Route/Area they are tracking into the command line and the program will return:

1. A list of caught pokemon
2. A list of uncaught pokemon available in the version of the game being tracked (if provided, otherwise 2 and 3 will be combined into one list)
3. A list of uncaught pokemon unavailable in the version of the game being tracked (if provided, otherwise 2 and 3 will be combined into one list)

Future features may include (in no particular order):
- a GUI rather than CLI
- Search for caught/uncaught status by individual pokemon
- Support for other games in the series
- Search individual pokemon to determine where it can be caught in all regions
