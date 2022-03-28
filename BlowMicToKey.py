import sounddevice as sd
import numpy as np
import time
import configparser
from scipy.fft import fft
from pynput.keyboard import Controller


def main():

    sensitivity, key, pressTime = config_handler()

    kb = Controller()

    with sd.InputStream(samplerate=1764, channels=1, dtype='float32') as stream:
        while True:
            signal = np.average(np.abs(fft(stream.read(600)[0])))
            if signal > sensitivity:
                kb.press(key)
                time.sleep(pressTime)
                kb.release(key)

            
def config_handler():
    try:
        config = configparser.ConfigParser(allow_no_value=True)
        config.read('config.cfg')

        sensitivity = float(config['config']['sensitivity'])
        key = config['config']['key_to_press']
        pressTime = float(config['config']['press_time'])
        return sensitivity, key, pressTime
    except KeyError:
        config = configparser.ConfigParser(allow_no_value=True)
        config.add_section('config')
        config.set('config', 'sensitivity', '0.1')
        config.set('config', 'key_to_press', 'f')
        config.set('config', 'press_time', '0.05')
        config.add_section('notes')
        config.set('notes', '; sensitivity value between 0 to 1', None)
        config.set('notes', '; key_to_press examples: a, f12, esc, num_lock, delete', None)
        config.set('notes', '; press_time is the time in seconds for how long the key is pressed', None)
        with open ('config.cfg', 'w') as configfile:
            config.write(configfile)
        print('Generated config file because either no config was found or it was invalid, exit in approx. 5 seconds')
        time.sleep(5)
        exit()


if __name__ == "__main__":
    main()
    