#TODO : make more generic?
def mangling(prefix, decl):
    print("%s_%s" % (prefix, decl["name"]))
    return decl["name"]
