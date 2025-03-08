import os
import json
import sys



if(__name__=="__main__"):
    if(len(sys.argv)<2):
        folder="./createArticle/%05d"%(0,)
        for i in range(99999):
            folder="./createArticle/%05d"%(i,)
            if(not os.path.exists(folder)):
                os.mkdir(folder)
                break
        print(folder)
        with open(folder+"/mainifest.json","w") as j:
            mainifest=dict()
            mainifest["head_image"]=None
            mainifest["short_descript"]=""
            json.dump(mainifest,j)
        with open(folder+"/main.html","w") as m:
            pass
    else:
        folder=sys.argv[1]
        if(os.path.exists(folder)):
            os.remove(folder)
        os.mkdir(folder)
        with open(folder+"/mainifest.json","w") as j:
            mainifest=dict()
            mainifest["head_image"]=None
            mainifest["short_descript"]=""
            json.dump(mainifest,j)
        with open(folder+"/main.html","w") as m:
            pass

