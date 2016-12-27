import curses
import json
import datetime

data = []


# y, x = std.getyx()
def main(std):
    offset = 0
    while True:
        max_y, max_x = std.getmaxyx()
        c = screen.getch()
        if c != -1:
            if c == 266:  # F2
                print(std.getmaxyx())
            elif c == 267:  # F3
                exit()
            elif c == 258:  # Down
                offset -= 1
                draw(max_y, offset)
                std.refresh()
            elif c == 259:  # Up
                offset += 1
                draw(max_y, offset)
                std.refresh()
            elif c == 10:  # Enter
                pass  # draw()
            screen.refresh()


def draw(max_y, offset=0, std=None):
    screen.erase()
    for i in range(max_y-1):
        message = data[offset + i]
        when = datetime.datetime.fromtimestamp(int(message['date'])).strftime('%d.%m %H:%M:%S')
        text = message['body']
        out = 'OUT' if message['out'] == 1 else 'IN'
        a = str(message['id'])
        if 'attachments' in message:
            a += ' a'
        resp = a + when + out + text  # ' '.join([a, when, out, text])
        screen.addstr(i, 1, resp)


with open('output_m/messages/216700259.json', 'r') as f:
    data = json.load(f)

screen = curses.initscr()
draw(10)
curses.wrapper(main)
curses.endwin()
