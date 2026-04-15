# shuttle-stop-crowd-ranking - Quick Sort Visualization

## Chosen Problem

The problem I have chosen is the shuttle stop crowd ranking, I chose to implement and visualize quick sort. I chose quick sort because the problem is asking to sort a single value crowd_count. This type of problem is something that quick sort would handle well and quick sort is easy to visualize as the algorithm repeatedly picks a pivot, compares it to other values, and splits them into smaller and larger groups. The main assumption for this problem is that crowd_count is a valid number so (crowd_count>=0), the other assumption is that it is okay to not perserve original order of equal values, as quick sort is not stable.

When the user runs the similation there is a bar chart where the similation happens. The user will notice 4 tags which indicate the status of that specific bar/stop. 

Tags:

[PIV]=Pivot (Pivot value)

[SWP]=Swap (Indicates which two values are being swapped)

[CMP]=Compare (Indicates which value is being compared to the pivot)

[   ]=Active subarray (part of the current section of the list that the recursive call is sorting)
## Demonstration

https://github.com/user-attachments/assets/94faabc0-970f-48c2-b7d3-d12ee3bf508a

## Problem Breakdown & Computational Thinking

**Decomposition:** This problem can be broken down into multiple steps
1. Take a list of shuttle stops, each stop has a `stop_name` and `crowd_count`
2. Choose a pivot value
3. Compare other values to pivot
4. Move smaller or larger crowd counts to the left or right side of the pivot
5. Put pivot in correct position
6. Repeat the process on left and right sublist
7. Display the results lowest to greatest

**Pattern Recognition:** Quick sort is repeated over and over again. It picks a pivot, compare pivot to other values, swap values that are in the wrong spot, puts pivot in correct position and repeat on the smaller sublists

**Abstraction:** The details that need to be shown are, the curren list order, pivot value, which values are being compared, which values are being swapped, and the current subarray that is being sorted. This will be shown using a horizontal bar chart, with tags to indicate the status. Details that the user doesn't need to know are things like variable namaes.

**Algorithm Design:** The user will see a editable table with all the shuttle stop data. Each row has `stop_name` and `crowd_count` , the user can add a new stop, remove a stop, and load sample stop data. For processing the program will go through the shuttle stop data to verify that it is valid, and runs quick sort on the list. For output the GUI will show a bar chart that updates as the sort is happening, and below it will be the full step history.

## Flowchart
<img width="297" height="678" alt="flowchart" src="https://github.com/user-attachments/assets/515f1a49-45c7-4590-995b-7782cae7e29d" />

## Steps to Run

Step 1: Download the latest version of python from: `https://www.python.org/downloads/`

Step 2: Open your terminal and verify that python is installed by running `pip --version` in the terminal 

Step 3: Install Gradio by running `pip install gradio` in the terminal

Step 4: Download `app.py` from the Github repo

Step 5: In the terminal run `python app.py`

Step 6: While the terminal is still open, open `http://localhost:7860` in your browser

Step 7: Run the simulation

## Hugging Face Link
https://huggingface.co/spaces/elvt/shutte-stop-crowd-ranking

## Tests
Test 1: When given only one stop, the app correctly handles it by returning the stop as there is nothing to sort and displaying a message in the status
<img width="2169" height="1305" alt="Test 1" src="https://github.com/user-attachments/assets/3fedab99-e7d9-426f-87e9-d50d7beccd7b" />

Test 2: When `crowd_count` is not a valid number (not greater than or equal to 0) the app displays a message in the status box, and ignores that stop and continues to sort the rest of the data without it
<img width="2174" height="1306" alt="Test 2" src="https://github.com/user-attachments/assets/cda56d74-587a-4d82-b396-200cada3ba28" />

Test 3:  When `stop_name` is left empty, the app displays a message in the status box, and ignores that stop and continues to sort the rest of the data without it
<img width="2177" height="1310" alt="Test 3" src="https://github.com/user-attachments/assets/d12ec8ef-444b-430e-ae84-57fb148aaf24" />

## Author & AI Acknowledgment
Author: Elvis Tann
Section: 001

Sources: CISC 121 Notes

**AI WAS USED (LEVEL 4):** This project was made with the help of Claude, I used the code from Claude and made changes to fix some bugs like the alignment of the bar chart being off, as well as adding personalized sample data. All code was reviewed, commented on and understood by me.
https://claude.ai/share/8f6a9773-26ec-4633-943f-dfa36235737b


