import spidev
import RPi.GPIO as GPIO
import time
import sys
import os


#cache 
CACHE_FILE='/tmp/lines.txt'

# GPIO pins for LCD
RST_PIN = 11  # Reset
DC_PIN = 13   # Data/Command

ROWS = 6
COLUMNS = 14
PIXELS_PER_ROW = 6

# LCD Commands
LCD_COMMAND = 0
LCD_DATA = 1
LCD_WIDTH = 84
LCD_HEIGHT = 48
CONTRAST= [0x21, 0x14, 0xaa, 0x20, 0x0c]# ASCII Font 5x7 (You can define your custom font here)
FONT = {
  ' ': [0x00, 0x00, 0x00, 0x00, 0x00],
  '!': [0x00, 0x00, 0x5f, 0x00, 0x00],
  '"': [0x00, 0x07, 0x00, 0x07, 0x00],
  '#': [0x14, 0x7f, 0x14, 0x7f, 0x14],
  '$': [0x24, 0x2a, 0x7f, 0x2a, 0x12],
  '%': [0x23, 0x13, 0x08, 0x64, 0x62],
  '&': [0x36, 0x49, 0x55, 0x22, 0x50],
  "'": [0x00, 0x05, 0x03, 0x00, 0x00],
  '(': [0x00, 0x1c, 0x22, 0x41, 0x00],
  ')': [0x00, 0x41, 0x22, 0x1c, 0x00],
  '*': [0x14, 0x08, 0x3e, 0x08, 0x14],
  '+': [0x08, 0x08, 0x3e, 0x08, 0x08],
  ',': [0x00, 0x50, 0x30, 0x00, 0x00],
  '-': [0x08, 0x08, 0x08, 0x08, 0x08],
  '.': [0x00, 0x60, 0x60, 0x00, 0x00],
  '/': [0x20, 0x10, 0x08, 0x04, 0x02],
  '0': [0x3e, 0x51, 0x49, 0x45, 0x3e],
  '1': [0x00, 0x42, 0x7f, 0x40, 0x00],
  '2': [0x42, 0x61, 0x51, 0x49, 0x46],
  '3': [0x21, 0x41, 0x45, 0x4b, 0x31],
  '4': [0x18, 0x14, 0x12, 0x7f, 0x10],
  '5': [0x27, 0x45, 0x45, 0x45, 0x39],
  '6': [0x3c, 0x4a, 0x49, 0x49, 0x30],
  '7': [0x01, 0x71, 0x09, 0x05, 0x03],
  '8': [0x36, 0x49, 0x49, 0x49, 0x36],
  '9': [0x06, 0x49, 0x49, 0x29, 0x1e],
  ':': [0x00, 0x36, 0x36, 0x00, 0x00],
  ';': [0x00, 0x56, 0x36, 0x00, 0x00],
  '<': [0x08, 0x14, 0x22, 0x41, 0x00],
  '=': [0x14, 0x14, 0x14, 0x14, 0x14],
  '>': [0x00, 0x41, 0x22, 0x14, 0x08],
  '?': [0x02, 0x01, 0x51, 0x09, 0x06],
  '@': [0x32, 0x49, 0x79, 0x41, 0x3e],
  'A': [0x7e, 0x11, 0x11, 0x11, 0x7e],
  'B': [0x7f, 0x49, 0x49, 0x49, 0x36],
  'C': [0x3e, 0x41, 0x41, 0x41, 0x22],
  'D': [0x7f, 0x41, 0x41, 0x22, 0x1c],
  'E': [0x7f, 0x49, 0x49, 0x49, 0x41],
  'F': [0x7f, 0x09, 0x09, 0x09, 0x01],
  'G': [0x3e, 0x41, 0x49, 0x49, 0x7a],
  'H': [0x7f, 0x08, 0x08, 0x08, 0x7f],
  'I': [0x00, 0x41, 0x7f, 0x41, 0x00],
  'J': [0x20, 0x40, 0x41, 0x3f, 0x01],
  'K': [0x7f, 0x08, 0x14, 0x22, 0x41],
  'L': [0x7f, 0x40, 0x40, 0x40, 0x40],
  'M': [0x7f, 0x02, 0x0c, 0x02, 0x7f],
  'N': [0x7f, 0x04, 0x08, 0x10, 0x7f],
  'O': [0x3e, 0x41, 0x41, 0x41, 0x3e],
  'P': [0x7f, 0x09, 0x09, 0x09, 0x06],
  'Q': [0x3e, 0x41, 0x51, 0x21, 0x5e],
  'R': [0x7f, 0x09, 0x19, 0x29, 0x46],
  'S': [0x46, 0x49, 0x49, 0x49, 0x31],
  'T': [0x01, 0x01, 0x7f, 0x01, 0x01],
  'U': [0x3f, 0x40, 0x40, 0x40, 0x3f],
  'V': [0x1f, 0x20, 0x40, 0x20, 0x1f],
  'W': [0x3f, 0x40, 0x38, 0x40, 0x3f],
  'X': [0x63, 0x14, 0x08, 0x14, 0x63],
  'Y': [0x07, 0x08, 0x70, 0x08, 0x07],
  'Z': [0x61, 0x51, 0x49, 0x45, 0x43],
  '[': [0x00, 0x7f, 0x41, 0x41, 0x00],
  '\\': [0x02, 0x04, 0x08, 0x10, 0x20],
  ']': [0x00, 0x41, 0x41, 0x7f, 0x00],
  '^': [0x04, 0x02, 0x01, 0x02, 0x04],
  '_': [0x40, 0x40, 0x40, 0x40, 0x40],
  '`': [0x00, 0x01, 0x02, 0x04, 0x00],
  'a': [0x20, 0x54, 0x54, 0x54, 0x78],
  'b': [0x7f, 0x48, 0x44, 0x44, 0x38],
  'c': [0x38, 0x44, 0x44, 0x44, 0x20],
  'd': [0x38, 0x44, 0x44, 0x48, 0x7f],
  'e': [0x38, 0x54, 0x54, 0x54, 0x18],
  'f': [0x08, 0x7e, 0x09, 0x01, 0x02],
  'g': [0x0c, 0x52, 0x52, 0x52, 0x3e],
  'h': [0x7f, 0x08, 0x04, 0x04, 0x78],
  'i': [0x00, 0x44, 0x7d, 0x40, 0x00],
  'j': [0x20, 0x40, 0x44, 0x3d, 0x00],
  'k': [0x7f, 0x10, 0x28, 0x44, 0x00],
  'l': [0x00, 0x41, 0x7f, 0x40, 0x00],
  'm': [0x7c, 0x04, 0x18, 0x04, 0x78],
  'n': [0x7c, 0x08, 0x04, 0x04, 0x78],
  'o': [0x38, 0x44, 0x44, 0x44, 0x38],
  'p': [0x7c, 0x14, 0x14, 0x14, 0x08],
  'q': [0x08, 0x14, 0x14, 0x18, 0x7c],
  'r': [0x7c, 0x08, 0x04, 0x04, 0x08],
  's': [0x48, 0x54, 0x54, 0x54, 0x20],
  't': [0x04, 0x3f, 0x44, 0x40, 0x20],
  'u': [0x3c, 0x40, 0x40, 0x20, 0x7c],
  'v': [0x1c, 0x20, 0x40, 0x20, 0x1c],
  'w': [0x3c, 0x40, 0x30, 0x40, 0x3c],
  'x': [0x44, 0x28, 0x10, 0x28, 0x44],
  'y': [0x0c, 0x50, 0x50, 0x50, 0x3c],
  'z': [0x44, 0x64, 0x54, 0x4c, 0x44],
  '{': [0x00, 0x08, 0x36, 0x41, 0x00],
  '|': [0x00, 0x00, 0x7f, 0x00, 0x00],
  '}': [0x00, 0x41, 0x36, 0x08, 0x00],
  '~': [0x10, 0x08, 0x08, 0x10, 0x08],
  '\x7f': [0x00, 0x7e, 0x42, 0x42, 0x7e],
}
SPI_BUS=0
SPI_CS=0
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(RST_PIN, GPIO.OUT)
GPIO.setup(DC_PIN, GPIO.OUT)
spi=spidev.SpiDev()
spi.open(SPI_BUS,SPI_CS)
spi.max_speed_hz=4000000

