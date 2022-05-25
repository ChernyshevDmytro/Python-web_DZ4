import pathlib as pl
import re
import os
import shutil
from threading import Thread


# Creating normalisation dictionary TRANS

CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "u", "ja", "je", "ji", "g")

TRANS = {}
for c, l in zip(CYRILLIC_SYMBOLS, TRANSLATION):
    TRANS[ord(c)] = l
    TRANS[ord(c.upper())] = l.upper() 

# Check if Path exists

def path_verification(path_to_folder):
    path_to_folder=rf'{path_to_folder}'
    i=0
    
    while i<10:
        i+=1 
        p = pl.Path(path_to_folder)
        
        if not p.exists() or p.is_file():
            print(f'Please enter the valid path to folder\nYou have {9-i} attempts')
            path_to_folder = input('Enter path to folder:')

        if i==10:
            break         

        if p.exists():
            path_to_folder_1=rf'{path_to_folder}' 
            return path_to_folder_1
        
# List output of folders and files. Empty folders remove                 
def find_files(path_to_folder_1, founded_files=[], founded_folders=[]):

          
    p = pl.Path(path_to_folder_1) 
                          
    for i,j in enumerate(p.iterdir()):
        
       
        if j.is_file():
            a=pl.PurePath(pl.Path(j))
            a=str(a)                             
            b=a.replace(j.suffix, '')
            b=a.replace(j.name, '')            
                      
            founded_files.append([j.name.replace(j.suffix, ''), j.suffix, b])
            
            
            
        if j.is_dir():
            
            founded_folders.append(os.fspath(j))
            path_to_folder_2=pl.Path(j)

            thread = Thread(target=find_files, args=(path_to_folder_2,))
            thread.start()
            
            
        

        
    #print(f'Please see unsorted list of folders and files bellow: ')
    #print(founded_files)
       
    return path_to_folder_1, founded_files, founded_folders

   

def normalize(founded_files,founded_folders, path_to_folder_1):     
    
    founded_files_normalized=[]
    founded_folders_normalized=[]
    c = len(path_to_folder_1)+1 

    
    for i in founded_files:
        if 'archives' in i[2] or 'video' in i[2] or 'audio' in i[2] or 'documents' in i[2] or 'images' in i[2]:
            founded_files_normalized.append([fr"{i[0]}", fr"{i[1]}", fr"{i[2]}"])
        else:    
            a=i[0] 
            a=i[0].translate(TRANS)
            d=re.sub(r'(\W)', '_', fr"{a}")
            founded_files_normalized.append([fr"{d}", fr"{i[1]}", fr"{i[2]}"])

    for j in founded_folders:
        if 'archives' in j or 'video' in j or 'audio' in j or 'documents' in j or 'images' in j:
            founded_folders_normalized.append(fr'{j}')
        else:
            ss=j[c:].translate(TRANS)
            #print(ss)
            ss=re.sub(r'[^\w^\\]', '_', fr"{ss}")
            founded_folders_normalized.append(fr'{j[0:c]}{ss}')
      
          
    return   founded_files_normalized, founded_folders_normalized


def files_rename(founded_files_normalized, founded_files):
    for  item1, item2 in zip(founded_files, founded_files_normalized): 
    
        if item1[0]!=item2[0]:
            
            os.rename( fr'{item1[2]}{item1[0]}{item1[1]}', fr'{item1[2]}{item2[0]}{item2[1]}')
            #print(item1[0])
            #print(item2[0])


def folders_rename(founded_folders, founded_folders_normalized):
   
    for  item3, item4 in zip(founded_folders, founded_folders_normalized):
        
        if item3!=item4:
            print(item3)
            print(item4)
            os.rename( f'{item3}', f'{item4}')   

def files_collect_images(founded_files, path_to_folder):
    list_of_images=[]
    for k in founded_files:
        
        
        if (k[1].casefold()=='.JPEG'.casefold() or k[1].casefold()=='.PNG'.casefold() or k[1].casefold()=='.JPG'.casefold() or k[1].casefold()=='.SVG'.casefold())\
            and fr"{path_to_folder}\images" not in  fr"{k[2]}":
             
            list_of_images.append(f"{k[0]}{k[1]}")
            if not pl.Path(fr"{path_to_folder}\images").exists():

                os.mkdir(fr'{path_to_folder}\images')
               

            
            os.replace(fr'{k[2]}{k[0]}{k[1]}' , fr"{path_to_folder}\images\{k[0]}{k[1]}")
    print(f"List of images: {list_of_images}")    

