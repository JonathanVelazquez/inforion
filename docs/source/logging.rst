============
Logging
============
In this section we present how logging works on Inforion CLI and API.

Inforion use the Python's built-in logging module. The log level is INFO.

CLI
---

Inforion CLI add two log handlers:

- **Console**. It is a stream handler that sends the log messages to sys.stdout.

- **File**. When you run CLI commands an *inforion.log* file is created on the user's current folder. The file handler defines a time rotate that create a new file everyday.


API
----

When you user the Inforion API, by default, only the console handler is created.
