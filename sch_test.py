#!/usr/bin/env python
# coding: utf-8

# In[3]:


import os
import datetime

filename = "_scheduled_task.txt"
filepath = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop', filename)

current_datetime = datetime.datetime.now()
date_string = current_datetime.strftime("%Y-%m-%d %H:%M:%S")

print(date_string)
with open(filepath, "w") as f:
    f.write(date_string)

