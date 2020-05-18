# A Garbage IOT Project

A micropython project that provides weekly garbage/waste day information on a compatible micro controller like ESP32, ESP8266, etc. This specific example uses Brampton city's public 3rd party api to download the aforementioned information. 

The project also goes through the process of updating a local proxy of the api data. We also go through the process of parsing the calendar(ics) files on the micro to overcome the onboard memory limitations of 1 megabit of the specific board I used. Switching over to the parsing method from the direct calls to the api allows for a lot less reliance on internet access for the device, as long as we have a fresh-enough set of datapoints in the local proxy that we can rely on those for the weekly data.

This way, we can completely switch between data-saver and latest-updates mode (the switching function has not been implemented, however the individual ideas have been shown to work in isolation). 

### The sleep problem
The last thing I tried to add to this project was a deep/shallow sleep feature to save battery life. I did compare the deepsleep feature built into the board I was using compared to a simple shallow sleep with turning off the display and setting a sleep interval. Unfortunately, I didn't save the results of the boot up time and battery performance; comparing full shutdown, deep sleep and shallow sleep and found that shallow sleep was the most responsive and the fastest way of getting the results displayed on the screen with deep sleep and full reboot taking almost the same amount of time with deep sleep being about a second faster. I believe I could make the deep sleep function work a lot better with some hardware changes, but I was way past the point that I was interested in optimising this feature of the project, and the toll on battery-life was far from adverse when compared to the other two methods. Moreover, I think the in-build clock speed management system of these boards brings a lot more in power savings, even when not using the deep sleep feature. Finally, I was using a 18650 cell to power this things, so while the power consumption figures would look a lot different between deep sleep and my implementation of sleep, the large cell and sparse usage brings the practical differences a lot closer than I initially thought.

### Hardware Details

I used a 128x32px oled screen to display the information. I also used a battery powered variant of the node-mcu 8266 board, which has slightly different GPIO pins from the ESP32 which is the better-suited micro for this use-case, but any pin-out diagram should help you to figure out what the pins should be. I used a simple button for the sleep/wake function.
