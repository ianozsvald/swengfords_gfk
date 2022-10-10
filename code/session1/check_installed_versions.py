#!/usr/bin/env python
# coding: utf-8

# # Check installed versions for core libraries
# 
# Note to STUDENTS - run this Notebook, we'll check you have the same versions as Ian has.
# 
# BE AWARE if you're running this on the command line, run it in IPython and _make sure you've activated your environment_ else it'll run with the (base) environment which you've not setup. 
# 
# Note for IAN - run this command if we update this Notebook `jupyter nbconvert --to python check_installed_versions.ipynb`

# In[1]:


print("Run this FIRST in a Jupyter Notebook")
print("Run this SECOND using IPython in a Terminal with 'ipython check_installed_versions'")


# In[2]:


import sys
print(f"Python version: {sys.version}")


# In[3]:


import pandas
print(f"pandas version is {pandas.__version__}")


# In[4]:


import numpy as np
print(f"numpy version {np.__version__}")


# In[5]:


import matplotlib
print(f"matplotlib version is {matplotlib.__version__}")


# In[6]:


import pandera
print(f"pandera version {pandera.__version__}")


# In[7]:


import pytest
print(f"pytest version {pytest.__version__}")


# In[9]:


import hypothesis
print(f"hypothesis version {hypothesis.__version__}")


# In[10]:


# your "active env location" should include ".../envs/course"
#!conda info


# In[11]:


# Let's show the system path
# NOTE it is worth us looking at this for a moment to understand where Python is getting imports from
# we expect to see
# a folder to _this_ Notebook (for Ian this might be '/home/ian/workspace/teaching/public_courses/live/swengds_material/code/session1',
# several paths to Python 3.x (e.g. /home/ian/miniconda3/envs/course/lib/python310.zip)
# '' # the empty string means "Python to search modules in the current directory"
# a site-packages folder where all the modules are stored
sys.path


# In[ ]:




