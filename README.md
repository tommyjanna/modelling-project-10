[![Work in Repl.it](https://classroom.github.com/assets/work-in-replit-14baed9a392b3a25080506f3b7b6d57f295ec2978f6f33ec97e36a161684cbe9.svg)](https://classroom.github.com/online_ide?assignment_repo_id=317169&assignment_repo_type=GroupAssignmentRepo)

# Flight Booking - CISC/CMPE 204 Modelling Project (Group 10)

This project uses the [Python package](https://pypi.org/project/nnf/) `nnf` for creating logical constraints in negation normal form.

Our model aims to represent a flight booking system for an airline on a given day.

There are a variable amount of airports and timesteps, that can be modified by changing the constant value at the top of the `run.py` program. Our project should be able to handle any number of airports/timesteps only limited by your computer's specs.

The booking system works on the basis of demand for flights at specific airportsneeding to be fulfilled each day.  In each generation of the model, the demand at each airport is a randomly generated number of flights. The number of pilots for a specific generation of themodel is the least number of pilots needed to fulfill the demand of each airport.


## Structure

* `run_verbose.py`: This program is functionally identical to `run.py`. This version enables additional verbose output to show the marker additional output to analyze the entire model that we used for debugging, without requiring them to modify the source code.
* `documents`: Contains folders for both of your draft and final submissions (including Jape proofs and final report). README.md files are included in both.
* `run.py`: General wrapper script that you can choose to use or not. Only requirement is that you implement the one function inside of there for the auto-checks.
* `test.py`: Run this file to confirm that your submission has everything required. This essentially just means it will check for the right files and sufficient theory size.
