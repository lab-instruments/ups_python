import requests

led_post = requests.post('http://10.1.1.172:8088/led', json={'led_val': 3})

print(led_post)
print(led_post.text)
