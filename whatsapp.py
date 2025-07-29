import pywhatkit

# Phone number in international format (e.g., +1234567890)
phone_number = "+31623907736"
message = "Hello, this is a test message!"
# Time to send the message (24-hour format, e.g., 14 for 2 PM, 30 for minutes)
hour = 9
minute = 47

pywhatkit.sendwhatmsg_instantly(phone_number, message)