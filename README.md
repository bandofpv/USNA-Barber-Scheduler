# USNA_Barber_Scheduler
This python script is used to automatically schedule USNA Barber shop appointments. 

Usage: (add link to website later)

## Introduction: 

As Midshipmen at the United States Naval Academy, we are required to keep our haircuts within regulation. This being 
said, we have to get our hair cut at least every two to three weeks depending on how close you get your cut. A common 
issue we face to get a haircut on campus is waiting in super long lines. The only way to avoid waiting in line is to 
schedule an appointment via the 
[schedule portal](https://www.usnabsd.com/services/barber-beauty-shop/barber-beauty-shop-scheduler/). This however, 
 only allows  you to schedule two weeks in advance and there's a chance someone already booked an appointment at the 
same time you desire. Midshipmen are often times so pre-occupied with school that it's hard to remember to book a 
haircut appointment, and you find yourself having to wait in line to get a last minute cut. The solution to this is to 
create a program that can automatically schedule appointments for you. The usage is simple, just enter the date and time 
of your appointment into the [dates.txt](https://github.com/bandofpv/USNA_Barber_Scheduler/blob/main/dates.txt) file and 
let the script run on a remote server. Doing so allows you to block out appointment times months in advance and never 
have to wait in line for a haircut. 

## Setup: 

A simple way to create your remote server to run the python auto-scheduling script is to use a Raspberry Pi. In my setup
 I used a Raspberry Pi 4. Any RPI with desktop capabilities will work, but I wanted to test out the new Raspberry Pi 
Connect service which provides easy remote access to your RPI anywhere on the planet, so long as you have access to a 
web browser. 

### Step 1, Installing Raspberry Pi OS

The first step is to install an operating system onto your RPI. Simply follow this 
[tutorial](https://www.raspberrypi.com/documentation/computers/getting-started.html#install-an-operating-system) to get 
started. 

**Note:** if you wish to use [RPI Connect](https://www.raspberrypi.com/documentation/services/connect.html), make sure 
you install the 64-bit OS. Otherwise, any RPI OS with desktop and recommended software should work. 

After a successful RPI OS install, run the following commands to make sure its up to date: 

```
pi@raspberrypi:~ $ sudo apt-get update
pi@raspberrypi:~ $ sudo apt-get upgrade
pi@raspberrypi:~ $ sudo reboot
```

### Step 2, Clone Repository and Install Required Software

Open a terminal window and clone this repository: 

`pi@raspberrypi:~ $ git clone https://github.com/bandofpv/USNA_Barber_Scheduler.git`

We now need to create our python environment. RPI automatically comes with the `venv` module, so we will use that to 
create our virtual environment. To do so, simply enter:

`pi@raspberrypi:~ $ python3 -m venv [name of evironment]`

Where `[name of environment]` is any name of your choosing. 

To now activate our environment, enter: 

`pi@raspberrypi:~ $ source [name of environement]/bin/activate`

Your terminal window should now look somthing like this: 

```
pi@raspberrypi:~ $ source barber/bin/activate
(barber) pi@raspberrypi:~ $
```

Where `barber` is my chosen environment name. 

We can now install the `selenium` python package which allows us to automate web browser interaction using python. In 
your virtual environment, enter: 

`(barber) pi@raspberrypi:~ $ pip install selenium`

With the `selenium` python package installed, we need to install the required driver to allow `selenium` to interact 
with our chosen browser. I personally used Firefox as it comes default with RPI OS. 

Firefox requires the use of GeckoDriver. Knowing which version of GeckoDriver to install can be a little tricky, so 
I recommend looking at this 
[blog post](https://nicolaslouge.com/post/how-to-set-up-selenium-python-geckodriver-raspberry-pi-arm-2023/). In my case, 
because I used the 64-bit OS, I installed the aarch64 version of GeckoDriver: 

```
pi@raspberrypi:~ $ wget https://github.com/mozilla/geckodriver/releases/download/v0.34.0/geckodriver-v0.34.0-linux-aarch64.tar.gz
pi@raspberrypi:~ $ sudo tar -xzvf geckodriver-v0.34.0-linux-aarch64.tar.gz -C /usr/local/bin
pi@raspberrypi:~ $ chmod +x /usr/local/bin/geckodriver
```

To test you installed GeckoDriver correctly, enter: 

`pi@raspberrypi:~ $ geckodriver -V`

You should not get any errors. 

### Step 3, Test The Script

Now, we can test our script to check if all the software was installed correctly. Simply change into our repository 
directory and modify the `main.py` script: 

```
pi@raspberrypi:~ $ cd USNA_Barber_Scheduler
pi@raspberrypi:~ $ nano main.py
```

The first few lines of code under the imports should look like this: 

```
# INPUT FULL_FILEPATH ==> full file path to USNA_Barber_Scheduler directory ex: /home/pi/USNA_Barber_Scheduler
filepath = "FULL_FILEPATH"

# INPUT: ALPHACODE ==> your alpha code
alpha = "ALPHACODE"

# INPUT: "Male Haircut", "Deep Conditioner & Blow Dry", "Shampoo & Haircut", "Blow Dry & Flat Iron", "Braids, or
# "Facial Waxing"
service = "Male Haircut"

# INPUT: "Sharr (Barber)" or "Patty (Beauty/Barber)"
barber = "Sharr (Barber)"
```

Change the string variables to work for your RPI file system and barber shop preferences. Then save and exit. 

Now we need to enter dates into the [dates.txt](https://github.com/bandofpv/USNA_Barber_Scheduler/blob/main/dates.txt) 
file: 

`pi@raspberrypi:~ $ nano dates.txt`

It's crucial that you follow the following format for enter dates: `YEAR-MN-DY HR:MN` with a new line for each 
appointment. Any deviation from this format could cause the script to break. It's important that you also enter times 
which are used on the 
[schedule portal](https://www.usnabsd.com/services/barber-beauty-shop/barber-beauty-shop-scheduler/). Here is an 
example: 

```
2024-06-04 13:20
2024-07-14 13:20
```

Let's test our script. Make sure you are in the virtual environment and run the python script: 

```
pi@raspberrypi:~ $ source barber/bin/activate
(barber) pi@raspberrypi:~ $ python main.py
```

A Firefox window should display and proceed to log in and schedule your appointment. If it is unable to log into your 
account, make sure that your password is set to its default value which should be the digits of your alpha code. 

### Step 4, Set Up Your CronJob

In order for the RPI to run the python script automatically, we can set up a CronJob. First, lets edit/create a crontab:

`pi@raspberrypi:~ $ crontab -e`

Select whatever editor of your choosing and write the following lines at the bottom of the file: 

```
DISPLAY=:0
0 12 * * * [full file path to venv]/bin/python [full file path to repo]/main.py
```

Make sure you fill in the sections with the **full** file path. Below is an example:

```
DISPLAY=:0
0 12 * * * /home/pi/barber/bin/python /home/pi/USNA_Barber_Scheduler/main.py
```

The first line allows the CronJob to access the RPI's local display and the second line runs the python script through 
the virtual environment every day at 12:00. 

You're all set! All you have to do now is keep the RPI powered and connected to the internet and let the code to the 
rest of the work for you.