# Helper functions
def lcd_reset():
    """
    Reset the LCD display by toggling the reset pin.
    """
    GPIO.output(RST_PIN, GPIO.LOW)
    time.sleep(0.1)
    GPIO.output(RST_PIN, GPIO.HIGH)


def update_lines(line: str) -> list:
    """
    Update the cache file with the new line and return the updated list of lines.

    Args:
        line (str): The new line to add to the cache.

    Returns:
        list: The updated list of lines.
    """
    lines = []
    try:
        with open(CACHE_FILE, 'r') as file:
            lines = file.readlines()
    except FileNotFoundError:
        pass

    if len(lines) < ROWS:
        lines.append(line + '\n')
    else:
        lines = [line + '\n']

    with open(CACHE_FILE, 'w') as file:
        file.writelines(lines)

    return [line.strip() for line in lines]

def lcd_write(byte, mode) -> None:
    """
    Write a byte or list of bytes to the LCD display.

    Args:
        byte (int or list): The byte or list of bytes to write.
        mode (int): The mode to write in (LCD_COMMAND or LCD_DATA).
    """
    GPIO.output(DC_PIN, GPIO.HIGH if mode == LCD_DATA else GPIO.LOW)
    if type(byte) is list:
      spi.writebytes(byte)
    else:
      spi.writebytes([byte])

