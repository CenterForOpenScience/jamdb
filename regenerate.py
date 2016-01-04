import jam

nsm = jam.NamespaceManager()

share_ns = nsm.get_namespace('SHARE')

for collection_name in share_ns.keys():
    share_ns.get_collection(collection_name).regenerate()
