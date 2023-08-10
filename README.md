# Informations about the project

This project still has some errors/problems and a TODO list.

## For errors/problems:
 - The SciPy Mixed Linear Optimizer does not necessarily recognize the difference between an unfeasible or unbounded problem. This differentiation being used in our project, we get a problem.
 - A problem of the satisfiability of the results returned by the belief review operator is present. We found a temporary solution with the rounding argument of the projector.
 - FloatConvexHullProjector probably has some issues while trying to project on dimensions n >= 2, since the quickhull algorithm only works with n+1 dots and cases where we have fewer dots need to be generalized.

## TODO list :
 - Fix all preceded errors ;
 - Top and Bottom implantation ;
 - Create a class for the weights of the distance function, and add a subclass corresponding to rational weights.
