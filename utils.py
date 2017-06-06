from preprocessing import parsing
import os
from glob import glob



for folder in os.listdir('./dataset'):
    print('------------- {} ---------------'.format(folder))
    for file in os.listdir('./dataset/'+folder):
        parsed = parsing('./dataset/'+folder+'/'+file)
        # top 2 length extract
        print('file: {}'.format(file))
        print(sorted([len(x) for x in parsed], reverse=True))
        # print length and other informations
