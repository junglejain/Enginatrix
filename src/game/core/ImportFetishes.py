import yaml

stream = open('../../../Content/fetishes.yaml', 'r')
fetishes = yaml.load_all(stream)

for fetish in fetishes:
    print(fetish)