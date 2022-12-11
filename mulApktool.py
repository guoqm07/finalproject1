import os, time
 
 
# Get the name of a non-directory subfile under a certain path
def get_file_name(file_dir):
     for root, dirs, files in os. walk(file_dir):
 
         return files # Return the names of all non-directory subfiles under the directory
 
 
# Determine whether the file is an apk file
def is_apk_file(file_name):
     res = True
     if file_name.find(".") != -1:
         if file_name.split(".")[1] == "apk":
             res = True
         else:
             res=False
     else:
         res = False
 
     return res
 
 
# Get the channel information value on the apk file name (generally multiple channels are packaged, and the file name will have channel value information). Since the naming method of each development may be different, you can write the relevant code yourself. This code is only applicable to The file is named as an apk file in the following format xx-channel value-xxx.apk
def get_file_name_channel_value(file_dir):
     files_name = get_file_name(file_dir)
     files_name_channel_value = {}
     for i in files_name:
         i_is_apk_file = is_apk_file(i)
         if i_is_apk_file:
             file_name_channel_value = i.split("-")[1]
             files_name_channel_value.update({i: file_name_channel_value})
     return files_name_channel_value
 
 
# Execute the apktool.bat file through the cmd command to decompile the apk file and obtain the channel value in the AndroidManifest.xml file
def get_apk_channel_value(src_file_dir):
     src_files = get_file_name(src_file_dir) # Get all files, excluding folders, excluding paths
 
     # Create a target folder path >>>> for storing the files obtained in the operation
     dest_file_dir = src_file_dir + "\packagefile\\"
     is_existed = os.path.exists(dest_file_dir)
     if not is_existed:
         os.mkdir(src_file_dir + "\packagefile")
     else:
         print("error: {} directory already exists".format(dest_file_dir))
 
     apk_channel_value = {}
     for file_name in src_files:
         file_name_is_apk_file_name = is_apk_file(file_name)
         if file_name_is_apk_file_name: # Filter out apk files
             # Decompile the apk file to the specified file path through the cmd command apktool.bat d apk file path -o decompiled file storage path
             dest_file_path = dest_file_dir + file_name.split(".")[0].replace("signed_zipalign", "unsigned")
             full_file_path = os.path.join(src_file_dir, file_name) # Get all file paths
             unsign_cmd = "apktool.bat d -f " + full_file_path + " -o " + dest_file_path
             res = os. popen(unsign_cmd)
            
             time. sleep(20)
             unsigned_AndroidManifest_path = dest_file_path + "\AndroidManifest.xml"
             with open(unsigned_AndroidManifest_path, "r", encoding="utf-8") as f:
                 for line in f. readlines():
                     if line.find("UMENG_CHANNEL") != -1:
                         content_res = line.split('=')[-1].split('"')[1]
                         apk_channel_value.update({file_name: content_res})
             time. sleep(20)
 
     return apk_channel_value
 
 
 
if __name__ == '__main__':
     apk_file_dir_path = "D:\app_apk"
     re = get_file_name_channel_value(apk_file_dir_path)
     print("The apk file in the {} directory and the channel value of the corresponding file name: {}".format(apk_file_dir_path, re))
 
     re1 = get_apk_channel_value(apk_file_dir_path)
     print("The channel value corresponding to the apk package in the {} directory is: {}".format(apk_file_dir_path, re1))
 
     if re == re1:
         print("Package channel and package file name channel value are the same")
     else:
         print("Package channel and package file name channel value are inconsistent, please compare in detail")