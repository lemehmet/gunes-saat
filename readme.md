# Gunes'in Saati
A home made alarm clock to wake up with style and learn how to build things. 
It is based on a Raspberry PI Zero W, uses a fancy OLED display with buttons from Adafruit
and an I2S codec with a power amplifier connected to a medium surface transducer to rock.
The framework has an emulator that features an soft display shown in a window and maps buttons to the keyboard.
## BoM
* Raspberry Pi Zero W, other pies work, too.
* [Adafruit 128x64 OLED Bonnet for Raspberry Pi](https://www.adafruit.com/product/3531). 
It is possible to use other displays with some customization:
  * The pixel format adaptation
  * Button assignments
* [Adafruit I2S 3W Stereo Speaker Bonnet for Raspberry Pi - Mini Kit](https://www.adafruit.com/product/3346).
Pi Zero does not have an headphone output and I2S sounds better anyway. Anything plays nicely with ALSA works.
If you are using non-zero pies, you can simply connect your favorite amplifier to the headphone jack.
* [Medium Surface Transducer with Wires - 4 Ohm 3 Watt](https://www.adafruit.com/product/1785). 
This small paperweight makes all the difference, it turns the bed frame to a speaker. Some notes on usage: 
    * Make sure your amplifier's output impedence matches and can drive these.
    * There is no point in attaching two of them to the same surface.
    * They need to be rigidly attached to the surface.
    * The cables of the model are tiny and fragile.
* The usual necessities
    * [2x20 pin strip](https://www.adafruit.com/product/2822)
    * A good power supply and a powered USB hub
    * A reliable USB OTG cable
    * A keyboard, mini hdmi cable for when things go wrong
    * Soldering iron, wirestripper etc.
 
## Software Installation
* First install raspian, lite version is more than enough. Follow the directions on https://www.raspberrypi.org/downloads/raspbian/.
* Install [circuit python](https://learn.adafruit.com/circuitpython-on-raspberrypi-linux/installing-circuitpython-on-raspberry-pi)
* Install Adafruit 128x64 OLED Bonnet support packages from [here](https://learn.adafruit.com/adafruit-128x64-oled-bonnet-for-raspberry-pi/usage)
* Install Pillow fork that adds native pixel format, improves rendering performance on rpi zero by 50x.
    * Remove repo version of Pillow: `sudo apt remove python3-pil`
    * Install libraries for building Pillow: `sudo apt-get install libjpeg-dev libtiff-dev zlib1g-dev libfreetype6-dev liblcms2-dev libwebp-dev tcl8.6-dev tk8.6-dev`
    * Clone the fork `git clone https://github.com/lemehmet/Pillow.git`
    * Change to the project directory `sudo pip3 install .`    
* Fork/Clone the saat project `git clone https://lemehmet@bitbucket.org/lemehmet/gunes-saat.git

## Wiring
* Before wiring make sure every component works.
* [OLED schematics](https://cdn-learn.adafruit.com/assets/assets/000/042/397/original/raspberry_pi_schem.png?1496866920)

![OLED Schematics](https://cdn-learn.adafruit.com/assets/assets/000/042/397/medium640/raspberry_pi_schem.png)
  
* If you are using 2x20 pin strips to connect two boards, solder audio in-between raspberry pi and oled display for the robustness against wear and tear.
* Follow the guideline for Adafruit I2S 3W Stereo Speaker Bonnet at [here](https://learn.adafruit.com/adafruit-speaker-bonnet-for-raspberry-pi/pinouts)
* [I2S Schematics](https://cdn-learn.adafruit.com/assets/assets/000/037/882/original/raspberry_pi_schem.png)

![I2S Schematics](https://cdn-learn.adafruit.com/assets/assets/000/037/882/medium640/raspberry_pi_schem.png) 

## Software Components

### OledDisplay
This is the base class for the application. It initializes the hardware components, sets up the timers and drives the event loop, as well as the emulator.
```python
import display

class Saat(display.OledDisplay):
    def __init__(self):
        display.OledDisplay.__init__(self)
        # Application specific initialization follows
        # Wherever needed, pass the subclass instance (Saat) for display
        
        # Initialize the views
        clock_view = ClockView(display=self)
        moving_ball = MovingBall(display=self)
        rico_ball = RicoBall(display=self)
        
        # Setup navigation
        rico_ball.set_right(clock_view)
        clock_view.set_left(rico_ball)
        clock_view.set_right(moving_ball)
        moving_ball.set_left(clock_view)
        moving_ball.set_right(rico_ball)
        
        # Set the initial view
        self.vm.set_root_view(rico_ball)
        # And let there be light
        self.vm.paint()
        
```

### View
The application uses views to draw on the display and handle events, such as button and timers. Each view is implemented
independently and only one can be active. The active view receives the events.
`View` is the base class for custom views, it defines default handlers for 
events and keeps a first-order link to neighboring views.

#### Initialization
Just subclass from `View` and initialize. The `RicoBall` example draws a moving ball and randomizes the movement vector 
with Button-A.
```python
import math
import random
import config
from views import View
from common import log_paint, log_fw

PI = math.pi
IKIPI = 2 * PI

class RicoBall(View):
    x = 0
    y = 0
    r = 4
    v = 0.0
    a = 0.0

    def __init__(self, display):
        View.__init__(self, display)
        random.seed()
        self._randomize()

    def _randomize(self):
        self.x = random.randrange(0, config.WIDTH + 1)
        self.y = random.randrange(0, config.HEIGHT + 1)
        self.v = random.random() * 10.0
        self.a = (random.random() - 0.5) * IKIPI
``` 

#### Painting
Implement `on_paint` method and draw using Pillow's image draw elements. Drawing an empty rectangle is a good way to 
start with a clean canvas, however in some cases drawing over the previous frame could be practical. Some drawing 
elements take more cpu time then others, like texts.
Painting and updating the display happen independently. Painting occurs only when the `paint` method is invoked. Usually
views decide when to paint. Display refresh happen periodically, set by `config.UPDATE_FREQ`. The display update method
relies on `mutex_disp` recursive mutex to be MT-Safe.
```python
class RicoBall(View):
    # ...
    def paint(self):
        log_paint.debug(f"RicoBall::paint() {self.x} x {self.y} {self.a} {self.v}")
        with self.display.mutex_disp:
            bounds = ((self.x - self.r, self.y - self.r), (self.x + self.r, self.y + self.r))
            self.display.draw.rectangle((0, 0, self.display.mx, self.display.my), fill=config.BG, outline=config.FG)
            self.display.draw.ellipse(bounds, fill=config.FG, width=self.r)
    # ...
```

#### Activation and De-activation (Gaining and losing focus)
Each time the view is selected to be active, the framework invokes `activate` method, similarly each time the view is 
deselected the framework invokes `deactivate` method. These events give the view the option to react to focus changes.

#### Timer
The framework invokes the active view's `on_sched_event` method **before** the display is updated. Refrain from doing
time consuming tasks in the timer handler. 

```python
class RicoBall(View):
    # ...
    def _move_ball(self):
        dx = math.ceil(self.v * math.cos(self.a))
        dy = math.ceil(self.v * math.sin(self.a))
        if self.x + dx >= config.WIDTH or self.x + dx <= 0:
            dx = -dx
            self.a = _normalize(PI - self.a)
        if self.y + dy >= config.HEIGHT or self.y + dy <= 0:
            dy = -dy
            self.a = _normalize(-self.a)
        self.x += dx
        self.y += dy

    def on_sched_event(self):
        log_fw.debug("RicoBall::on_sched_event()")
        self._move_ball()
        self.paint()
    # ...
```

#### Button Events
There are 7 buttons defined, 4 navigation/joystick, 2 tactile (A and B) and 1 joystick center (C). The framework propagates
the button events to views and invokes the related method. Feel free to invoke paint within these methods, paint is not
part of the event queue.
Button-C is dedicated to navigation and should not be used.
```python
class RicoBall(View):
    # ...
    def on_sched_event(self):
        log_fw.debug("RicoBall::on_sched_event()")
        self._move_ball()
        self.paint()

    def on_button_a(self, pressed, repeated):
        # Re-randomize the initial position, direction and speed
        if pressed and not repeated:
            self._randomize()
        self.paint()

    def on_button_b(self, pressed, repeated):
        # Toggle filled/empty ball
        if pressed and not repeated:
            self.filled = not self.filled
            self.paint()

    def on_button_c(self, pressed, repeated):
        # Do nothing
        pass

    def on_button_up(self, pressed, repeated):
        # Increase the size of the ball
        if pressed:
            self.r = self.r + 1 if self.y < self.display.my else self.display.my
        self.paint()

    def on_button_down(self, pressed, repeated):
        # Decrease the size of the ball
        if pressed:
            self.r = self.r - 1 if self.y > 1 else 1
        self.paint()

    def on_button_left(self, pressed, repeated):
        # Change the direction by 15 degrees to ccw
        if pressed and not repeated:
            self.a = _normalize(self.a + (PI / 12.0))
        self.paint()

    def on_button_right(self, pressed, repeated):
        # Change the direction by 15 degrees to cw
        if pressed and not repeated:
            self.a = _normalize(self.a - (PI / 12.0))
        self.paint()
    # ...
```
`pressed` is `True` when the button is down and `False` when it is up. If the button stays down, the framework invokes 
the same method with`repeated=True`. This helps quick action, such as resizing the ball in the above example.  

#### Navigation
Each view keeps a reference to their first degree neighbors, up, down, left, and right. If a direction is not set, 
or set to None, it is considered empty. The view manager handles the navigation events. Whenever Button-C is pressed 
the framework goes into the navigation mode and stays in nav-mode until Button-C is pressed again. In the nav-mode,
direction buttons are used to select the next view, when a direction key is pressed if a neighbor is defined for that 
direction, the framework changes the active view and performs a simple sliding animation. The old and new views' 
`deactivate` and `activate` methods are invoked respectively.  