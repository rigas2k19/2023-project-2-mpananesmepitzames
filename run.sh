#!/bin/bash

if [ $# -eq 0 ]; then
    # No argument provided, run all scripts
    echo "Running all scripts..."
    bash Task1/task1.sh
    # python3 Task2/task2.py
    python3 Task3/task3.py
    python3 Task4/task4.py
else
    # Argument provided, run the corresponding script
    case $1 in
        1)
            echo "Running Task1/task1.sh..."
            bash Task1/task1.sh
            ;;
        2)
            echo "Running Task2/task2.py..."
            python3 Task2/task2.py
            ;;
        3)
            echo "Running Task3/task3.py..."
            python3 Task3/task3.py
            ;;
        4)
        echo "Running Task4/task4.py..."
        python3 Task4/task4.py
        ;;
        *)
            echo "Invalid task number."
            exit 1
            ;;
    esac
fi
