import os

g = os.walk("/Users/darren/work/tmp/com.wuba_10.22.6_liqucn.com/")

for path,dir_list,file_list in g:
    for file_name in file_list:
        if file_name.endswith(('.dex')):
            print(file_name);
            path_dex = os.path.join(path, file_name);
            print(path_dex);
            commd = "/usr/local/bin/jadx -d out -j 4 "+ path_dex
            print(commd);
            os.system(commd);
