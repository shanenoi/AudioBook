from gtts      import gTTS
from threading import Thread
from sys       import argv
import os
import time
import re

args = argv[1].split("::")
FILE = args[0]
LANG = args[1]
PROCESSES_REMAIN = 0
MEM_EACH = 19832
FREE = int(
    re.findall(
        r"Mem: +\d+ +\d+ +(\d+)",
        os.popen("free").read()
    )[0]
)


def text_to_speech(array_sentences, process_name="main"):
    global PROCESSES_REMAIN

    for index, val in array_sentences:
        # time.sleep(0.001)
        tts = gTTS(text=val, lang=LANG)
        tts.save(f"tts_temp_{index:010}.mp3")

    PROCESSES_REMAIN -= 1
    print("(+) {}: completed, remain: {}"\
          .format(process_name,
                  PROCESSES_REMAIN
          )
    )
    
    if not PROCESSES_REMAIN:
        rename()


def rename():
    os.system(f"cat tts_temp_*.mp3 > \"{FILE}.meom\" &&"
              f" rm tts_temp_*.mp3 &&"
              f" mv \"{FILE}.meom\" \"{FILE}.mp3\""
    )


if __name__ == "__main__":
    array_sentences = [sentence for sentence in 
                       re.findall("([àáãạảăắằẳẵặâấầẩẫậèéẹẻẽêềếểễệđìíĩỉịò"
                                  "óõọỏôốồổỗộơớờởỡợùúũụủưứừửữựỳỵỷỹýÀÁÃ"
                                  "ẠẢĂẮẰẲẴẶÂẤẦẨẪẬÈÉẸẺẼÊỀẾỂỄỆĐÌÍĨỈỊÒÓÕỌ"
                                  "ỎÔỐỒỔỖỘƠỚỜỞỠỢÙÚŨỤỦƯỨỪỬỮỰỲỴỶỸÝA-Za-z ]+)", 
                       open(FILE).read()) if sentence.strip()
    ]

    len_array_sentences = len(array_sentences)
    array_sentences = list(zip(range(len_array_sentences),
                               array_sentences)
    )

    #print(array_sentences)

    thr = int(FREE/MEM_EACH)
    branch = int(len_array_sentences/thr)
    index = 0

    format_zeros = len(str(len_array_sentences))
    if len_array_sentences > thr:
        PROCESSES_REMAIN = thr+1
        for _ in range(0, thr):
            Thread(target=text_to_speech,
                   args=(array_sentences[index:index+branch],
                         f"{{:0{format_zeros}}}->"
                         f"{{:0{format_zeros}}}"\
                         .format(index, index+branch)
                   )
            ).start()
            index += branch
    else:
        PROCESSES_REMAIN = 1

    Thread(target=text_to_speech,
           args=(array_sentences[index:],
                 f"{{:0{format_zeros}}}->end"\
                 .format(index)
           )
    ).start()