def files_collect_video(founded_files, path_to_folder):
    list_of_video=[]
    for k in founded_files:
        
        if (k[1].casefold()=='.AVI'.casefold() or k[1].casefold()=='.MP4'.casefold() or k[1].casefold()=='.MOV'.casefold() or k[1].casefold()=='.MKV'.casefold())\
             and fr"{path_to_folder}\video" not in  fr"{k[2]}":

            list_of_video.append(f"{k[0]}{k[1]}")
            if not pl.Path(fr"{path_to_folder}\video").exists():
                os.mkdir(fr'{path_to_folder}\video')

           
            os.replace(fr'{k[2]}{k[0]}{k[1]}' , fr"{path_to_folder}\video\{k[0]}{k[1]}")
    print(f"List of video: {list_of_video}") 

def files_collect_documents(founded_files, path_to_folder):

    list_of_documents=[]
    for k in founded_files:
        
        if (k[1].casefold()=='.DOC'.casefold() or k[1].casefold()=='.DOCX'.casefold() or k[1].casefold()=='.TXT'.casefold() or k[1].casefold()=='.PDF'.casefold()) \
            or k[1].casefold()=='.XLSX'.casefold() or k[1].casefold()=='.PPTX'.casefold() and fr"{path_to_folder}\documents" not in  fr"{k[2]}":
            list_of_documents.append(f"{k[0]}{k[1]}")
            

            if not pl.Path(fr"{path_to_folder}\documents").exists():
                os.mkdir(fr'{path_to_folder}\documents')

                
            
            os.replace(fr'{k[2]}{k[0]}{k[1]}' , fr"{path_to_folder}\documents\{k[0]}{k[1]}")          
    print(f"List of documents: {list_of_documents}")  
    
def files_collect_audio(founded_files, path_to_folder):
    list_of_audio=[]
    for k in founded_files:
        
        if (k[1].casefold()=='.MP3'.casefold() or k[1].casefold()=='.OGG'.casefold() or k[1].casefold()=='.WAV'.casefold() or k[1].casefold()=='.AMR'.casefold())\
              and fr"{path_to_folder}\audio" not in  fr"{k[2]}":

            list_of_audio.append(f"{k[0]}{k[1]}")
            if not pl.Path(fr"{path_to_folder}\audio").exists():
                os.mkdir(fr'{path_to_folder}\audio')

            
            os.replace(fr'{k[2]}{k[0]}{k[1]}' , fr"{path_to_folder}\audio\{k[0]}{k[1]}")  
    print(f"List of audio: {list_of_audio}")  
 
def files_collect_archives(founded_files, path_to_folder):
    list_of_archives=[]
    for k in founded_files:
        
        if (k[1].casefold()=='.ZIP'.casefold() or k[1].casefold()=='.GZ'.casefold() or k[1].casefold()=='.TAR'.casefold())  and fr"{path_to_folder}\archives" not in  fr"{k[2]}":
            list_of_archives.append(f"{k[0]}{k[1]}") 

            if not pl.Path(fr"{path_to_folder}\archives").exists():
                os.mkdir(fr'{path_to_folder}\archives')

            
            #os.replace(fr'{k[2]}{k[0]}{k[1]}' , fr"{path_to_folder}\archives\{k[0]}{k[1]}")
            
            shutil.unpack_archive(fr'{k[2]}{k[0]}{k[1]}',  fr"{path_to_folder}\archives\{k[0]}")
             
    print(f"List of archives: {list_of_archives}")  

       




