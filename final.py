from djitellopy import Tello
import numpy as np
import time

cards = np.array([
    [85, 14, 6, 55, 65, 25],
    [70, 11, 18, 14, 30, 50],
    [45, 0, 20, 40, 75, 2],
])
tello = Tello()
vertical_amt = 40
horizontal_amt = 18


def main():
    tello.connect()

    battery = tello.get_battery()
    if battery <= 20:
        print("[Warning]: Battery is low.", battery, "%")
    else:
        print("Battery:", battery, "%")

    tello.takeoff()
    tello.move_up(40)
    tello.set_speed(10)
    instructions = get_instructions()
    pop_balloons(instructions)
    tello.land()


def get_instructions():
    pos = [2, 2]
    instructions = [{'up': 0, 'down': 0, 'left': 0, 'right': 0} for _ in range(len(nums))]
    coords = [np.argwhere(cards == n)[0].tolist() for n in nums]

    for i, (target_y, target_x) in enumerate(coords):
        current_y, current_x = pos
        diff_y, diff_x = (target_y - current_y), (target_x - current_x)

        if diff_y < 0:
            instructions[i]['up'] = abs(diff_y)
        elif diff_y > 0:
            instructions[i]['down'] = diff_y

        if diff_x < 0:
            instructions[i]['left'] = abs(diff_x)
        elif diff_x > 0:
            instructions[i]['right'] = diff_x

        prev_pos = pos.copy()
        pos[1] += diff_x
        pos[0] += diff_y
        if prev_pos[1] <= 2 and pos[1] > 2:
            instructions[i]['right'] += 0.6
        if prev_pos[1] > 2 and pos[1] <= 2:
            instructions[i]['left'] += 0.6

    return instructions


def pop_balloons(instructions):
    for instruction in instructions:
        up, down, left, right = instruction['up'], instruction['down'], instruction['left'], instruction['right']
        up, down, left, right = int(round(up)), int(round(down)), int(round(left)), int(round(right))

        if up:
            print('up ', up * vertical_amt, 'cm')
            tello.move_up(up * vertical_amt)
        elif down:
            print('down ', up * vertical_amt, 'cm')
            tello.move_down(down * vertical_amt)

        if left:
            print('left ', left * horizontal_amt, 'cm')
            tello.move_left(left * horizontal_amt)
        elif right:
            print('right ', right * horizontal_amt, 'cm')
            tello.move_right(right * horizontal_amt)

        time.sleep(0.5)
        tello.move_forward(50)
        time.sleep(0.5)
        tello.move_back(50)
        time.sleep(1.5)


if __name__ == '__main__':
    nums = [int(n.strip()) for n in input('Balloons to pop (IDs separated by commas): ').split(',')]
    main()