def lcd_command(command) -> None:
    """
    Send a command to the LCD display.

    Args:
        command (int or list): The command to send.
    """
    lcd_write(command, LCD_COMMAND)

def lcd_data(data) -> None:
    """
    Send data to the LCD display.

    Args:
        data (int or list): The data to send.
    """
    lcd_write(data, LCD_DATA)

def lcd_init()->None:
    """
    Initialize the LCD display.
    """
    lcd_reset()
    lcd_command(CONTRAST)
    lcd_command(0x21)  # Extended instruction set
    lcd_command(0xB1)  # Set Vop (contrast)
    lcd_command(0x04)  # Set temperature coefficient
    lcd_command(0x14)  # Set bias mode
    lcd_command(0x20)  # Basic instruction set
    lcd_command(0x0C)  # Display control: normal mode
    lcd_clear()

def lcd_clear()-> None:
    """
    Clear the LCD display.
    """
    white_board = [0] * (ROWS * COLUMNS * PIXELS_PER_ROW)
    lcd_data(white_board)

def lcd_set_cursor(x, y)-> None:
    """
    Set the cursor position on the LCD display.

    Args:
        x (int): The x-coordinate of the cursor.
        y (int): The y-coordinate of the cursor.
    """
    lcd_command([x+128, y+64])

def lcd_print(lines: list)-> None:
    """
    Print lines (new line new row) of text to the LCD display.

    Args:
        lines (list): The lines of text to print.
    """
    for row,line in enumerate(lines):
      lcd_set_cursor(0, row)       
      for char in line:
         lcd_data(FONT[char])

def main():
    lcd_init()
    lcd_set_cursor(0, 0)
    if len(sys.argv) > 1:
        user_input = sys.argv[1]
        if user_input == "--clear":
            lcd_clear()
            if os.path.exists(CACHE_FILE):
                os.remove(CACHE_FILE)
        else:
            lcd_print(update_lines(user_input))
        
    else:
        print("Please provide text to display as the first argument.")

if "__main__" == __name__:
    main()