import os

PARENT_DIR = os.environ.get('BOARDGAME_ASSET_PATH')
bg_name = 'railroad_ink'
f = open(PARENT_DIR + '/' + bg_name + '/' + bg_name + '_page0.txt')
print(f.read())