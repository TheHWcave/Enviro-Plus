In Part 1 of my review on Youtube  (see https://youtu.be/L1kl1kVbmBw)
I discussed changes to the BME280 driver by Pimoroni and I showed a little test program that presents and records the results of the 
- BME280 (temperature, pressure, humidity) 
- MICS 6814 (three-in-one gas sensor)
- PMS5003 (particulate matter sensor)

- plus an extra TMP36 temperature sensor to correct the wrong readings from the BME280

Weather_Gas_PM.py is that program
BME280_new.py is the new driver for the BME280

To use this software, you must have the Pimoroni Enviro+ library installed (as explained on their website) and keep both the BME280_new.py and Weather_GAS_PM.py in the same folder.

NOTE:
According to Bosch Sensortec, the internal BME280 temperature_fine variable should be the chip temperature, therefore correction to ambient temperature is wrong and I removed that function from the BME280_new driver and the example.
