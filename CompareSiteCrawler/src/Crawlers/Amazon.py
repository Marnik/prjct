import re

regex = '%d{12,13}'

match = re.match(regex, '82718273')

print re.match