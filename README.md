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


