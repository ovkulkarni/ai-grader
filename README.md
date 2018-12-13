# AI Grader

This is a web application I wrote in Django to help grade labs for the AI class at TJHSST.
It leverages `celery` to run the grader scripts in the background. This allows long-running scripts and creates a queue so that there are not too many jobs running at once.