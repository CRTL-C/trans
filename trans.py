import colorama   # for colored text because we love colors in terminal

#colors
SB = '\033[96m'  #skyblue
P = '\033[95m'  #pink
B = '\033[94m'  #blue
Y = '\033[93m'  #yellow
G= '\033[92m'   #green
R = '\033[91m'  #red
W = '\033[90m' #white


print(""" %s
                                      tttt
                                      t  t
                                      t  t                                             
                                 tttttt  tttttt   %s  rrrrrrrrr        aa                  nn
                                                                                        n    n            ssssssssss
                               ttttttt %s ttttttt   rrrrrrrrrr      aaa  aa           nn      nn          s      
                                      t  t          rrr          aaa      aa         nn        nn         s   s    
                                      t  t          rrr          aa  %s   aaa        nn        nn         ssssssss 
                                      t  t          rrr          aa      aaaa        nn        nn               ss
                                                                                                                  
        
                                          (TRANSLATE PDFS AND  TEXT FILES)

                                          %sby Adhrit 
                                           twitter : https://twitter.com/xadhrit 
                                           github : https://github.com/xadhrit 
                                                 
       """%(R,Y,SB,G, P))




# Standard Libraries
import os
import time

## installed libs
from google_trans_new import google_translator  #google api interface 
from PyPDF2 import PdfFileReader        # lib for various pdf operations
from pdfminer.high_level import extract_text   #lib for  extracting text from pdf
from multiprocessing.dummy import Pool as ThreadPool ## concurrecy and creating pools



pool = ThreadPool(8)

### asking for language in which you want to translate your pdf
lang = input( "Enter target language : e.g. (en- english,zh- chienese, th-thai, de-destuche ) : ")

# asking for where is pdf file
_path = input(str(G+"Enter pdf file path or name(if in same folder) : "))

def check_file(_path):
        file_path, extension = os.path.splitext(_path)
        if (extension == '.pdf'):
            print('We got the pdf {}'.format(_path))

        else:
            print( R + 'Invalid file or not a pdf ')

def request(text):
    translator = google_translator(timeout=10)
    translated_text = translator.translate(text.strip(), lang)                                                              
    return translated_text



def translate_func():
    
    
    # open , read  and get pages from pdf
    check_file(_path)
    name, ex = os.path.splitext(_path)
    fp = open(_path, 'rb')
    reader = PdfFileReader(fp)
    num_pages = reader.numPages
    print(B + "Pdf contents {} pages".format(num_pages))

    #extracting text
    
    time_before= time.time()
    text = extract_text(_path)
    time_after = time.time()
    print( P +"Extracting text from Each Page of {} in total of {} seconds".format(_path, time_after-time_before))
   
    ## putting all text in one new file
    fw = open(f'{name}.txt'  , 'w')
    fw.write(text)
    
    print(SB +  'Successfully created text file for all text ')

    ## start translating stuff
    
    time_first = time.time()

    with open(f'{name}.txt', 'r') as fn:
        lines = fn.readlines()
        try:
            results = pool.map(request, lines)
            pass
        except Exception as error:
            raise error

        pool.close()
        pool.join()

        time_second = time.time()

        print("Translating in %s  in a total of %s seconds"%(len(lines), time_second-time_first))
        fn.close()
        result_file = f'{name}_{lang}.txt'
        result = open(result_file, 'w')
        result.write(str(results))
        print('  Created your %s lang translated text file of %s  '%(lang, _path))





def main():
    translate_func()


if __name__ == '__main__':
    main()


    



