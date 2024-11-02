velocity = 0
distance = 0

while True:
    acc = AccX - AccErrorX
    velocity += (acc * elapsedTime)
    distance += velocity*elapsedTime + (0.5*acc*(elapsedTime**2))

