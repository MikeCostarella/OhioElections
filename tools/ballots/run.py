import importlib, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "react-app", "public", "data", "county")
for m in ["mahoning", "columbiana", "ashtabula", "lake", "cuyahoga", "geauga", "summit", "stark", "portage", "medina", "lorain", "franklin", "hamilton", "montgomery", "lucas", "butler", "warren", "delaware", "clermont", "licking", "greene", "fairfield", "clark", "wood", "richland", "wayne", "miami", "allen", "tuscarawas", "muskingum", "ross", "erie", "hancock", "scioto", "belmont", "jefferson", "marion", "union", "knox", "athens", "washington", "pickaway", "sandusky", "huron", "lawrence", "seneca", "darke", "ashland", "shelby", "auglaize", "brown", "logan", "crawford", "highland", "ottawa", "clinton"]:
    c = importlib.import_module(m).build()
    print(m, c.write(OUT), len(c.places), "places")
