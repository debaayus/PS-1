
# **PS-1 project at Indira Gandhi Centre for Atomic Research** 

This is a project to satisfy the requirements of BITS F221 Practice School-I Summer term 2021.

### Three parts in the project:
* Backend- Deals with feature extraction, data matrix creation, machine learning with dimensionality reduction
* Frontend- GUI to wrap the backend modules
* Preprocessing- Accepts data from frontend and processes it before sending to the frontend

### Libraries to be used:
* PySimpleGUI
* Matplotlib
* Scikit-learn
* Pandas
* Numpy
* Pyinstaller
---
### **All the above packages were installed as 32-bit packages in a conda virtual environment for running in x86 Windows 7.**
There shouldn't be a problem in running the 32-bit(x86) executable in a 64-bit(x64) Windows OS.

To mirror a similar virtual conda environment as that of the project, use
`set CONDA_FORCE_32BIT=1` before creating the aforementioned environment to run the project.

After setting the 32bit flag to 1, please create the environment using the yml file in the directory:  
`conda env create --file environment.yml`  

If there are conflicts, you can create a similar environment and make conda resolve any conflicts:  
`conda create --name project_name python=3.6 matplotlib numpy pandas scikit-learn git pysimplegui`  
`conda activate project_name`  
`python main.py`  

#### **Note:** 
The above command has to be run every time before activating this project's virtual environment(in a Windows anaconda prompt), otherwise conda won't hesitate to install x64(64-bit) packages in a 32-bit environment. If you use conda regularly, then please set the flag back to 0, after completing your work in this project's 32bit environment.

`set CONDA_FORCE_32BIT=0`



