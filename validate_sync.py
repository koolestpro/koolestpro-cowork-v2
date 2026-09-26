import json

path = 'ridwan_content_system_updated.html'
content = open(path, encoding='utf-8').read()
start_marker = '<script id="cowork-sync-data" type="application/json">'
start = content.index(start_marker) + len(start_marker)
end = content.index('</script>', start)
d = json.loads(content[start:end])
print('sync data OK, items:', len(d['items']))
ids = [i['id'] for i in d['items']]
print('duplicate ids:', len(ids) - len(set(ids)))
new_item = [i for i in d['items'] if i['id'] == 'static-ad-obvi_super-collagen-protein-20260711']
print('new item present:', len(new_item) == 1)
if new_item:
    for k in ['id','type','title','slug','status','day','created','folder','week','month','monthSlug']:
        assert k in new_item[0], f'missing field {k}'
    print('all required fields present, status =', new_item[0]['status'])
