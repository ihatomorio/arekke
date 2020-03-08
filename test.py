import re, os

s = "https://booth.pximg.net/e8e75036-3788-4cff-b6ac-97397dd0f50a/i/1759716/53acb9de-94cd-4146-9aaf-07e663e20941_base_resized.jpg"

print(re.findall(r'https://.*/(.*_base_resized\.jpg)', s))

print(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

url = s
filename = re.findall(r'https://.*/(.*_base_resized\.jpg)', url)

assert 'resized' in url

path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(path)

path += "/../../media/booth/" + filename[0]
print(path)
