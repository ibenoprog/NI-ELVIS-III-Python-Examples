"""
NI ELVIS III Serial Peripheral Interface Example
This example illustrates how to write data to or read data from a Serial
Peripheral Interface (SPI) slave device through the SPI channels on the NI
ELVIS III. The program first defines the configuration for the SPI
channels, and then writes to and reads from the device. Each time the write
function is called, a list of data is written to the SPI device; each time the
read function is called, a list of data is returned from the SPI device.

The SPI configuration consists of six parameters: frequency, bank, clock_phase,
clock_polarity data_direction, and frame_length. There are two identical banks
of SPI port (A and B). You can configure the port as follows:
    Frequency: 40Hz to 4000000Hz
    Clock phase: leading and trailing
    Clock polaritie: low and high
    Direction: LSB and MSB
    Frame length: 4 to 16

This example uses ADXL345 as the slave device. The 0x00 hexadecimal data sent
from the master device requests the slave device to send back a default device 
code which is equal to 'E5' in hexadecimal or '229' in decimal. This returned
value is used for validation. All the SPI configuration is set correctly and
the connection is functioning correctly if the device ID 'E5' is returned.

See http://www.analog.com/media/en/technical-documentation/data-sheets/ADXL345.pdf
for more details about ADXL345.

The program performs two different acquisitions by using the write/read
functions. Section 1 demonstrates how to use the write function and the read
function separately. Section 2 demonstrates how to use the writeread function
to write to and read from the SPI channel.

This example uses:
    1. Bank A, SPI.CS.
    2. Bank A, SPI.CLK.
    3. Bank A, SPI.MISO.
    4. Bank A, SPI.MOSI.

Hardware setup:
    1. Connect SPI.CS (DIO0) on bank A to SPI.CS of a slave device.
    2. Connect SPI.CLK (DIO5) on bank A to SPI.CLK of a slave device.
    3. Connect SPI.MISO (DIO6) on bank A to SPI.MOSI of a slave device.
    4. Connect SPI.MOSI (DIO7) on bank A to SPI.MISO of a slave device.

Result:
    The program writes 0x00, which specifies the address to read from, to the
    SPI device. Then the program reads back a value from the 0x00 register of
    the SPI device. The returned value is E5 in hexadecimal.
"""
import time
import sys
sys.path.append('source/nielvisiii')
import academicIO
from enums import Bank, SPIClockPhase, SPIClockPolarity, SPIDataDirection

# specify the bank
bank = Bank.A
# specify the frequency, in Hz, of the generated clock signal
frequency = 1000000
# specify the clock phase at which the data remains stable in the SPI
# transmission cycle
clock_phase = SPIClockPhase.LEADING
# specify the base level of the clock signal and the logic level of the
# leading and trailing edges
clock_polarity = SPIClockPolarity.LOW
# specify the order in which the bits in the SPI frame are transmitted
data_direction = SPIDataDirection.MSB
# specify the number of bits that make up one SPI transmission frame
frame_length = 8

##############################################################################
# Section 1:
# You use the write function and the read function to write to and read from
# the SPI channel.
##############################################################################

# configure an SPI session
with academicIO.SPI(frequency,
                    bank,
                    clock_phase,
                    clock_polarity,
                    data_direction,
                    frame_length) as SPI:
    # specify the bytes to write to the SPI channel
    data_to_write = [0x00]
    # write data to the SPI channel
    SPI.write(data_to_write)
    # specify the number of frame (int) to read from the SPI channel
    number_frames = 1
    # read one byte of data from SPI channel
    value_array = SPI.read(number_frames)
    # print the data
    print "value read from SPI.read: ", value_array[0]

##############################################################################
# Section 2:
# You use the writeread function which reads back a value immediately after it
# is written.
##############################################################################

# configure an SPI session
with academicIO.SPI(frequency,
                    bank,
                    clock_phase,
                    clock_polarity,
                    data_direction,
                    frame_length) as SPI:
    # specify the bytes to write to the SPI channel
    data_to_write = [0x00]
    # write to and read from the SPI channel
    value_array = SPI.writeread(data_to_write)
    # print the data read back from the SPI channel
    print "value read from SPI.writeread: ", value_array[0]
