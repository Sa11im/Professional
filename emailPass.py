from random import choice
import string
import zipfile
import re


def password(z):
    """Генерация пароля с заданным пользователем количеством символов
    из заглавных и строчных букв, цифр и спецсимволов """
    a, au, n, s = 0, 0, 0, 0
    while True:
        p = (''.join(i for _ in range(z) for i in choice(string.printable.strip())))
        for i in p:
            if i in string.ascii_lowercase:
                a = 1
            if i in string.ascii_uppercase:
                au = 1
            if i in string.digits:
                n = 1
            if i in string.punctuation:
                s = 1
        if a == au == n == s == 1:
            break
    return p


def email_gen(list_of_names):
    """Генерация имейлов на основе фамилии и первой буквы имени"""
    mails = []
    for i in list_of_names:
        letter = 1
        while i[1] + '.' + i[0][0:letter] + '@company.io' in mails:
            letter += 1
        mails.append(i[1] + '.' + i[0][0:letter] + '@company.io')
    return mails


file_name = 'task_file.txt'
# попытка открыть архив
try:
    z = zipfile.ZipFile(f'{file_name}.zip', 'r')
    z.extract(f'{file_name}')
    z.close()
except FileNotFoundError:
    print(f'Архив {file_name}.zip не найден.')
# попытка открыть текстовый файл
try:
    with open(f'{file_name}') as f:
        file = f.readlines()
    rows = []
    for i in file[1:]:
        a = i.split(', ')
        rows.append([a[1].strip(), a[2].strip(), a[3].strip(), a[4].strip()])
    names = []
    mistakes = []

    for i in range(len(rows)):
        pattern_name = r'(^[A-Z]{1}[a-z]{2,})'
        pattern_city = r'([^[A-Z]{1}[a-z].*[A-z]+)'
        pattern_tel = r'^\d{7}$'
        if re.findall(pattern_name, rows[i][0]) and \
                re.findall(pattern_name, rows[i][1]) and \
                re.findall(pattern_city, rows[i][3]) and \
                re.findall(pattern_tel, rows[i][2]):
            names.append([rows[i][0], rows[i][1], rows[i][2], rows[i][3]])
        else:
            mistakes.append([rows[i][0], rows[i][1], rows[i][2], rows[i][3]])

    with open('mistakes_data.txt', 'w') as f:
        f.write('Строки с ошибочными данными:\n')
        for i in mistakes:
            print(i, file=f)
    if mistakes:
        print('Ошибочные данные сохранены в файле mistakes_data.txt')

    mail = email_gen(names)
    with open('task_file.txt', 'w') as f:
        f.write('{:30} {:15} {:15} {:10} {:15} {:15}'.format('Email', 'Name', 'Last_name', 'Tel', 'City', 'Password'))
        print(file=f)
        for i in range(len(names)):
            print('{:30} {:15} {:15} {:10} {:15} {:15}'.format(mail[i], names[i][0], names[i][1], names[i][2],
                                                               names[i][3], password(12)), file=f)

    print('Имейлы и пароли сохранены в файл task_file.txt')
except FileNotFoundError:
    print(f'Не найден {file_name}.\nИмейлы и пароли не сгенерированы.')
