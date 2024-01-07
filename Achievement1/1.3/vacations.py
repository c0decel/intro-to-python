destinations = ['Mexico', 'Poland', 'Japan', 'United States']

your_destination = input("Where are you going for vacation?: ").title()

if your_destination == destinations[0]:
    print("Nice I have been to " + destinations[0] + " I love it")

elif your_destination == destinations[1]:
    print(destinations[1] + "? Damn I wanna go to " + destinations[1] + " I'm jealous")

elif your_destination == destinations[2]:
    print("If I went to " + destinations[2] + " they'd have a food shortage by the time I left")

elif your_destination == destinations[3]:
    print("When you go to " + destinations[3] + ", NEVER sign up for the store credit card they offer you")

else:
    print(your_destination + "? Never heard of it!")

