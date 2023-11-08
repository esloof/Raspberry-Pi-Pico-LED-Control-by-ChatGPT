import network
import machine
import usocket as socket

led_pin = machine.Pin("LED", machine.Pin.OUT)
html = """<!DOCTYPE html>
<html>
<head> <title>Raspberry Pi Pico LED Control</title> </head>
<body>
LED Control:
<form method="get" action="toggle">
<button type="submit">Toggle LED</button>
</form>
</body>
</html>
"""

# Set up WiFi connection
wlan = network.WLAN(network.STA_IF)
wlan.active(True)  # Activate the wireless interface
wlan.connect('WiFi', 'Password')  # Replace with your SSID and password
while wlan.isconnected() == False:
        print('Waiting for connection...')
        sleep(1)
print(wlan.ifconfig())

# Initialize socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)

while True:
    conn, addr = s.accept()
    print("Got a connection from %s" % str(addr))
    request = conn.recv(1024)
    request = str(request)
    print("Content = %s" % request)
    led_on = request.find('/toggle')
    if led_on == 6:
        led_pin.value(not led_pin.value())  # Toggle LED

    response = html
    conn.send('HTTP/1.1 200 OK\n')
    conn.send('Content-Type: text/html\n')
    conn.send('Connection: close\n\n')
    conn.sendall(response)
