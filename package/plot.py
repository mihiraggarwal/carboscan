import numpy as np
import matplotlib.pyplot as plt
import subprocess
from PIL import Image
import os

# bar graph
# scatter plot
# Bar chart on polar axis
#colors = ['pink', 'lightblue', 'lightgreen']

def runcmd(cmd, verbose = False, *args, **kwargs):

    process = subprocess.Popen(
        cmd,
        stdout = subprocess.PIPE,
        stderr = subprocess.PIPE,
        text = True,
        shell = True
    )
    std_out, std_err = process.communicate()
    if verbose:
        print(std_out.strip(), std_err)
    pass
runcmd("wget -P /tmp https://raw.githubusercontent.com/h4pZ/rose-pine-matplotlib/main/themes/rose-pine.mplstyle")

def create_subplots():
    data = {'apple': 10, 'orange': 15, 'lemon': 5, 'lime': 20}
    names = list(data.keys())
    values = list(data.values())

    fig, axs = plt.subplots(1, 3, figsize=(9, 3), sharey=True)
    axs[0].bar(names, values)
    axs[1].scatter(names, values)
    axs[2].plot(names, values)
    fig.suptitle('Categorical Plotting')

    # path exists
    if os.path.exists("package/static/chart.png"):
        os.remove("package/static/chart.png")
        plt.savefig("package/static/chart.png")
    else:
        plt.savefig("package/static/chart.png")

with plt.style.context("/tmp/rose-pine.mplstyle"):
    create_subplots()