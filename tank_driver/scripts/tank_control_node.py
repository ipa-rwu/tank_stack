#!/usr/bin/env python

from src.tank_control.tank_control import TankControl

def main():
    driver = TankControl()

    # Run driver. This will block
    driver.run()


if __name__ == '__main__':
    main()