#!/bin/bash
# Store the PID of cicflowmeter process
# Delay to allow the process to start properly
(
  # Child process
  # Create a new session and detach from the controlling terminal
  setsid >/dev/null 2>&1

  # Now the child process is independent and detached from the parent and terminal

  # Execute the desired command or script
  exec ./flowmeter.sh
) &

sleep 1
cicflowmeter_pid=$(ps aux | grep '[c]icflowmeter' | awk '{print $2}')

if [ -z "$cicflowmeter_pid" ]; then
    echo "Failed to get PID of cicflowmeter process."
    exit 1
fi

echo "cicflowmeter PID: $cicflowmeter_pid"

# Wait for 10 seconds
sleep 20

# Terminate cicflowmeter process with SIGINT
echo "Terminating cicflowmeter process with SIGINT..."
kill -s INT $cicflowmeter_pid

# Check if the process is still running
if ps -p $cicflowmeter_pid > /dev/null; then
    echo "cicflowmeter process is still running."
else
    echo "cicflowmeter process has been terminated."
fi

