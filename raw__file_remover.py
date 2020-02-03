# raw__file_remover.py

_names = 'RAW File Remover'
__version__ = '1.0'

_descrt = '''
DESCRIPTION:
В результате выполнения программы в выбранном каталоге, перемещаются в подкаталог Remove, файлы имен которых нет в выбранном каталоге источнике.
Соответствие файлов устанавливается по имени без учета расширения.
Расширения файлов задаются в переменных «ext_src» и «ext_trg».

Практическое применение:
на основании отобранных фотографий в формате jpeg оставить для обработки raw файлы.
'''

import os

def prn_cpr(head=False):
    rep = 70
    if head:
        print('_'*rep)
        print(_names, 'ver: ',__version__)
        print(_descrt)
    else:
        print('\n©Kotelnikov Evgeny  aka Kjeck')
        print('_'*rep) 

def get_lsfiles(param):
    #Формирует список файлов.
    if param == 1:
        text = 'Директория источник:   '
    elif param == 2:
        text = 'Директория назначения: '
    else:
        text = 'Указать директорию(<Ctr+C> для отмены): '
    try:
        path = input(text)
        if path == '': # Enter
             get_lsfiles(3)
    except EOFError: # Ctr+D
        print('(EOF) Ошибка ввода')
        get_lsfiles(3)
    except KeyboardInterrupt: # Ctr+C
        print('Отмена')
        prn_cpr()
        exit()

    # Удалим слеш в конце если он есть
    s = path[-1]
    if s== '/' or s=='\\':
        path = path[:len(path)-1]

    global path_trg
    path_trg = path
        
    if not os.path.exists(path):
        print('Такой директории не существует')
        get_lsfiles(3)
    else:
        ls = os.listdir(path)
        if len(ls) == 0:
            print('Нет файлов в директории')
            get_lsfiles(3)
        else:
            return ls

def del_ext(ls, lext):
    #Удаляет папки и расширения у файлов в списке
    i=0
    while i < len(ls): 
        element = ls[i]
        #Пока не знаю как понять файл это или папка, поэтому предположу, что
        #если в имени нет расширения то это папка и удалю ее из списка файлов
        #для большей простоты - нет точки = нет расширения 
        if element.find('.') == -1:
            del ls[i]
            continue
        ls[i] = element[0:len(element)-lext]
        i+=1
    return ls

def remove_files(ls_src, ls_trg, ext_trg):
    #Перемещает файлы в каталоге назначения в папку Remove

    # Создадим папку
    folder = path_trg+os.sep+'Remove'
    os.makedirs(folder, exist_ok=True)
    if not os.path.exists(folder):
        print('Не удалось создать папку: ',folder)
        return -1

    # Переберем список файлов директории назначения и если имени файла нет
    # в списке исходных файлов переместим файл в каталог Remove
    i=0
    total_remove = 0
    while i < len(ls_trg):
        element = ls_trg[i]
        if not element in ls_src:
            file = path_trg+os.sep+element+'.'+ext_trg
            if os.path.exists(file):
                try:
                    os.replace(file, folder+os.sep+element+'.'+ext_trg)
                    total_remove+=1
                except:
                    return -1
        i+=1
    return total_remove
           
def main():

    prn_cpr(True)
    
    #Расширения файлов в каталогах
    ext_src = 'jpg'
    ext_trg = 'cr2'

    # Получим cписки файлов в каталогах
    ls_src = get_lsfiles(1)
    ls_trg = get_lsfiles(2)
    
    # Удалим расширения и папки из списков файлов 
    ls_src = del_ext(ls_src, len(ext_src)+1)
    ls_trg = del_ext(ls_trg, len(ext_trg)+1)

    # Для статистики
    total_src = len(ls_src)
    total_trg = len(ls_trg)
        
    # Переместим не нужные файлы в каталоге назначения
    res = remove_files(ls_src, ls_trg, ext_trg)
    if res>=0:
        # Вывод статистики
        print('\nФайлы в <',path_trg,'> обработаны')
        print('Файлов в каталоге источнике:  ',total_src)
        print('Файлов в каталоге назначения: ',total_trg)
        print('Удалено файлов:               ',res)
    else:
        print('Что-то пошло не так :(')
    prn_cpr()

main()
