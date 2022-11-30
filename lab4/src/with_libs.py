from yaml import load, Loader
from dict2xml import dict2xml


data = load(open("schedule.yaml"), Loader=Loader)
f = open("xml_from_yaml_lib.xml", "w", encoding="utf-8")
f.write(dict2xml(data))
