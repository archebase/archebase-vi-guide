import json,sys
p=sys.argv[1] if len(sys.argv)>1 else 'tokens/archebase.tokens.json'; d=json.load(open(p)); assert all(len(v)==7 and v[0]=='#' for v in d['colors'].values()); print('PASS semantic tokens')
