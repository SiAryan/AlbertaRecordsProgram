Group:

	Luke Kapeluck - 1529435
	Aryan Singh - 1533732

Overview:

	The system designed is meant to be intuitive to use while providing the functionality required.
	The program was originally designed in C# to be used with a full GUI in Windows, but was later realized that this was not possible on the lab machines. This led to a good idea of what needed to be done when transferred to Python as the planning was already complete.

	The system will display individual commands for each user type which can be executed at any point during the process, except when entering a password on the login screen. Most of the time you will be using the program to enter values requested. Follow the directions prompted on the screen.

Software Design:

	The UI was designed with the idea of modularity to make the programming easier. Using nested dictionaries specifying allowed commands per screen type, and their descriptions we can easily design the software to use generic methods to handle all situations. The rulesets are defined in the dictionary known as 'screenRules'. Function pointers are then used to define what happens when that specific command is executed. Overall, this makes the UI's screens simple to define.

	We did not think it was necessary to apply a UI design pattern considering the small scale of the application, this also simplified the programming and allowed for easy modularity.

	//

Testing Strategy:
	
	The testing was done in stages as the programming was done, as well as when the program was completed. The UI was tested separately as a front-end application, and the SQL separately as back-end. This was to make sure that each side was done correctly before they were integrated.

	The front-end was tested by checking if every command was implemented correctly and all screens were shown as intended. If the program threw an error or didn't display as intended, then we know there was an error that needed to be fixed. If we could get through the whole program without that happening then we know it was done correctly

	//

Group Work Strategy:

	When initially starting the project in C#, as a group we agreed that Luke would do the front-end WPF application and Aryan would handle as much of the back-end as he can before Luke finished the front-end. It was chosen like this because Luke had job experience with WPF and could likely quickly program the front-end. The integration of C# with SQLite was deemed as more difficult and would likely take longer, so Luke would help when he finished.

	Plans stayed the same for simplicity when we switched over to Python. Python took more thinking for Luke to complete the front-end due to no design pattern and the error checking removed from WPF. Python and SQLite was a simpler integration thankfully.

	Luke was specifically responsible for doing as much of the project as possible without using the sqlite integration which was called front-end. Aryan being responsible for those wholes left, called back-end.

	Work started on October 30th for the Python application. Work ended on November 30th.
	Luke worked approximately 16 hours throughout the days stated, making progress on the design of the UI on Wednesday and Thursday mainly, and programming the UI and integrating the back-end on the remaining days. Part of the last couple days were spent helping with the back-end and integrating the back-end with the front end.

	//

	Luke and Aryan, being friends had a relatively easy time coordinating the work effort. Work was posted to a GitHub repository and source control was used to coordinate the programming. Both teammates met up multiple days to work on the project and test. Other communication was done over texting and GitHub.