def files_collect_other_files(founded_files, path_to_folder):
    list_of_unknown_suffix=set()
    list_of_known_suffix=set()
    
    list_of_other_files=[]
    for k in founded_files:
        list_of_known_suffix.add(k[1])
        if 'archives' in k[2] or 'video' in k[2] or 'audio' in k[2] or 'documents' in k[2] or 'images' in k[2]:
            continue
        elif    k[1].casefold()!='.ZIP'.casefold()  and k[1].casefold()!='.GZ'.casefold()   and k[1].casefold()!='.TAR'.casefold()\
            and k[1].casefold()!='.MP3'.casefold()  and k[1].casefold()!='.OGG'.casefold()  and k[1].casefold()!='.WAV'.casefold()  and k[1].casefold()!='.AMR'.casefold()\
            and k[1].casefold()!='.DOC'.casefold()  and k[1].casefold()!='.DOCX'.casefold() and k[1].casefold()!='.TXT'.casefold()  and k[1].casefold()!='.PDF'.casefold()\
            and k[1].casefold()!='.XLSX'.casefold() and k[1].casefold()!='.PPTX'.casefold() and k[1].casefold()!='.AVI'.casefold()  and k[1].casefold()!='.MP4'.casefold()\
            and k[1].casefold()!='.MOV'.casefold()  and k[1].casefold()!='.MKV'.casefold()  and k[1].casefold()!='.JPEG'.casefold() and k[1].casefold()!='.PNG'.casefold()\
            and k[1].casefold()!='.JPG'.casefold()  and k[1].casefold()!='.SVG'.casefold() :      
            list_of_other_files.append(f"{k[0]}{k[1]}")
            if not pl.Path(fr"{path_to_folder}\other_files").exists():
                os.mkdir(fr'{path_to_folder}\other_files')
            list_of_unknown_suffix.add(k[1])
            
            os.replace(fr'{k[2]}{k[0]}{k[1]}' , fr"{path_to_folder}\other_files\{k[0]}{k[1]}")
    list_of_known_suffix=list_of_known_suffix ^ list_of_unknown_suffix

    print(f"List of other files: {list_of_other_files}") 
    print (f"List of known suffix: {list_of_known_suffix}\nList of unknown suffix: {list_of_unknown_suffix}")       


def del_empty_dirs(path_to_folder_1):
    path = pl.Path(path_to_folder_1)
    
    for d in os.listdir(path):
        a = os.path.join(path, d)

        if os.path.isdir(a):
            del_empty_dirs(a)

            if not os.listdir(a) and 'archives' not in a and 'video' not in a and 'audio' not in a and 'documents' not in a and 'images' not in a:
                os.rmdir(a)

def clean():
    
    path_to_folder = input('Enter path to folder:')   
    path_to_folder_1=path_verification(path_to_folder)
    
    
     
    path_to_folder_1, founded_files, founded_folders = find_files(path_to_folder_1)

    
    founded_files_normalized, founded_folders_normalized= normalize(founded_files,founded_folders, path_to_folder_1)

    files_rename(founded_files_normalized, founded_files)
    founded_files.clear()

    founded_files_normalized.clear()
    founded_folders_normalized.clear()
    founded_folders.clear()


    path_to_folder_1=path_verification(path_to_folder)
    
    path_to_folder_1, founded_files, founded_folders = find_files(path_to_folder_1)


    founded_files_normalized, founded_folders_normalized= normalize(founded_files,founded_folders, path_to_folder_1)

    folders_rename(founded_folders, founded_folders_normalized)

    founded_folders_normalized.clear()
    founded_folders.clear()
    founded_files_normalized.clear()
    founded_files.clear()
    
    path_to_folder_1, founded_files, founded_folders = find_files(path_to_folder_1)


    thread_img = Thread(target=files_collect_images(founded_files, path_to_folder))
    thread_img.start()
    
    thread_video = Thread(target=files_collect_video(founded_files, path_to_folder))
    thread_video.start()

    thread_doc = Thread(target=files_collect_documents(founded_files, path_to_folder))
    thread_doc.start()

    thread_audio = Thread(target=files_collect_audio(founded_files, path_to_folder))
    thread_audio.start()

    thread_arch = Thread(target=files_collect_archives(founded_files, path_to_folder))
    thread_arch.start()
    
    thread_other = Thread(target=files_collect_other_files(founded_files, path_to_folder))
    thread_other.start()
    

    del_empty_dirs(path_to_folder_1)


clean()
